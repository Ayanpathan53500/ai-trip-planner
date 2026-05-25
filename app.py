import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient
import requests
from datetime import datetime, timedelta
import pandas as pd

load_dotenv()

GOOGLE_API_KEY   = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY   = os.getenv("TAVILY_API_KEY")
RAPIDAPI_KEY     = os.getenv("RAPIDAPI_KEY")
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
}

# ─────────────────────────────────────────
# FUNCTIONS
# ─────────────────────────────────────────

def get_destination_id(city):
    try:
        search_query = f"{city} India"
        res = requests.get(
            "https://booking-com.p.rapidapi.com/v1/hotels/locations",
            headers=headers,
            params={"name": search_query, "locale": "en-gb"},
            timeout=10
        )
        if res.status_code != 200:
            return None, None

        data = res.json()
        if not data:
            return None, None

        city_lower = city.lower()
        for item in data:
            label   = item.get("label", "").lower()
            country = item.get("country", "").lower()
            if city_lower in label and ("india" in label or "india" in country):
                return item["dest_id"], item["dest_type"]

        return data[0]["dest_id"], data[0]["dest_type"]

    except Exception as e:
        print("Destination error:", e)
        return None, None


def get_route_places(source, destination):
    try:
        geo_url = "https://api.geoapify.com/v1/geocode/search"

        def get_coords(city):
            res = requests.get(geo_url, params={"text": city, "apiKey": GEOAPIFY_API_KEY}).json()
            if not res.get("features"):
                return None
            p = res["features"][0]["properties"]
            return p["lon"], p["lat"]

        start = get_coords(source)
        end   = get_coords(destination)
        if not start or not end:
            return []

        rr = requests.get("https://api.geoapify.com/v1/routing", params={
            "waypoints": f"{start[1]},{start[0]}|{end[1]},{end[0]}",
            "mode": "drive", "apiKey": GEOAPIFY_API_KEY
        }).json()

        if "features" not in rr:
            return []

        coords = rr["features"][0]["geometry"]["coordinates"]
        if isinstance(coords[0][0], list):
            coords = coords[0]

        step = max(1, len(coords) // 6)
        places, seen = [], set()

        for lon, lat in coords[::step]:
            res = requests.get("https://api.geoapify.com/v2/places", params={
                "categories": "tourism.sights,tourism.attraction",
                "filter": f"circle:{lon},{lat},4000",
                "limit": 2,
                "apiKey": GEOAPIFY_API_KEY
            }).json()
            for item in res.get("features", []):
                prop = item["properties"]
                name = prop.get("name", "Place")
                if name in seen:
                    continue
                seen.add(name)
                places.append({
                    "title":   name,
                    "address": prop.get("formatted", ""),
                    "image":   f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=400&height=300&center=lonlat:{prop.get('lon')},{prop.get('lat')}&zoom=14&apiKey={GEOAPIFY_API_KEY}"
                })

        return places[:10]

    except Exception as e:
        print("Route places error:", e)
        return []


def get_hotels(destination, days, budget_max):
    try:
        dest_id, dest_type = get_destination_id(destination)
        if not dest_id:
            return []

        today    = datetime.today()
        checkin  = today + timedelta(days=1)
        checkout = checkin + timedelta(days=max(days, 1))

        res = requests.get(
            "https://booking-com.p.rapidapi.com/v1/hotels/search",
            headers=headers,
            params={
                "dest_id":            dest_id,
                "dest_type":          dest_type,
                "checkin_date":       checkin.strftime("%Y-%m-%d"),
                "checkout_date":      checkout.strftime("%Y-%m-%d"),
                "adults_number":      2,
                "room_number":        1,
                "order_by":           "popularity",
                "locale":             "en-gb",
                "units":              "metric",
                "filter_by_currency": "INR",
                "currency":           "INR",
            },
            timeout=20
        )

        if res.status_code != 200:
            print(f"Hotel API error: {res.status_code}")
            return []

        results = res.json().get("result", [])
        if not results:
            return []

        hotels = []

        for h in results[:30]:
            price    = None
            currency = "INR"

            # Method 1: composite_price_breakdown → gross_amount_per_night
            cpb = h.get("composite_price_breakdown", {})
            if cpb:
                gpn = cpb.get("gross_amount_per_night", {})
                if gpn.get("value"):
                    price    = float(gpn["value"])
                    currency = gpn.get("currency", "INR")
                else:
                    ga = cpb.get("gross_amount", {})
                    if ga.get("value"):
                        price    = float(ga["value"]) / max(days, 1)
                        currency = ga.get("currency", "INR")

            # Method 2: price_breakdown
            if not price:
                pb = h.get("price_breakdown", {})
                if pb.get("gross_price"):
                    price    = float(pb["gross_price"]) / max(days, 1)
                    currency = pb.get("currency", "INR")

            # Method 3: min_total_price
            if not price and h.get("min_total_price"):
                price    = float(h["min_total_price"]) / max(days, 1)
                currency = "INR"

            if not price or price <= 0:
                continue

            # Convert to INR
            conversion = {
                "USD": 83, "EUR": 90, "GBP": 105, "AED": 23,
                "SGD": 62, "THB": 2.4, "IDR": 0.0053,
                "MYR": 18, "LKR": 0.26, "NPR": 0.63,
            }
            if currency != "INR":
                rate      = conversion.get(currency, 83)
                price_inr = int(price * rate)
            else:
                price_inr = int(price)

            # Sanity: if still suspiciously low, assume USD
            if price_inr < 500:
                price_inr = int(price * 83)

            hotels.append({
                "name":            h.get("hotel_name", "Unknown Hotel"),
                "price_per_night": price_inr,
                "rating":          h.get("review_score", "N/A"),
                "review":          h.get("review_score_word", ""),
                "image":           h.get("main_photo_url", ""),
                "address":         h.get("address", ""),
                "distance":        h.get("distance_to_cc", "N/A"),
                "url":             h.get("url", "#"),
            })

        if not hotels:
            return []

        hotels.sort(key=lambda x: x["price_per_night"])

        budget_upper = max(budget_max, 5000)
        filtered = [h for h in hotels if h["price_per_night"] <= budget_upper]

        return filtered[:8] if filtered else hotels[:5]

    except Exception as e:
        print(f"Hotel error: {e}")
        import traceback
        traceback.print_exc()
        return []


def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places, traveler_type):
    names = [p["title"] for p in route_places]
    traveler_clean = traveler_type.split(" ", 1)[1] if " " in traveler_type else traveler_type

    prompt = f"""
    Create a complete personalized travel plan:

    From: {source}
    To: {destination}
    Days: {days}
    Budget: Rs.{budget_min} to Rs.{budget_max}
    Travel Mode: {travel_mode}
    Traveling As: {traveler_clean}

    Personalization rules based on traveler type:
    - Couple: romantic restaurants, sunset spots, couples activities, privacy-focused hotels
    - Family with Kids: kid-friendly activities, safe areas, family rooms, theme parks, beaches
    - Friends Group: nightlife, adventure sports, group activities, budget stays, street food
    - Solo Traveler: safety tips, solo-friendly hostels, self-guided tours, local experiences
    - Business Traveler: business hotels, fast transport, work-friendly cafes, short itinerary
    - Senior Citizens: comfortable transport, relaxed pace, accessible attractions, good hospitals nearby
    - Backpacker: budget stays, local transport, cheap eats, hidden gems, off-beat places

    Include:
    - Personalized route journey plan for {traveler_clean}
    - Places between route: {', '.join(names)}
    - Day-wise itinerary tailored for {traveler_clean}
    - Budget breakdown (transport + hotel + food)
    - Specific travel tips for {traveler_clean}
    - Recommended accommodation type for {traveler_clean}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────

st.set_page_config(page_title="Voyagr — AI Travel Planner", page_icon="✈️", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
#MainMenu,header,footer,.stDeployButton,[data-testid="stToolbar"]{visibility:hidden!important;display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}

:root{
  --cream:#FAF8F5; --ink:#1A1714; --ink-soft:#5A5550;
  --accent:#C4622D; --accent-lt:#F5EDE6; --gold:#C9A84C;
  --border:#E8E4DE; --white:#FFFFFF;
  --shadow:0 2px 24px rgba(26,23,20,0.08);
  --shadow-lg:0 8px 40px rgba(26,23,20,0.14);
  --ff-head:'Playfair Display',Georgia,serif;
  --ff-body:'DM Sans',system-ui,sans-serif;
}

html,body,[class*="css"],.stApp{
  font-family:var(--ff-body)!important;
  background:var(--cream)!important;
  color:var(--ink)!important;
}
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:var(--cream);}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:99px;}

.v-nav{
  position:fixed;top:0;left:0;right:0;z-index:9999;
  background:rgba(255,255,255,0.96);
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  border-bottom:1px solid var(--border);
  height:64px;display:flex;align-items:center;
  justify-content:space-between;padding:0 48px;
  box-shadow:0 1px 0 var(--border),0 4px 16px rgba(26,23,20,0.04);
}
.v-logo{font-family:var(--ff-head);font-size:22px;font-weight:700;color:var(--ink);letter-spacing:-0.5px;display:flex;align-items:center;gap:8px;}
.v-logo span{color:var(--accent);font-family:var(--ff-head);}
.v-nav-links{display:flex;gap:36px;font-size:13.5px;font-weight:500;color:var(--ink-soft);align-items:center;}
.v-nav-links a{color:var(--ink-soft);text-decoration:none;transition:color 0.2s;}
.v-nav-links a:hover{color:var(--accent);}
.v-nav-cta{background:var(--ink);color:var(--white)!important;padding:9px 22px;border-radius:99px;font-size:13px;font-weight:500;text-decoration:none;transition:background 0.2s;}
.v-nav-cta:hover{background:var(--accent)!important;}
.v-spacer{height:64px;}

.v-hero{position:relative;height:560px;overflow:hidden;background:#1A1714;}
.v-slide{position:absolute;inset:0;background-size:cover;background-position:center 40%;opacity:0;transition:opacity 1.2s ease-in-out;}
.v-s1{background-image:url('https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1600&q=80');animation:fade4 20s 0s infinite;}
.v-s2{background-image:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&q=80');animation:fade4 20s 5s infinite;}
.v-s3{background-image:url('https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1600&q=80');animation:fade4 20s 10s infinite;}
.v-s4{background-image:url('https://images.unsplash.com/photo-1548013146-72479768bada?w=1600&q=80');animation:fade4 20s 15s infinite;}
@keyframes fade4{0%{opacity:0;}5%{opacity:1;}25%{opacity:1;}30%{opacity:0;}100%{opacity:0;}}

.v-hero-overlay{position:absolute;inset:0;z-index:2;background:linear-gradient(to top,rgba(26,23,20,0.88) 0%,rgba(26,23,20,0.45) 45%,rgba(26,23,20,0.10) 100%);}
.v-hero-text{position:absolute;bottom:0;left:0;right:0;z-index:3;padding:0 56px 56px;pointer-events:none;}
.v-hero-tag{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,0.13);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.26);color:white;font-size:11.5px;font-weight:500;letter-spacing:1.4px;text-transform:uppercase;padding:7px 16px;border-radius:99px;margin-bottom:18px;}
.v-hero-tag::before{content:"";width:7px;height:7px;background:#4ade80;border-radius:50%;animation:blink 2s infinite;}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.4;}}
.v-hero-text h1{font-family:var(--ff-head);font-size:54px;font-weight:700;color:white;line-height:1.08;letter-spacing:-1.5px;margin-bottom:14px;text-shadow:0 2px 20px rgba(0,0,0,.3);}
.v-hero-text h1 em{font-style:italic;color:var(--gold);}
.v-hero-text p{font-size:16px;color:rgba(255,255,255,0.76);font-weight:300;line-height:1.6;max-width:560px;}
.v-dots{position:absolute;bottom:22px;right:48px;z-index:4;display:flex;gap:8px;align-items:center;}
.v-dot{width:8px;height:8px;border-radius:99px;background:rgba(255,255,255,0.35);}
.v-dot.d1{animation:dot1 20s 0s infinite;}.v-dot.d2{animation:dot1 20s 5s infinite;}.v-dot.d3{animation:dot1 20s 10s infinite;}.v-dot.d4{animation:dot1 20s 15s infinite;}
@keyframes dot1{0%,4%{background:white;width:22px;}30%,100%{background:rgba(255,255,255,0.35);width:8px;}}

.v-search-wrap{padding:0 40px;margin-top:-48px;position:relative;z-index:50;}
.v-search-panel{background:var(--white);border-radius:20px;border:1px solid var(--border);box-shadow:var(--shadow-lg);padding:26px 32px 22px;}
.v-search-eyebrow{font-size:16px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase;color:var(--ink-soft);margin-bottom:18px;display:flex;align-items:center;gap:10px;}
.v-search-eyebrow::before{content:'';width:24px;height:2px;background:var(--accent);border-radius:2px;display:inline-block;}
.v-field-label{font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--ink-soft);margin-bottom:6px;display:block;}

div[data-baseweb="input"] input{background:var(--cream)!important;border:1.5px solid var(--border)!important;border-radius:10px!important;font-family:var(--ff-body)!important;font-size:15px!important;color:var(--ink)!important;height:48px!important;padding:0 16px!important;transition:border-color .2s,box-shadow .2s!important;}
div[data-baseweb="input"] input:focus{border-color:var(--accent)!important;background:white!important;box-shadow:0 0 0 3px rgba(196,98,45,0.11)!important;}
div[data-baseweb="select"]>div{background:var(--cream)!important;border:1.5px solid var(--border)!important;border-radius:10px!important;font-family:var(--ff-body)!important;font-size:15px!important;min-height:48px!important;}
div[data-testid="stNumberInput"] input{background:var(--cream)!important;border:1.5px solid var(--border)!important;border-radius:10px!important;font-size:15px!important;height:48px!important;}

div[data-testid="stButton"]>button{background:var(--accent)!important;color:white!important;border:none!important;border-radius:12px!important;font-family:var(--ff-body)!important;font-size:15.5px!important;font-weight:700!important;height:52px!important;letter-spacing:.4px!important;transition:all .2s!important;box-shadow:0 4px 18px rgba(196,98,45,0.32)!important;}
div[data-testid="stButton"]>button:hover{background:#b05527!important;transform:translateY(-1px)!important;box-shadow:0 7px 24px rgba(196,98,45,0.42)!important;}
div[data-testid="stButton"]>button:active{transform:translateY(0)!important;}

div[data-baseweb="tab-list"]{background:var(--cream)!important;border-radius:12px!important;padding:4px!important;gap:2px!important;border:1px solid var(--border)!important;}
button[data-baseweb="tab"]{font-family:var(--ff-body)!important;font-size:13.5px!important;font-weight:500!important;border-radius:9px!important;color:var(--ink-soft)!important;padding:9px 20px!important;transition:all .2s!important;}
button[data-baseweb="tab"][aria-selected="true"]{background:var(--white)!important;color:var(--accent)!important;font-weight:700!important;box-shadow:0 1px 8px rgba(26,23,20,0.08)!important;}
div[data-baseweb="tab-highlight"],div[data-baseweb="tab-border"]{display:none!important;}

.v-section{padding:40px 40px 16px;}
.v-section-head{display:flex;align-items:baseline;gap:12px;margin-bottom:22px;}
.v-section-head h2{font-family:var(--ff-head);font-size:26px;font-weight:600;color:var(--ink);letter-spacing:-0.4px;}
.v-section-head span{font-size:13px;color:var(--ink-soft);}

.v-dest-card{border-radius:14px;overflow:hidden;height:210px;position:relative;cursor:pointer;background-size:cover;background-position:center;transition:transform .3s cubic-bezier(.34,1.56,.64,1);}
.v-dest-card:hover{transform:translateY(-5px);}
.v-dest-gradient{position:absolute;inset:0;background:linear-gradient(to top,rgba(26,23,20,0.76) 0%,transparent 55%);}
.v-dest-info{position:absolute;bottom:0;left:0;right:0;padding:16px;}
.v-dest-name{font-family:var(--ff-head);font-size:18px;font-weight:600;color:white;margin-bottom:2px;}
.v-dest-sub{font-size:11px;color:rgba(255,255,255,0.7);letter-spacing:.4px;}

.v-overview{background:var(--ink);border-radius:16px;padding:20px 28px;margin:0 40px 8px;display:flex;align-items:center;flex-wrap:wrap;}
.v-overview-item{flex:1;min-width:110px;padding:0 20px;border-right:1px solid rgba(255,255,255,0.11);}
.v-overview-item:first-child{padding-left:0;}
.v-overview-item:last-child{border-right:none;}
.v-ov-label{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:rgba(255,255,255,0.42);margin-bottom:4px;}
.v-ov-value{font-size:14.5px;font-weight:500;color:white;}
.v-ov-value.accent{color:var(--gold);}

.v-hotel{background:var(--white);border:1px solid var(--border);border-radius:16px;overflow:hidden;display:flex;margin-bottom:16px;transition:box-shadow .2s,transform .2s;}
.v-hotel:hover{box-shadow:var(--shadow);transform:translateY(-2px);}
.v-hotel-img{width:210px;flex-shrink:0;background-size:cover;background-position:center;min-height:160px;}
.v-hotel-body{padding:22px 26px;flex:1;display:flex;flex-direction:column;justify-content:space-between;}
.v-hotel-name{font-family:var(--ff-head);font-size:20px;font-weight:600;color:var(--ink);margin-bottom:8px;}
.v-hotel-meta{display:flex;align-items:center;gap:14px;margin-bottom:10px;flex-wrap:wrap;}
.v-rating{background:#FFF8EC;color:#92600A;font-size:12px;font-weight:600;padding:4px 10px;border-radius:99px;border:1px solid #F5D98A;}
.v-hotel-addr{font-size:13px;color:var(--ink-soft);margin-bottom:14px;line-height:1.5;}
.v-hotel-footer{display:flex;align-items:center;justify-content:space-between;border-top:1px solid var(--border);padding-top:14px;margin-top:4px;}
.v-price{font-size:22px;font-weight:700;color:var(--accent);}
.v-price small{font-size:13px;font-weight:400;color:var(--ink-soft);}
.v-book-btn{background:var(--ink);color:white;font-size:13px;font-weight:600;padding:10px 22px;border-radius:99px;text-decoration:none;transition:background .2s;}
.v-book-btn:hover{background:var(--accent);color:white;}

.v-plan-line{padding:11px 18px;border-left:3px solid var(--accent);border-radius:0 10px 10px 0;background:#F5EDE6;margin-bottom:9px;font-size:14px;color:var(--ink);line-height:1.6;}
.v-day-header{background:var(--ink);color:white;padding:10px 18px;border-radius:9px;font-size:12.5px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin:18px 0 10px;}

.v-links-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:18px;}
.v-link-card{background:var(--white);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center;text-decoration:none;color:var(--ink);font-size:13px;font-weight:500;transition:all .2s;display:block;}
.v-link-card:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-2px);box-shadow:0 4px 14px rgba(196,98,45,0.12);}
.v-link-icon{font-size:22px;margin-bottom:6px;}

.v-metric{background:var(--white);border:1px solid var(--border);border-radius:14px;padding:20px;text-align:center;}
.v-metric-label{font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--ink-soft);margin-bottom:8px;}
.v-metric-value{font-family:var(--ff-head);font-size:24px;font-weight:600;color:var(--ink);}

.v-place-card{background:var(--white);border:1px solid var(--border);border-radius:14px;overflow:hidden;margin-bottom:14px;transition:box-shadow .2s;}
.v-place-card:hover{box-shadow:var(--shadow);}
.v-place-img{width:100%;height:160px;background-size:cover;background-position:center;}
.v-place-info{padding:14px 16px;}
.v-place-name{font-weight:600;font-size:15px;color:var(--ink);margin-bottom:4px;}
.v-place-addr{font-size:12px;color:var(--ink-soft);line-height:1.4;}

.v-divider{height:1px;background:var(--border);margin:8px 0 20px;}
.stSpinner>div{border-top-color:var(--accent)!important;}
div[data-testid="stSuccess"]{background:#F0FAF4!important;border:1px solid #86EFAC!important;border-radius:12px!important;border-left:4px solid #22C55E!important;}
div[data-testid="stWarning"]{border-radius:12px!important;border-left:4px solid #F59E0B!important;}

.v-footer{background:var(--ink);color:rgba(255,255,255,0.45);text-align:center;padding:28px;font-size:13px;margin-top:64px;}
.v-footer strong{color:rgba(255,255,255,0.8);font-weight:500;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────

st.markdown("""
<div class="v-nav">
  <div class="v-logo">✈ Voyag<span>r</span></div>
  <div class="v-nav-links">
    <a href="#">Explore</a>
    <a href="#">Hotels</a>
    <a href="#">Flights</a>
    <a href="#">Packages</a>
    <a href="#" class="v-nav-cta">Sign in</a>
  </div>
</div>
<div class="v-spacer"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HERO
# ─────────────────────────────────────────

st.markdown("""
<div class="v-hero">
  <div class="v-slide v-s1"></div>
  <div class="v-slide v-s2"></div>
  <div class="v-slide v-s3"></div>
  <div class="v-slide v-s4"></div>
  <div class="v-hero-overlay"></div>
  <div class="v-hero-text">
    <div class="v-hero-tag">AI-Powered Travel Planning</div>
    <h1>Your next <em>adventure</em>,<br>perfectly planned.</h1>
    <p>From itinerary to hotels — Voyagr builds your dream trip in seconds using AI.</p>
  </div>
  <div class="v-dots">
    <div class="v-dot d1"></div>
    <div class="v-dot d2"></div>
    <div class="v-dot d3"></div>
    <div class="v-dot d4"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SEARCH PANEL
# ─────────────────────────────────────────

st.markdown("<div class='v-search-wrap'><div class='v-search-panel'>", unsafe_allow_html=True)
st.markdown("<div class='v-search-eyebrow'>Plan your trip</div>", unsafe_allow_html=True)

row1_c1, row1_c2 = st.columns(2)
with row1_c1:
    st.markdown("<span class='v-field-label'>📍 From</span>", unsafe_allow_html=True)
    source = st.text_input("From", placeholder="Enter origin city (e.g. Indore)", label_visibility="collapsed")
with row1_c2:
    st.markdown("<span class='v-field-label'>🏁 To</span>", unsafe_allow_html=True)
    destination = st.text_input("To", placeholder="e.g. Goa, Manali, Jaipur, Delhi", label_visibility="collapsed")

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

row2_c1, row2_c2, row2_c3, row2_c4, row2_c5 = st.columns([1, 1.2, 1.2, 1.2, 1.4])

with row2_c1:
    st.markdown("<span class='v-field-label'>📅 Days</span>", unsafe_allow_html=True)
    days = st.number_input("Days", min_value=1, max_value=15, value=3, label_visibility="collapsed")

with row2_c2:
    st.markdown("<span class='v-field-label'>💰 Min Budget (₹)</span>", unsafe_allow_html=True)
    budget_min = st.number_input("Min Budget", min_value=0, value=5000, step=1000, label_visibility="collapsed")

with row2_c3:
    st.markdown("<span class='v-field-label'>💰 Max Budget (₹)</span>", unsafe_allow_html=True)
    budget_max = st.number_input("Max Budget", min_value=0, value=20000, step=1000, label_visibility="collapsed")

with row2_c4:
    st.markdown("<span class='v-field-label'>🚆 Travel Mode</span>", unsafe_allow_html=True)
    travel_mode = st.selectbox("Mode", ["🚗 Car", "✈️ Flight", "🚆 Train", "🚌 Bus"], label_visibility="collapsed")

with row2_c5:
    st.markdown("<span class='v-field-label'>👥 Traveling As</span>", unsafe_allow_html=True)
    traveler_type = st.selectbox(
        "Traveler Type",
        ["👫 Couple", "👨‍👩‍👧‍👦 Family with Kids", "👯 Friends Group",
         "🧳 Solo Traveler", "💼 Business Traveler", "🧓 Senior Citizens", "🎒 Backpacker"],
        label_visibility="collapsed"
    )

if budget_min > budget_max:
    st.warning("⚠️ Minimum budget cannot exceed maximum budget.")

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
generate = st.button("✦  Generate My Trip Plan", use_container_width=True)
st.markdown("</div></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# POPULAR DESTINATIONS
# ─────────────────────────────────────────

st.markdown("""
<div class="v-section">
  <div class="v-section-head">
    <h2>Popular Destinations</h2>
    <span>Trending in India</span>
  </div>
</div>
""", unsafe_allow_html=True)

dest_data = [
    ("Goa",    "Sun, Sea & Serenity",   "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80"),
    ("Manali", "Mountains & Adventure", "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=600&q=80"),
    ("Jaipur", "Royal Heritage",        "https://images.unsplash.com/photo-1548013146-72479768bada?w=600&q=80"),
    ("Kerala", "Backwaters & Spice",    "https://images.unsplash.com/photo-1593693411515-c20261bcad6e?w=600&q=80"),
]

dcols = st.columns(4, gap="medium")
for i, (name, sub, img) in enumerate(dest_data):
    with dcols[i]:
        st.markdown(f"""
        <div class="v-dest-card" style="background-image:url('{img}');">
          <div class="v-dest-gradient"></div>
          <div class="v-dest-info">
            <div class="v-dest-name">{name}</div>
            <div class="v-dest-sub">{sub}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────

if generate and source and destination:

    with st.spinner("Building your perfect trip plan..."):
        route_places = get_route_places(source, destination)
        hotels       = get_hotels(destination, days, budget_max)
        plan         = generate_plan(source, destination, days, budget_min, budget_max,
                                     travel_mode, route_places, traveler_type)

    st.success(f"✓  Your trip from {source} to {destination} is ready!")

    mode_clean = travel_mode.replace("🚗 ","").replace("✈️ ","").replace("🚆 ","").replace("🚌 ","")

    st.markdown(f"""
    <div class="v-overview">
      <div class="v-overview-item"><div class="v-ov-label">Journey</div><div class="v-ov-value accent">{source} → {destination}</div></div>
      <div class="v-overview-item"><div class="v-ov-label">Duration</div><div class="v-ov-value">{days} Days</div></div>
      <div class="v-overview-item"><div class="v-ov-label">Budget</div><div class="v-ov-value">₹{budget_min:,} – ₹{budget_max:,}</div></div>
      <div class="v-overview-item"><div class="v-ov-label">Travel Mode</div><div class="v-ov-value">{mode_clean}</div></div>
      <div class="v-overview-item"><div class="v-ov-label">Traveling As</div><div class="v-ov-value">{traveler_type}</div></div>
      <div class="v-overview-item"><div class="v-ov-label">Hotels Found</div><div class="v-ov-value">{len(hotels)} options</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding:20px 40px 0;'>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["  🗺️  Itinerary  ", "  🛣️  Route Places  ", "  🏨  Hotels  ", "  📊  Summary  "]
    )

    # ── ITINERARY ──
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Day-wise Itinerary")
        st.markdown("<div class='v-divider'></div>", unsafe_allow_html=True)
        for line in plan.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.lower().startswith("day") or line.startswith("##"):
                st.markdown(f"<div class='v-day-header'>{line.replace('##','').replace('**','').strip()}</div>", unsafe_allow_html=True)
            else:
                clean = line.lstrip("*-•").strip()
                if clean:
                    st.markdown(f"<div class='v-plan-line'>{clean}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Quick Booking")
        st.markdown("<div class='v-divider'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="v-links-grid">
          <a href="https://www.makemytrip.com" target="_blank" class="v-link-card"><div class="v-link-icon">🛏️</div>MakeMyTrip</a>
          <a href="https://www.irctc.co.in"    target="_blank" class="v-link-card"><div class="v-link-icon">🚆</div>IRCTC</a>
          <a href="https://www.redbus.in"      target="_blank" class="v-link-card"><div class="v-link-icon">🚌</div>RedBus</a>
          <a href="https://www.goibibo.com"    target="_blank" class="v-link-card"><div class="v-link-icon">✈️</div>Goibibo</a>
        </div>
        """, unsafe_allow_html=True)

    # ── ROUTE PLACES ──
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Attractions Along Your Route")
        st.markdown("<div class='v-divider'></div>", unsafe_allow_html=True)
        if not route_places:
            st.warning("No route places found for this journey.")
        else:
            cols = st.columns(2, gap="medium")
            for i, p in enumerate(route_places):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="v-place-card">
                      <div class="v-place-img" style="background-image:url('{p['image']}');"></div>
                      <div class="v-place-info">
                        <div class="v-place-name">📍 {p['title']}</div>
                        <div class="v-place-addr">{p['address']}</div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── HOTELS ──
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Available Hotels")
        st.markdown("<div class='v-divider'></div>", unsafe_allow_html=True)
        if not hotels:
            st.warning("No hotels found. Try increasing your max budget or check your RapidAPI key.")
        else:
            for h in hotels:
                price = h.get("price_per_night", 0)
                try:
                    pf = f"₹{int(price):,}"
                except Exception:
                    pf = f"₹{price}"

                img_url = h.get("image", "")
                if img_url:
                    img_html = f'<div class="v-hotel-img" style="background-image:url(\'{img_url}\');"></div>'
                else:
                    img_html = '<div class="v-hotel-img" style="background:#f0ede8;display:flex;align-items:center;justify-content:center;font-size:36px;">🏨</div>'

                st.markdown(f"""
                <div class="v-hotel">
                  {img_html}
                  <div class="v-hotel-body">
                    <div>
                      <div class="v-hotel-name">{h.get('name','Hotel')}</div>
                      <div class="v-hotel-meta">
                        <span class="v-rating">⭐ {h.get('rating','N/A')} / 10 — {h.get('review','')}</span>
                        <span style="font-size:12px;color:#888;">📏 {h.get('distance','N/A')} from centre</span>
                      </div>
                      <div class="v-hotel-addr">📍 {h.get('address','N/A')}</div>
                    </div>
                    <div class="v-hotel-footer">
                      <div class="v-price">{pf} <small>/ night</small></div>
                      <a href="{h.get('url','#')}" target="_blank" class="v-book-btn">Book Now →</a>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── SUMMARY ──
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Trip Summary")
        st.markdown("<div class='v-divider'></div>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4, gap="medium")
        for col, (lbl, val) in zip([m1, m2, m3, m4], [
            ("Origin", source), ("Destination", destination),
            ("Duration", f"{days} days"), ("Max Budget", f"₹{budget_max:,}")
        ]):
            with col:
                st.markdown(f'<div class="v-metric"><div class="v-metric-label">{lbl}</div><div class="v-metric-value">{val}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "Detail": ["From", "To", "Duration", "Budget Range", "Travel Mode", "Traveling As", "Hotels Found", "Attractions"],
            "Value":  [source, destination, f"{days} days",
                       f"₹{budget_min:,} – ₹{budget_max:,}", travel_mode,
                       traveler_type, str(len(hotels)), str(len(route_places))]
        }), use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────

st.markdown("""
<div class="v-footer">
  <strong>Voyagr</strong> — AI Travel Planner &nbsp;·&nbsp;
  Built with Gemini AI &nbsp;·&nbsp;
  Hotel data via Booking.com &nbsp;·&nbsp;
  Maps by Geoapify<br><br>
  © 2026 Voyagr · All rights reserved
</div>
""", unsafe_allow_html=True)

# =================================================================================================================
# ===================================================================================================================
# import os
# import streamlit as st
# from dotenv import load_dotenv
# from google import genai
# from tavily import TavilyClient
# import requests
# from datetime import datetime, timedelta
# import pandas as pd

# load_dotenv()

# GOOGLE_API_KEY   = os.getenv("GOOGLE_API_KEY")
# TAVILY_API_KEY   = os.getenv("TAVILY_API_KEY")
# RAPIDAPI_KEY     = os.getenv("RAPIDAPI_KEY")
# GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

# # ── Make.com webhook URL for the AI bot ──
# MAKE_WEBHOOK_URL = "https://hook.us2.make.com/wbxbj9bmg13b89b1irrugvbfwg7runx6"

# client = genai.Client(api_key=GOOGLE_API_KEY)
# tavily = TavilyClient(api_key=TAVILY_API_KEY)

# headers = {
#     "X-RapidAPI-Key": RAPIDAPI_KEY,
#     "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
# }

# # ─────────────────────────────────────────
# # FUNCTIONS
# # ─────────────────────────────────────────

# def get_destination_id(city):
#     try:
#         search_query = f"{city} India"
#         res = requests.get(
#             "https://booking-com.p.rapidapi.com/v1/hotels/locations",
#             headers=headers,
#             params={"name": search_query, "locale": "en-gb"},
#             timeout=10
#         )
#         if res.status_code != 200:
#             return None, None

#         data = res.json()
#         if not data:
#             return None, None

#         city_lower = city.lower()
#         for item in data:
#             label   = item.get("label", "").lower()
#             country = item.get("country", "").lower()
#             if city_lower in label and ("india" in label or "india" in country):
#                 return item["dest_id"], item["dest_type"]

#         return data[0]["dest_id"], data[0]["dest_type"]

#     except Exception as e:
#         print("Destination error:", e)
#         return None, None


# def get_route_places(source, destination):
#     try:
#         geo_url = "https://api.geoapify.com/v1/geocode/search"

#         def get_coords(city):
#             res = requests.get(geo_url, params={"text": city, "apiKey": GEOAPIFY_API_KEY}).json()
#             if not res.get("features"):
#                 return None
#             p = res["features"][0]["properties"]
#             return p["lon"], p["lat"]

#         start = get_coords(source)
#         end   = get_coords(destination)
#         if not start or not end:
#             return []

#         rr = requests.get("https://api.geoapify.com/v1/routing", params={
#             "waypoints": f"{start[1]},{start[0]}|{end[1]},{end[0]}",
#             "mode": "drive", "apiKey": GEOAPIFY_API_KEY
#         }).json()

#         if "features" not in rr:
#             return []

#         coords = rr["features"][0]["geometry"]["coordinates"]
#         if isinstance(coords[0][0], list):
#             coords = coords[0]

#         step = max(1, len(coords) // 6)
#         places, seen = [], set()

#         for lon, lat in coords[::step]:
#             res = requests.get("https://api.geoapify.com/v2/places", params={
#                 "categories": "tourism.sights,tourism.attraction",
#                 "filter": f"circle:{lon},{lat},4000",
#                 "limit": 2,
#                 "apiKey": GEOAPIFY_API_KEY
#             }).json()
#             for item in res.get("features", []):
#                 prop = item["properties"]
#                 name = prop.get("name", "Place")
#                 if name in seen:
#                     continue
#                 seen.add(name)
#                 places.append({
#                     "title":   name,
#                     "address": prop.get("formatted", ""),
#                     "image":   f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=400&height=300&center=lonlat:{prop.get('lon')},{prop.get('lat')}&zoom=14&apiKey={GEOAPIFY_API_KEY}"
#                 })

#         return places[:10]

#     except Exception as e:
#         print("Route places error:", e)
#         return []


# def get_hotels(destination, days, budget_max):
#     try:
#         dest_id, dest_type = get_destination_id(destination)
#         if not dest_id:
#             return []

#         today    = datetime.today()
#         checkin  = today + timedelta(days=1)
#         checkout = checkin + timedelta(days=max(days, 1))

#         res = requests.get(
#             "https://booking-com.p.rapidapi.com/v1/hotels/search",
#             headers=headers,
#             params={
#                 "dest_id":            dest_id,
#                 "dest_type":          dest_type,
#                 "checkin_date":       checkin.strftime("%Y-%m-%d"),
#                 "checkout_date":      checkout.strftime("%Y-%m-%d"),
#                 "adults_number":      2,
#                 "room_number":        1,
#                 "order_by":           "popularity",
#                 "locale":             "en-gb",
#                 "units":              "metric",
#                 "filter_by_currency": "INR",
#                 "currency":           "INR",
#             },
#             timeout=20
#         )

#         if res.status_code != 200:
#             print(f"Hotel API error: {res.status_code}")
#             return []

#         results = res.json().get("result", [])
#         if not results:
#             return []

#         hotels = []

#         for h in results[:30]:
#             price    = None
#             currency = "INR"

#             cpb = h.get("composite_price_breakdown", {})
#             if cpb:
#                 gpn = cpb.get("gross_amount_per_night", {})
#                 if gpn.get("value"):
#                     price    = float(gpn["value"])
#                     currency = gpn.get("currency", "INR")
#                 else:
#                     ga = cpb.get("gross_amount", {})
#                     if ga.get("value"):
#                         price    = float(ga["value"]) / max(days, 1)
#                         currency = ga.get("currency", "INR")

#             if not price:
#                 pb = h.get("price_breakdown", {})
#                 if pb.get("gross_price"):
#                     price    = float(pb["gross_price"]) / max(days, 1)
#                     currency = pb.get("currency", "INR")

#             if not price and h.get("min_total_price"):
#                 price    = float(h["min_total_price"]) / max(days, 1)
#                 currency = "INR"

#             if not price or price <= 0:
#                 continue

#             conversion = {
#                 "USD": 83, "EUR": 90, "GBP": 105, "AED": 23,
#                 "SGD": 62, "THB": 2.4, "IDR": 0.0053,
#                 "MYR": 18, "LKR": 0.26, "NPR": 0.63,
#             }
#             if currency != "INR":
#                 rate      = conversion.get(currency, 83)
#                 price_inr = int(price * rate)
#             else:
#                 price_inr = int(price)

#             if price_inr < 500:
#                 price_inr = int(price * 83)

#             hotels.append({
#                 "name":            h.get("hotel_name", "Unknown Hotel"),
#                 "price_per_night": price_inr,
#                 "rating":          h.get("review_score", "N/A"),
#                 "review":          h.get("review_score_word", ""),
#                 "image":           h.get("main_photo_url", ""),
#                 "address":         h.get("address", ""),
#                 "distance":        h.get("distance_to_cc", "N/A"),
#                 "url":             h.get("url", "#"),
#             })

#         if not hotels:
#             return []

#         hotels.sort(key=lambda x: x["price_per_night"])

#         budget_upper = max(budget_max, 5000)
#         filtered = [h for h in hotels if h["price_per_night"] <= budget_upper]

#         return filtered[:8] if filtered else hotels[:5]

#     except Exception as e:
#         print(f"Hotel error: {e}")
#         import traceback
#         traceback.print_exc()
#         return []


# def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places, traveler_type):
#     names = [p["title"] for p in route_places]
#     traveler_clean = traveler_type.split(" ", 1)[1] if " " in traveler_type else traveler_type

#     prompt = f"""
#     Create a complete personalized travel plan:

#     From: {source}
#     To: {destination}
#     Days: {days}
#     Budget: Rs.{budget_min} to Rs.{budget_max}
#     Travel Mode: {travel_mode}
#     Traveling As: {traveler_clean}

#     Personalization rules based on traveler type:
#     - Couple: romantic restaurants, sunset spots, couples activities, privacy-focused hotels
#     - Family with Kids: kid-friendly activities, safe areas, family rooms, theme parks, beaches
#     - Friends Group: nightlife, adventure sports, group activities, budget stays, street food
#     - Solo Traveler: safety tips, solo-friendly hostels, self-guided tours, local experiences
#     - Business Traveler: business hotels, fast transport, work-friendly cafes, short itinerary
#     - Senior Citizens: comfortable transport, relaxed pace, accessible attractions, good hospitals nearby
#     - Backpacker: budget stays, local transport, cheap eats, hidden gems, off-beat places

#     Include:
#     - Personalized route journey plan for {traveler_clean}
#     - Places between route: {', '.join(names)}
#     - Day-wise itinerary tailored for {traveler_clean}
#     - Budget breakdown (transport + hotel + food)
#     - Specific travel tips for {traveler_clean}
#     - Recommended accommodation type for {traveler_clean}
#     """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )
#     return response.text


# def ask_bot(message):
#     """Send a message to the make.com webhook and return the bot reply."""
#     try:
#         response = requests.post(
#             MAKE_WEBHOOK_URL,
#             json={"message": message},
#             timeout=30
#         )
#         response.raise_for_status()
#         # Try JSON first ({"response":...} or {"message":...} or {"reply":...})
#         try:
#             data = response.json()
#             return (
#                 data.get("response")
#                 or data.get("message")
#                 or data.get("reply")
#                 or str(data)
#             )
#         except Exception:
#             return response.text
#     except requests.exceptions.Timeout:
#         return "⏱️ The bot is taking too long to respond. Please try again."
#     except requests.exceptions.ConnectionError:
#         return "🔌 Could not connect to the bot. Check your make.com webhook URL."
#     except Exception as e:
#         return f"❌ Error: {e}"


# # ─────────────────────────────────────────
# # PAGE CONFIG
# # ─────────────────────────────────────────

# st.set_page_config(page_title="Voyagr — AI Travel Planner", page_icon="✈️", layout="wide")

# st.markdown("""
# <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">

# <style>
# *,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
# #MainMenu,header,footer,.stDeployButton,[data-testid="stToolbar"]{visibility:hidden!important;display:none!important;}
# .block-container{padding:0!important;max-width:100%!important;}

# :root{
#   --cream:#FAF8F5; --ink:#1A1714; --ink-soft:#5A5550;
#   --accent:#C4622D; --accent-lt:#F5EDE6; --gold:#C9A84C;
#   --border:#E8E4DE; --white:#FFFFFF;
#   --shadow:0 2px 24px rgba(26,23,20,0.08);
#   --shadow-lg:0 8px 40px rgba(26,23,20,0.14);
#   --ff-head:'Playfair Display',Georgia,serif;
#   --ff-body:'DM Sans',system-ui,sans-serif;
# }

# html,body,[class*="css"],.stApp{
#   font-family:var(--ff-body)!important;
#   background:var(--cream)!important;
#   color:var(--ink)!important;
# }
# ::-webkit-scrollbar{width:5px;}
# ::-webkit-scrollbar-track{background:var(--cream);}
# ::-webkit-scrollbar-thumb{background:var(--border);border-radius:99px;}

# .v-nav{
#   position:fixed;top:0;left:0;right:0;z-index:9999;
#   background:rgba(255,255,255,0.96);
#   backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
#   border-bottom:1px solid var(--border);
#   height:64px;display:flex;align-items:center;
#   justify-content:space-between;padding:0 48px;
#   box-shadow:0 1px 0 var(--border),0 4px 16px rgba(26,23,20,0.04);
# }
# .v-logo{font-family:var(--ff-head);font-size:22px;font-weight:700;color:var(--ink);letter-spacing:-0.5px;display:flex;align-items:center;gap:8px;}
# .v-logo span{color:var(--accent);font-family:var(--ff-head);}
# .v-nav-links{display:flex;gap:36px;font-size:13.5px;font-weight:500;color:var(--ink-soft);align-items:center;}
# .v-nav-links a{color:var(--ink-soft);text-decoration:none;transition:color 0.2s;}
# .v-nav-links a:hover{color:var(--accent);}
# .v-nav-cta{background:var(--ink);color:var(--white)!important;padding:9px 22px;border-radius:99px;font-size:13px;font-weight:500;text-decoration:none;transition:background 0.2s;}
# .v-nav-cta:hover{background:var(--accent)!important;}
# .v-spacer{height:64px;}

# .v-hero{position:relative;height:560px;overflow:hidden;background:#1A1714;}
# .v-slide{position:absolute;inset:0;background-size:cover;background-position:center 40%;opacity:0;transition:opacity 1.2s ease-in-out;}
# .v-s1{background-image:url('https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1600&q=80');animation:fade4 20s 0s infinite;}
# .v-s2{background-image:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&q=80');animation:fade4 20s 5s infinite;}
# .v-s3{background-image:url('https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1600&q=80');animation:fade4 20s 10s infinite;}
# .v-s4{background-image:url('https://images.unsplash.com/photo-1548013146-72479768bada?w=1600&q=80');animation:fade4 20s 15s infinite;}
# @keyframes fade4{0%{opacity:0;}5%{opacity:1;}25%{opacity:1;}30%{opacity:0;}100%{opacity:0;}}

# .v-hero-overlay{position:absolute;inset:0;z-index:2;background:linear-gradient(to top,rgba(26,23,20,0.88) 0%,rgba(26,23,20,0.45) 45%,rgba(26,23,20,0.10) 100%);}
# .v-hero-text{position:absolute;bottom:0;left:0;right:0;z-index:3;padding:0 56px 56px;pointer-events:none;}
# .v-hero-tag{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,0.13);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.26);color:white;font-size:11.5px;font-weight:500;letter-spacing:1.4px;text-transform:uppercase;padding:7px 16px;border-radius:99px;margin-bottom:18px;}
# .v-hero-tag::before{content:"";width:7px;height:7px;background:#4ade80;border-radius:50%;animation:blink 2s infinite;}
# @keyframes blink{0%,100%{opacity:1;}50%{opacity:.4;}}
# .v-hero-text h1{font-family:var(--ff-head);font-size:54px;font-weight:700;color:white;line-height:1.08;letter-spacing:-1.5px;margin-bottom:14px;text-shadow:0 2px 20px rgba(0,0,0,.3);}
# .v-hero-text h1 em{font-style:italic;color:var(--gold);}
# .v-hero-text p{font-size:16px;color:rgba(255,255,255,0.76);font-weight:300;line-height:1.6;max-width:560px;}
# .v-dots{position:absolute;bottom:22px;right:48px;z-index:4;display:flex;gap:8px;align-items:center;}
# .v-dot{width:8px;height:8px;border-radius:99px;background:rgba(255,255,255,0.35);}
# .v-dot.d1{animation:dot1 20s 0s infinite;}.v-dot.d2{animation:dot1 20s 5s infinite;}.v-dot.d3{animation:dot1 20s 10s infinite;}.v-dot.d4{animation:dot1 20s 15s infinite;}
# @keyframes dot1{0%,4%{background:white;width:22px;}30%,100%{background:rgba(255,255,255,0.35);width:8px;}}

# .v-search-wrap{padding:0 40px;margin-top:-48px;position:relative;z-index:50;}
# .v-search-panel{background:var(--white);border-radius:20px;border:1px solid var(--border);box-shadow:var(--shadow-lg);padding:26px 32px 22px;}
# .v-search-eyebrow{font-size:16px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase;color:var(--ink-soft);margin-bottom:18px;display:flex;align-items:center;gap:10px;}
# .v-search-eyebrow::before{content:'';width:24px;height:2px;background:var(--accent);border-radius:2px;display:inline-block;}
# .v-field-label{font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--ink-soft);margin-bottom:6px;display:block;}

# div[data-baseweb="input"] input{background:var(--cream)!important;border:1.5px solid var(--border)!important;border-radius:10px!important;font-family:var(--ff-body)!important;font-size:15px!important;color:var(--ink)!important;height:48px!important;padding:0 16px!important;transition:border-color .2s,box-shadow .2s!important;}
# div[data-baseweb="input"] input:focus{border-color:var(--accent)!important;background:white!important;box-shadow:0 0 0 3px rgba(196,98,45,0.11)!important;}
# div[data-baseweb="select"]>div{background:var(--cream)!important;border:1.5px solid var(--border)!important;border-radius:10px!important;font-family:var(--ff-body)!important;font-size:15px!important;min-height:48px!important;}
# div[data-testid="stNumberInput"] input{background:var(--cream)!important;border:1.5px solid var(--border)!important;border-radius:10px!important;font-size:15px!important;height:48px!important;}

# div[data-testid="stButton"]>button{background:var(--accent)!important;color:white!important;border:none!important;border-radius:12px!important;font-family:var(--ff-body)!important;font-size:15.5px!important;font-weight:700!important;height:52px!important;letter-spacing:.4px!important;transition:all .2s!important;box-shadow:0 4px 18px rgba(196,98,45,0.32)!important;}
# div[data-testid="stButton"]>button:hover{background:#b05527!important;transform:translateY(-1px)!important;box-shadow:0 7px 24px rgba(196,98,45,0.42)!important;}
# div[data-testid="stButton"]>button:active{transform:translateY(0)!important;}

# div[data-baseweb="tab-list"]{background:var(--cream)!important;border-radius:12px!important;padding:4px!important;gap:2px!important;border:1px solid var(--border)!important;}
# button[data-baseweb="tab"]{font-family:var(--ff-body)!important;font-size:13.5px!important;font-weight:500!important;border-radius:9px!important;color:var(--ink-soft)!important;padding:9px 20px!important;transition:all .2s!important;}
# button[data-baseweb="tab"][aria-selected="true"]{background:var(--white)!important;color:var(--accent)!important;font-weight:700!important;box-shadow:0 1px 8px rgba(26,23,20,0.08)!important;}
# div[data-baseweb="tab-highlight"],div[data-baseweb="tab-border"]{display:none!important;}

# .v-section{padding:40px 40px 16px;}
# .v-section-head{display:flex;align-items:baseline;gap:12px;margin-bottom:22px;}
# .v-section-head h2{font-family:var(--ff-head);font-size:26px;font-weight:600;color:var(--ink);letter-spacing:-0.4px;}
# .v-section-head span{font-size:13px;color:var(--ink-soft);}

# .v-dest-card{border-radius:14px;overflow:hidden;height:210px;position:relative;cursor:pointer;background-size:cover;background-position:center;transition:transform .3s cubic-bezier(.34,1.56,.64,1);}
# .v-dest-card:hover{transform:translateY(-5px);}
# .v-dest-gradient{position:absolute;inset:0;background:linear-gradient(to top,rgba(26,23,20,0.76) 0%,transparent 55%);}
# .v-dest-info{position:absolute;bottom:0;left:0;right:0;padding:16px;}
# .v-dest-name{font-family:var(--ff-head);font-size:18px;font-weight:600;color:white;margin-bottom:2px;}
# .v-dest-sub{font-size:11px;color:rgba(255,255,255,0.7);letter-spacing:.4px;}

# .v-overview{background:var(--ink);border-radius:16px;padding:20px 28px;margin:0 40px 8px;display:flex;align-items:center;flex-wrap:wrap;}
# .v-overview-item{flex:1;min-width:110px;padding:0 20px;border-right:1px solid rgba(255,255,255,0.11);}
# .v-overview-item:first-child{padding-left:0;}
# .v-overview-item:last-child{border-right:none;}
# .v-ov-label{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:rgba(255,255,255,0.42);margin-bottom:4px;}
# .v-ov-value{font-size:14.5px;font-weight:500;color:white;}
# .v-ov-value.accent{color:var(--gold);}

# .v-hotel{background:var(--white);border:1px solid var(--border);border-radius:16px;overflow:hidden;display:flex;margin-bottom:16px;transition:box-shadow .2s,transform .2s;}
# .v-hotel:hover{box-shadow:var(--shadow);transform:translateY(-2px);}
# .v-hotel-img{width:210px;flex-shrink:0;background-size:cover;background-position:center;min-height:160px;}
# .v-hotel-body{padding:22px 26px;flex:1;display:flex;flex-direction:column;justify-content:space-between;}
# .v-hotel-name{font-family:var(--ff-head);font-size:20px;font-weight:600;color:var(--ink);margin-bottom:8px;}
# .v-hotel-meta{display:flex;align-items:center;gap:14px;margin-bottom:10px;flex-wrap:wrap;}
# .v-rating{background:#FFF8EC;color:#92600A;font-size:12px;font-weight:600;padding:4px 10px;border-radius:99px;border:1px solid #F5D98A;}
# .v-hotel-addr{font-size:13px;color:var(--ink-soft);margin-bottom:14px;line-height:1.5;}
# .v-hotel-footer{display:flex;align-items:center;justify-content:space-between;border-top:1px solid var(--border);padding-top:14px;margin-top:4px;}
# .v-price{font-size:22px;font-weight:700;color:var(--accent);}
# .v-price small{font-size:13px;font-weight:400;color:var(--ink-soft);}
# .v-book-btn{background:var(--ink);color:white;font-size:13px;font-weight:600;padding:10px 22px;border-radius:99px;text-decoration:none;transition:background .2s;}
# .v-book-btn:hover{background:var(--accent);color:white;}

# .v-plan-line{padding:11px 18px;border-left:3px solid var(--accent);border-radius:0 10px 10px 0;background:#F5EDE6;margin-bottom:9px;font-size:14px;color:var(--ink);line-height:1.6;}
# .v-day-header{background:var(--ink);color:white;padding:10px 18px;border-radius:9px;font-size:12.5px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin:18px 0 10px;}

# .v-links-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:18px;}
# .v-link-card{background:var(--white);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center;text-decoration:none;color:var(--ink);font-size:13px;font-weight:500;transition:all .2s;display:block;}
# .v-link-card:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-2px);box-shadow:0 4px 14px rgba(196,98,45,0.12);}
# .v-link-icon{font-size:22px;margin-bottom:6px;}

# .v-metric{background:var(--white);border:1px solid var(--border);border-radius:14px;padding:20px;text-align:center;}
# .v-metric-label{font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--ink-soft);margin-bottom:8px;}
# .v-metric-value{font-family:var(--ff-head);font-size:24px;font-weight:600;color:var(--ink);}

# .v-place-card{background:var(--white);border:1px solid var(--border);border-radius:14px;overflow:hidden;margin-bottom:14px;transition:box-shadow .2s;}
# .v-place-card:hover{box-shadow:var(--shadow);}
# .v-place-img{width:100%;height:160px;background-size:cover;background-position:center;}
# .v-place-info{padding:14px 16px;}
# .v-place-name{font-weight:600;font-size:15px;color:var(--ink);margin-bottom:4px;}
# .v-place-addr{font-size:12px;color:var(--ink-soft);line-height:1.4;}

# .v-divider{height:1px;background:var(--border);margin:8px 0 20px;}
# .stSpinner>div{border-top-color:var(--accent)!important;}
# div[data-testid="stSuccess"]{background:#F0FAF4!important;border:1px solid #86EFAC!important;border-radius:12px!important;border-left:4px solid #22C55E!important;}
# div[data-testid="stWarning"]{border-radius:12px!important;border-left:4px solid #F59E0B!important;}

# /* ── BOT CHAT STYLES ── */
# .bot-header{
#   display:flex;align-items:center;gap:14px;
#   background:var(--ink);border-radius:16px;
#   padding:20px 28px;margin-bottom:20px;
# }
# .bot-avatar{
#   width:52px;height:52px;border-radius:50%;
#   background:linear-gradient(135deg,var(--accent),var(--gold));
#   display:flex;align-items:center;justify-content:center;
#   font-size:24px;flex-shrink:0;
# }
# .bot-header-text h3{
#   font-family:var(--ff-head);font-size:20px;
#   font-weight:600;color:white;margin-bottom:4px;
# }
# .bot-header-text p{font-size:13px;color:rgba(255,255,255,0.6);}
# .bot-status{
#   margin-left:auto;display:flex;align-items:center;gap:7px;
#   font-size:12px;color:rgba(255,255,255,0.7);font-weight:500;
# }
# .bot-status::before{
#   content:'';width:8px;height:8px;background:#4ade80;
#   border-radius:50%;animation:blink 2s infinite;
# }
# .bot-chat-area{
#   background:var(--white);border:1px solid var(--border);
#   border-radius:16px;padding:20px;
#   min-height:280px;max-height:440px;
#   overflow-y:auto;margin-bottom:14px;
# }
# .bot-bubble-wrap{display:flex;margin-bottom:16px;gap:10px;align-items:flex-end;}
# .bot-bubble-wrap.user{flex-direction:row-reverse;}
# .bot-icon{
#   width:34px;height:34px;border-radius:50%;flex-shrink:0;
#   display:flex;align-items:center;justify-content:center;font-size:16px;
# }
# .bot-icon.assistant{background:linear-gradient(135deg,var(--accent),var(--gold));}
# .bot-icon.user-ic{background:var(--ink);}
# .bot-bubble{
#   max-width:75%;padding:12px 16px;border-radius:16px;
#   font-size:14px;line-height:1.6;color:var(--ink);
# }
# .bot-bubble.assistant{
#   background:var(--cream);border:1px solid var(--border);
#   border-bottom-left-radius:4px;
# }
# .bot-bubble.user{
#   background:var(--accent);color:white;
#   border-bottom-right-radius:4px;
# }
# .bot-empty{text-align:center;padding:50px 20px;color:var(--ink-soft);font-size:14px;}
# .bot-empty .bot-empty-icon{font-size:40px;margin-bottom:12px;}
# .bot-empty h4{font-family:var(--ff-head);font-size:18px;color:var(--ink);margin-bottom:8px;}

# /* standalone section */
# .bot-standalone{padding:40px 40px 0;}
# .bot-standalone-head{margin-bottom:24px;}
# .bot-standalone-head h2{
#   font-family:var(--ff-head);font-size:30px;
#   font-weight:600;color:var(--ink);letter-spacing:-0.5px;margin-bottom:6px;
# }
# .bot-standalone-head p{font-size:14px;color:var(--ink-soft);line-height:1.6;}

# .v-footer{background:var(--ink);color:rgba(255,255,255,0.45);text-align:center;padding:28px;font-size:13px;margin-top:64px;}
# .v-footer strong{color:rgba(255,255,255,0.8);font-weight:500;}
# </style>
# """, unsafe_allow_html=True)

# # ─────────────────────────────────────────
# # NAVBAR
# # ─────────────────────────────────────────

# st.markdown("""
# <div class="v-nav">
#   <div class="v-logo">✈ Voyag<span>r</span></div>
#   <div class="v-nav-links">
#     <a href="#">Explore</a>
#     <a href="#">Hotels</a>
#     <a href="#">Flights</a>
#     <a href="#">Packages</a>
#     <a href="#" class="v-nav-cta">Sign in</a>
#   </div>
# </div>
# <div class="v-spacer"></div>
# """, unsafe_allow_html=True)

# # ─────────────────────────────────────────
# # HERO
# # ─────────────────────────────────────────

# st.markdown("""
# <div class="v-hero">
#   <div class="v-slide v-s1"></div>
#   <div class="v-slide v-s2"></div>
#   <div class="v-slide v-s3"></div>
#   <div class="v-slide v-s4"></div>
#   <div class="v-hero-overlay"></div>
#   <div class="v-hero-text">
#     <div class="v-hero-tag">AI-Powered Travel Planning</div>
#     <h1>Your next <em>adventure</em>,<br>perfectly planned.</h1>
#     <p>From itinerary to hotels — Voyagr builds your dream trip in seconds using AI.</p>
#   </div>
#   <div class="v-dots">
#     <div class="v-dot d1"></div>
#     <div class="v-dot d2"></div>
#     <div class="v-dot d3"></div>
#     <div class="v-dot d4"></div>
#   </div>
# </div>
# """, unsafe_allow_html=True)

# # ─────────────────────────────────────────
# # SEARCH PANEL
# # ─────────────────────────────────────────

# st.markdown("<div class='v-search-wrap'><div class='v-search-panel'>", unsafe_allow_html=True)
# st.markdown("<div class='v-search-eyebrow'>Plan your trip</div>", unsafe_allow_html=True)

# row1_c1, row1_c2 = st.columns(2)
# with row1_c1:
#     st.markdown("<span class='v-field-label'>📍 From</span>", unsafe_allow_html=True)
#     source = st.text_input("From", placeholder="Enter origin city (e.g. Indore)", label_visibility="collapsed")
# with row1_c2:
#     st.markdown("<span class='v-field-label'>🏁 To</span>", unsafe_allow_html=True)
#     destination = st.text_input("To", placeholder="e.g. Goa, Manali, Jaipur, Delhi", label_visibility="collapsed")

# st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# row2_c1, row2_c2, row2_c3, row2_c4, row2_c5 = st.columns([1, 1.2, 1.2, 1.2, 1.4])

# with row2_c1:
#     st.markdown("<span class='v-field-label'>📅 Days</span>", unsafe_allow_html=True)
#     days = st.number_input("Days", min_value=1, max_value=15, value=3, label_visibility="collapsed")

# with row2_c2:
#     st.markdown("<span class='v-field-label'>💰 Min Budget (₹)</span>", unsafe_allow_html=True)
#     budget_min = st.number_input("Min Budget", min_value=0, value=5000, step=1000, label_visibility="collapsed")

# with row2_c3:
#     st.markdown("<span class='v-field-label'>💰 Max Budget (₹)</span>", unsafe_allow_html=True)
#     budget_max = st.number_input("Max Budget", min_value=0, value=20000, step=1000, label_visibility="collapsed")

# with row2_c4:
#     st.markdown("<span class='v-field-label'>🚆 Travel Mode</span>", unsafe_allow_html=True)
#     travel_mode = st.selectbox("Mode", ["🚗 Car", "✈️ Flight", "🚆 Train", "🚌 Bus"], label_visibility="collapsed")

# with row2_c5:
#     st.markdown("<span class='v-field-label'>👥 Traveling As</span>", unsafe_allow_html=True)
#     traveler_type = st.selectbox(
#         "Traveler Type",
#         ["👫 Couple", "👨‍👩‍👧‍👦 Family with Kids", "👯 Friends Group",
#          "🧳 Solo Traveler", "💼 Business Traveler", "🧓 Senior Citizens", "🎒 Backpacker"],
#         label_visibility="collapsed"
#     )

# if budget_min > budget_max:
#     st.warning("⚠️ Minimum budget cannot exceed maximum budget.")

# st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
# generate = st.button("✦  Generate My Trip Plan", use_container_width=True)
# st.markdown("</div></div>", unsafe_allow_html=True)

# # ─────────────────────────────────────────
# # POPULAR DESTINATIONS
# # ─────────────────────────────────────────

# st.markdown("""
# <div class="v-section">
#   <div class="v-section-head">
#     <h2>Popular Destinations</h2>
#     <span>Trending in India</span>
#   </div>
# </div>
# """, unsafe_allow_html=True)

# dest_data = [
#     ("Goa",    "Sun, Sea & Serenity",   "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80"),
#     ("Manali", "Mountains & Adventure", "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=600&q=80"),
#     ("Jaipur", "Royal Heritage",        "https://images.unsplash.com/photo-1548013146-72479768bada?w=600&q=80"),
#     ("Kerala", "Backwaters & Spice",    "https://images.unsplash.com/photo-1593693411515-c20261bcad6e?w=600&q=80"),
# ]

# dcols = st.columns(4, gap="medium")
# for i, (name, sub, img) in enumerate(dest_data):
#     with dcols[i]:
#         st.markdown(f"""
#         <div class="v-dest-card" style="background-image:url('{img}');">
#           <div class="v-dest-gradient"></div>
#           <div class="v-dest-info">
#             <div class="v-dest-name">{name}</div>
#             <div class="v-dest-sub">{sub}</div>
#           </div>
#         </div>
#         """, unsafe_allow_html=True)

# # ─────────────────────────────────────────
# # RESULTS  (Trip Plan + Bot as 5th tab)
# # ─────────────────────────────────────────

# if generate and source and destination:

#     with st.spinner("Building your perfect trip plan..."):
#         route_places = get_route_places(source, destination)
#         hotels       = get_hotels(destination, days, budget_max)
#         plan         = generate_plan(source, destination, days, budget_min, budget_max,
#                                      travel_mode, route_places, traveler_type)

#     st.success(f"✓  Your trip from {source} to {destination} is ready!")

#     mode_clean = travel_mode.replace("🚗 ","").replace("✈️ ","").replace("🚆 ","").replace("🚌 ","")

#     st.markdown(f"""
#     <div class="v-overview">
#       <div class="v-overview-item"><div class="v-ov-label">Journey</div><div class="v-ov-value accent">{source} → {destination}</div></div>
#       <div class="v-overview-item"><div class="v-ov-label">Duration</div><div class="v-ov-value">{days} Days</div></div>
#       <div class="v-overview-item"><div class="v-ov-label">Budget</div><div class="v-ov-value">₹{budget_min:,} – ₹{budget_max:,}</div></div>
#       <div class="v-overview-item"><div class="v-ov-label">Travel Mode</div><div class="v-ov-value">{mode_clean}</div></div>
#       <div class="v-overview-item"><div class="v-ov-label">Traveling As</div><div class="v-ov-value">{traveler_type}</div></div>
#       <div class="v-overview-item"><div class="v-ov-label">Hotels Found</div><div class="v-ov-value">{len(hotels)} options</div></div>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("<div style='padding:20px 40px 0;'>", unsafe_allow_html=True)

#     tab1, tab2, tab3, tab4, tab5 = st.tabs(
#         ["  🗺️  Itinerary  ", "  🛣️  Route Places  ", "  🏨  Hotels  ", "  📊  Summary  ", "  🤖  AI Assistant  "]
#     )

#     # ── ITINERARY ──
#     with tab1:
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.markdown("### Day-wise Itinerary")
#         st.markdown("<div class='v-divider'></div>", unsafe_allow_html=True)
#         for line in plan.split("\n"):
#             line = line.strip()
#             if not line:
#                 continue
#             if line.lower().startswith("day") or line.startswith("##"):
#                 st.markdown(f"<div class='v-day-header'>{line.replace('##','').replace('**','').strip()}</div>", unsafe_allow_html=True)
#             else:
#                 clean = line.lstrip("*-•").strip()
#                 if clean:
#                     st.markdown(f"<div class='v-plan-line'>{clean}</div>", unsafe_allow_html=True)
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.markdown("### Quick Booking")
#         st.markdown("<div class='v-divider'></div>", unsafe_allow_html=True)
#         st.markdown("""
#         <div class="v-links-grid">
#           <a href="https://www.makemytrip.com" target="_blank" class="v-link-card"><div class="v-link-icon">🛏️</div>MakeMyTrip</a>
#           <a href="https://www.irctc.co.in"    target="_blank" class="v-link-card"><div class="v-link-icon">🚆</div>IRCTC</a>
#           <a href="https://www.redbus.in"      target="_blank" class="v-link-card"><div class="v-link-icon">🚌</div>RedBus</a>
#           <a href="https://www.goibibo.com"    target="_blank" class="v-link-card"><div class="v-link-icon">✈️</div>Goibibo</a>
#         </div>
#         """, unsafe_allow_html=True)

#     # ── ROUTE PLACES ──
#     with tab2:
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.markdown("### Attractions Along Your Route")
#         st.markdown("<div class='v-divider'></div>", unsafe_allow_html=True)
#         if not route_places:
#             st.warning("No route places found for this journey.")
#         else:
#             cols = st.columns(2, gap="medium")
#             for i, p in enumerate(route_places):
#                 with cols[i % 2]:
#                     st.markdown(f"""
#                     <div class="v-place-card">
#                       <div class="v-place-img" style="background-image:url('{p['image']}');"></div>
#                       <div class="v-place-info">
#                         <div class="v-place-name">📍 {p['title']}</div>
#                         <div class="v-place-addr">{p['address']}</div>
#                       </div>
#                     </div>
#                     """, unsafe_allow_html=True)

#     # ── HOTELS ──
#     with tab3:
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.markdown("### Available Hotels")
#         st.markdown("<div class='v-divider'></div>", unsafe_allow_html=True)
#         if not hotels:
#             st.warning("No hotels found. Try increasing your max budget or check your RapidAPI key.")
#         else:
#             for h in hotels:
#                 price = h.get("price_per_night", 0)
#                 try:
#                     pf = f"₹{int(price):,}"
#                 except Exception:
#                     pf = f"₹{price}"

#                 img_url = h.get("image", "")
#                 if img_url:
#                     img_html = f'<div class="v-hotel-img" style="background-image:url(\'{img_url}\');"></div>'
#                 else:
#                     img_html = '<div class="v-hotel-img" style="background:#f0ede8;display:flex;align-items:center;justify-content:center;font-size:36px;">🏨</div>'

#                 st.markdown(f"""
#                 <div class="v-hotel">
#                   {img_html}
#                   <div class="v-hotel-body">
#                     <div>
#                       <div class="v-hotel-name">{h.get('name','Hotel')}</div>
#                       <div class="v-hotel-meta">
#                         <span class="v-rating">⭐ {h.get('rating','N/A')} / 10 — {h.get('review','')}</span>
#                         <span style="font-size:12px;color:#888;">📏 {h.get('distance','N/A')} from centre</span>
#                       </div>
#                       <div class="v-hotel-addr">📍 {h.get('address','N/A')}</div>
#                     </div>
#                     <div class="v-hotel-footer">
#                       <div class="v-price">{pf} <small>/ night</small></div>
#                       <a href="{h.get('url','#')}" target="_blank" class="v-book-btn">Book Now →</a>
#                     </div>
#                   </div>
#                 </div>
#                 """, unsafe_allow_html=True)

#     # ── SUMMARY ──
#     with tab4:
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.markdown("### Trip Summary")
#         st.markdown("<div class='v-divider'></div>", unsafe_allow_html=True)
#         m1, m2, m3, m4 = st.columns(4, gap="medium")
#         for col, (lbl, val) in zip([m1, m2, m3, m4], [
#             ("Origin", source), ("Destination", destination),
#             ("Duration", f"{days} days"), ("Max Budget", f"₹{budget_max:,}")
#         ]):
#             with col:
#                 st.markdown(f'<div class="v-metric"><div class="v-metric-label">{lbl}</div><div class="v-metric-value">{val}</div></div>', unsafe_allow_html=True)

#         st.markdown("<br>", unsafe_allow_html=True)
#         st.dataframe(pd.DataFrame({
#             "Detail": ["From", "To", "Duration", "Budget Range", "Travel Mode", "Traveling As", "Hotels Found", "Attractions"],
#             "Value":  [source, destination, f"{days} days",
#                        f"₹{budget_min:,} – ₹{budget_max:,}", travel_mode,
#                        traveler_type, str(len(hotels)), str(len(route_places))]
#         }), use_container_width=True, hide_index=True)

#     # ── AI ASSISTANT TAB (make.com bot) ──
#     with tab5:
#         st.markdown("<br>", unsafe_allow_html=True)

#         st.markdown(f"""
#         <div class="bot-header">
#           <div class="bot-avatar">🤖</div>
#           <div class="bot-header-text">
#             <h3>Voyagr AI Assistant</h3>
#             <p>Ask anything about your {destination} trip — visa, packing, local tips & more</p>
#           </div>
#           <div class="bot-status">Online · Powered by make.com</div>
#         </div>
#         """, unsafe_allow_html=True)

#         # Session state for this tab's chat
#         if "bot_messages" not in st.session_state:
#             st.session_state.bot_messages = []

#         # Clear chat
#         if st.button("🗑️ Clear Chat", key="clear_bot_tab"):
#             st.session_state.bot_messages = []
#             st.rerun()

#         # Suggestion chips (only when empty)
#         if not st.session_state.bot_messages:
#             st.markdown("<p style='font-size:13px;color:var(--ink-soft);margin-bottom:8px;font-weight:500;'>💡 Quick questions:</p>", unsafe_allow_html=True)
#             suggestions = [
#                 f"Best time to visit {destination}?",
#                 f"What to pack for {destination}?",
#                 f"Local food to try in {destination}",
#                 f"Safety tips for {destination}",
#                 f"Hidden gems in {destination}",
#                 f"Budget tips for {destination}",
#             ]
#             sug_cols = st.columns(3)
#             for idx, sug in enumerate(suggestions):
#                 with sug_cols[idx % 3]:
#                     if st.button(sug, key=f"tab_sug_{idx}"):
#                         st.session_state.bot_messages.append({"role": "user", "content": sug})
#                         with st.spinner("Thinking..."):
#                             reply = ask_bot(sug)
#                         st.session_state.bot_messages.append({"role": "assistant", "content": reply})
#                         st.rerun()

#         # Chat display
#         st.markdown("<div class='bot-chat-area'>", unsafe_allow_html=True)
#         if not st.session_state.bot_messages:
#             st.markdown("""
#             <div class="bot-empty">
#               <div class="bot-empty-icon">✈️</div>
#               <h4>Your travel assistant is ready</h4>
#               <p>Ask anything about your destination, packing tips, visa info, local food, safety & more.</p>
#             </div>
#             """, unsafe_allow_html=True)
#         else:
#             for msg in st.session_state.bot_messages:
#                 if msg["role"] == "user":
#                     st.markdown(f"""
#                     <div class="bot-bubble-wrap user">
#                       <div class="bot-icon user-ic">👤</div>
#                       <div class="bot-bubble user">{msg['content']}</div>
#                     </div>""", unsafe_allow_html=True)
#                 else:
#                     st.markdown(f"""
#                     <div class="bot-bubble-wrap">
#                       <div class="bot-icon assistant">🤖</div>
#                       <div class="bot-bubble assistant">{msg['content']}</div>
#                     </div>""", unsafe_allow_html=True)
#         st.markdown("</div>", unsafe_allow_html=True)

#         # Chat input
#         bot_input = st.chat_input(
#             f"Ask about {destination}... e.g. visa, packing list, local food",
#             key="bot_tab_input"
#         )
#         if bot_input:
#             st.session_state.bot_messages.append({"role": "user", "content": bot_input})
#             with st.spinner("Voyagr AI is thinking..."):
#                 reply = ask_bot(bot_input)
#             st.session_state.bot_messages.append({"role": "assistant", "content": reply})
#             st.rerun()

#     st.markdown("</div>", unsafe_allow_html=True)

# # ─────────────────────────────────────────
# # STANDALONE BOT SECTION
# # Always visible below — for general travel questions
# # ─────────────────────────────────────────

# st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

# st.markdown("""
# <div class="bot-standalone">
#   <div class="bot-standalone-head">
#     <h2>🤖 AI Travel Assistant</h2>
#     <p>Not planning a specific trip yet? Ask any travel question — destination ideas, visa info, packing lists, best seasons, and more.</p>
#   </div>
# </div>
# """, unsafe_allow_html=True)

# if "standalone_messages" not in st.session_state:
#     st.session_state.standalone_messages = []

# st.markdown("<div style='padding:0 40px;'>", unsafe_allow_html=True)

# st.markdown("""
# <div class="bot-header">
#   <div class="bot-avatar">✈️</div>
#   <div class="bot-header-text">
#     <h3>Ask Voyagr Anything</h3>
#     <p>Visa requirements · Packing tips · Best seasons · Local food · Safety advice</p>
#   </div>
#   <div class="bot-status">Online · Always Ready</div>
# </div>
# """, unsafe_allow_html=True)

# # Clear button
# if st.button("🗑️ Clear", key="clear_standalone"):
#     st.session_state.standalone_messages = []
#     st.rerun()

# # Chat display
# st.markdown("<div class='bot-chat-area'>", unsafe_allow_html=True)
# if not st.session_state.standalone_messages:
#     st.markdown("""
#     <div class="bot-empty">
#       <div class="bot-empty-icon">🌍</div>
#       <h4>Where do you want to go?</h4>
#       <p>Ask me anything — I can help with any destination worldwide.</p>
#     </div>
#     """, unsafe_allow_html=True)
# else:
#     for msg in st.session_state.standalone_messages:
#         if msg["role"] == "user":
#             st.markdown(f"""
#             <div class="bot-bubble-wrap user">
#               <div class="bot-icon user-ic">👤</div>
#               <div class="bot-bubble user">{msg['content']}</div>
#             </div>""", unsafe_allow_html=True)
#         else:
#             st.markdown(f"""
#             <div class="bot-bubble-wrap">
#               <div class="bot-icon assistant">🤖</div>
#               <div class="bot-bubble assistant">{msg['content']}</div>
#             </div>""", unsafe_allow_html=True)
# st.markdown("</div>", unsafe_allow_html=True)

# # Chat input
# sa_input = st.chat_input(
#     "Ask any travel question... e.g. 'Best time to visit Japan?'",
#     key="standalone_bot_input"
# )
# if sa_input:
#     st.session_state.standalone_messages.append({"role": "user", "content": sa_input})
#     with st.spinner("Thinking..."):
#         sa_reply = ask_bot(sa_input)
#     st.session_state.standalone_messages.append({"role": "assistant", "content": sa_reply})
#     st.rerun()

# st.markdown("</div>", unsafe_allow_html=True)

# # ─────────────────────────────────────────
# # FOOTER
# # ─────────────────────────────────────────

# st.markdown("""
# <div class="v-footer">
#   <strong>Voyagr</strong> — AI Travel Planner &nbsp;·&nbsp;
#   Built with Gemini AI &nbsp;·&nbsp;
#   Hotel data via Booking.com &nbsp;·&nbsp;
#   Maps by Geoapify &nbsp;·&nbsp;
#   Bot powered by make.com<br><br>
#   © 2026 Voyagr · All rights reserved
# </div>
# """, unsafe_allow_html=True)