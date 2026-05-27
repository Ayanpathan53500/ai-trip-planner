

import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient
import requests
from datetime import datetime, timedelta
import pandas as pd
from database import save_chat, load_chats, clear_session

load_dotenv()

MAKE_WEBHOOK_URL = "https://hook.us2.make.com/ib1w3k6e16d8w9g34baesyg87l8thu5q"

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
            try:
                res = requests.get(
                    geo_url,
                    params={"text": city + " India", "apiKey": GEOAPIFY_API_KEY},
                    timeout=10
                ).json()
                if not res.get("features"):
                    return None
                p = res["features"][0]["properties"]
                return p["lon"], p["lat"]
            except Exception as e:
                print(f"Geocode error for {city}: {e}")
                return None

        start = get_coords(source)
        end   = get_coords(destination)
        print(f"Coords — start: {start}, end: {end}")

        if not start or not end:
            print("Geocoding failed, falling back to Tavily")
            return _get_route_places_tavily(source, destination)

        # ── Routing ──
        try:
            rr = requests.get(
                "https://api.geoapify.com/v1/routing",
                params={
                    "waypoints": f"{start[1]},{start[0]}|{end[1]},{end[0]}",
                    "mode":      "drive",
                    "apiKey":    GEOAPIFY_API_KEY
                },
                timeout=15
            ).json()
        except Exception as e:
            print(f"Routing error: {e}")
            return _get_route_places_tavily(source, destination)

        if "features" not in rr or not rr["features"]:
            print(f"No routing features. Response: {rr}")
            return _get_route_places_tavily(source, destination)

        # ── Flatten coordinates ──
        geometry = rr["features"][0]["geometry"]
        coords   = geometry["coordinates"]
        if isinstance(coords[0][0], list):
            flat = [pt for segment in coords for pt in segment]
        elif isinstance(coords[0], list):
            flat = coords
        else:
            flat = [coords]

        if not flat:
            return _get_route_places_tavily(source, destination)

        # ── Sample 8 points ──
        total   = len(flat)
        indices = [int(i * (total - 1) / 7) for i in range(8)] if total >= 8 else list(range(total))
        sampled = [flat[i] for i in indices]

        places, seen = [], set()

        for lon, lat in sampled:
            try:
                res = requests.get(
                    "https://api.geoapify.com/v2/places",
                    params={
                        "categories": "tourism.sights,tourism.attraction,tourism.museum",
                        "filter":     f"circle:{lon},{lat},5000",
                        "limit":      3,
                        "apiKey":     GEOAPIFY_API_KEY
                    },
                    timeout=10
                ).json()
            except Exception as e:
                print(f"Places fetch error at {lon},{lat}: {e}")
                continue

            for item in res.get("features", []):
                prop = item.get("properties", {})
                name = prop.get("name") or prop.get("address_line1") or prop.get("formatted", "")[:40]
                if not name or name in seen:
                    continue
                seen.add(name)
                place_lon = prop.get("lon", lon)
                place_lat = prop.get("lat", lat)
                image_url = (
                    f"https://maps.geoapify.com/v1/staticmap"
                    f"?style=osm-carto&width=400&height=240"
                    f"&center=lonlat:{place_lon},{place_lat}"
                    f"&zoom=14&marker=lonlat:{place_lon},{place_lat};type:awesome;color:%23C4622D"
                    f"&apiKey={GEOAPIFY_API_KEY}"
                )
                places.append({
                    "title":   name,
                    "address": prop.get("formatted", ""),
                    "image":   image_url
                })
                if len(places) >= 12:
                    break
            if len(places) >= 12:
                break

        print(f"Geoapify found {len(places)} places")

        # ── Fallback if Geoapify returned nothing ──
        if not places:
            return _get_route_places_tavily(source, destination)

        return places[:10]

    except Exception as e:
        print(f"get_route_places error: {e}")
        import traceback
        traceback.print_exc()
        return _get_route_places_tavily(source, destination)


def _get_route_places_tavily(source, destination):
    """Fallback: use Tavily to search for tourist attractions along the route."""
    try:
        print(f"Using Tavily fallback for {source} → {destination}")
        query = f"tourist attractions places to visit between {source} and {destination} India road trip"
        results = tavily.search(query=query, max_results=8, search_depth="basic")

        places = []
        seen   = set()

        for r in results.get("results", []):
            title   = r.get("title", "").strip()
            content = r.get("content", "").strip()
            url     = r.get("url", "")

            if not title or title in seen:
                continue
            seen.add(title)

            # Build a static map image using a simple geocode of the title
            try:
                geo = requests.get(
                    "https://api.geoapify.com/v1/geocode/search",
                    params={"text": title + " India", "apiKey": GEOAPIFY_API_KEY},
                    timeout=6
                ).json()
                if geo.get("features"):
                    p   = geo["features"][0]["properties"]
                    lon = p.get("lon", 78.9629)
                    lat = p.get("lat", 20.5937)
                else:
                    lon, lat = 78.9629, 20.5937
            except Exception:
                lon, lat = 78.9629, 20.5937

            image_url = (
                f"https://maps.geoapify.com/v1/staticmap"
                f"?style=osm-carto&width=400&height=240"
                f"&center=lonlat:{lon},{lat}"
                f"&zoom=13&marker=lonlat:{lon},{lat};type:awesome;color:%23C4622D"
                f"&apiKey={GEOAPIFY_API_KEY}"
            )

            # Use first 120 chars of content as address/description
            address = content[:120] + "…" if len(content) > 120 else content

            places.append({
                "title":   title,
                "address": address,
                "image":   image_url
            })

            if len(places) >= 8:
                break

        print(f"Tavily fallback found {len(places)} places")
        return places

    except Exception as e:
        print(f"Tavily fallback error: {e}")
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
            return []

        results = res.json().get("result", [])
        if not results:
            return []

        hotels = []
        for h in results[:30]:
            price    = None
            currency = "INR"

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

            if not price:
                pb = h.get("price_breakdown", {})
                if pb.get("gross_price"):
                    price    = float(pb["gross_price"]) / max(days, 1)
                    currency = pb.get("currency", "INR")

            if not price and h.get("min_total_price"):
                price    = float(h["min_total_price"]) / max(days, 1)
                currency = "INR"

            if not price or price <= 0:
                continue

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
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
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
  --nav-h:64px;
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
  height:var(--nav-h);display:flex;align-items:center;
  justify-content:space-between;padding:0 40px;
  box-shadow:0 1px 0 var(--border),0 4px 16px rgba(26,23,20,0.04);
}
.v-logo{font-family:var(--ff-head);font-size:22px;font-weight:700;color:var(--ink);letter-spacing:-0.5px;display:flex;align-items:center;gap:8px;}
.v-logo span{color:var(--accent);}
.v-nav-links{display:flex;gap:28px;font-size:13.5px;font-weight:500;color:var(--ink-soft);align-items:center;}
.v-nav-links a{color:var(--ink-soft);text-decoration:none;transition:color 0.2s;}
.v-nav-links a:hover{color:var(--accent);}
.v-nav-cta{background:var(--ink);color:var(--white)!important;padding:9px 22px;border-radius:99px;font-size:13px;font-weight:500;text-decoration:none;transition:background 0.2s;}
.v-nav-cta:hover{background:var(--accent)!important;}
.v-spacer{height:var(--nav-h);}

.v-hero{position:relative;height:560px;overflow:hidden;background:#1A1714;}
.v-slide{position:absolute;inset:0;background-size:cover;background-position:center 40%;opacity:0;transition:opacity 1.2s ease-in-out;}
.v-s1{background-image:url('https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1600&q=80');animation:fade4 20s 0s infinite;}
.v-s2{background-image:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&q=80');animation:fade4 20s 5s infinite;}
.v-s3{background-image:url('https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1600&q=80');animation:fade4 20s 10s infinite;}
.v-s4{background-image:url('https://images.unsplash.com/photo-1548013146-72479768bada?w=1600&q=80');animation:fade4 20s 15s infinite;}
@keyframes fade4{0%{opacity:0;}5%{opacity:1;}25%{opacity:1;}30%{opacity:0;}100%{opacity:0;}}
.v-hero-overlay{position:absolute;inset:0;z-index:2;background:linear-gradient(to top,rgba(26,23,20,0.88) 0%,rgba(26,23,20,0.45) 45%,rgba(26,23,20,0.10) 100%);}
.v-hero-text{position:absolute;bottom:0;left:0;right:0;z-index:3;padding:0 40px 48px;pointer-events:none;}
.v-hero-tag{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,0.13);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.26);color:white;font-size:11.5px;font-weight:500;letter-spacing:1.4px;text-transform:uppercase;padding:7px 16px;border-radius:99px;margin-bottom:18px;}
.v-hero-tag::before{content:"";width:7px;height:7px;background:#4ade80;border-radius:50%;animation:blink 2s infinite;}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.4;}}
.v-hero-text h1{font-family:var(--ff-head);font-size:52px;font-weight:700;color:white;line-height:1.08;letter-spacing:-1.5px;margin-bottom:14px;text-shadow:0 2px 20px rgba(0,0,0,.3);}
.v-hero-text h1 em{font-style:italic;color:var(--gold);}
.v-hero-text p{font-size:16px;color:rgba(255,255,255,0.76);font-weight:300;line-height:1.6;max-width:560px;}
.v-dots{position:absolute;bottom:22px;right:40px;z-index:4;display:flex;gap:8px;align-items:center;}
.v-dot{width:8px;height:8px;border-radius:99px;background:rgba(255,255,255,0.35);}
.v-dot.d1{animation:dot1 20s 0s infinite;}.v-dot.d2{animation:dot1 20s 5s infinite;}.v-dot.d3{animation:dot1 20s 10s infinite;}.v-dot.d4{animation:dot1 20s 15s infinite;}
@keyframes dot1{0%,4%{background:white;width:22px;}30%,100%{background:rgba(255,255,255,0.35);width:8px;}}

.v-search-wrap{padding:0 32px;margin-top:-48px;position:relative;z-index:50;}
.v-search-panel{background:var(--white);border-radius:20px;border:1px solid var(--border);box-shadow:var(--shadow-lg);padding:24px 28px 20px;}
.v-search-eyebrow{font-size:15px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:var(--ink-soft);margin-bottom:16px;display:flex;align-items:center;gap:10px;}
.v-search-eyebrow::before{content:'';width:24px;height:2px;background:var(--accent);border-radius:2px;display:inline-block;}
.v-field-label{font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--ink-soft);margin-bottom:6px;display:block;}

div[data-baseweb="input"] input{background:var(--cream)!important;border:1.5px solid var(--border)!important;border-radius:10px!important;font-family:var(--ff-body)!important;font-size:15px!important;color:var(--ink)!important;height:48px!important;padding:0 16px!important;transition:border-color .2s,box-shadow .2s!important;}
div[data-baseweb="input"] input:focus{border-color:var(--accent)!important;background:white!important;box-shadow:0 0 0 3px rgba(196,98,45,0.11)!important;}
div[data-baseweb="select"]>div{background:var(--cream)!important;border:1.5px solid var(--border)!important;border-radius:10px!important;font-family:var(--ff-body)!important;font-size:15px!important;min-height:48px!important;}
div[data-testid="stNumberInput"] input{background:var(--cream)!important;border:1.5px solid var(--border)!important;border-radius:10px!important;font-size:15px!important;height:48px!important;}

div[data-testid="stButton"]>button{background:var(--accent)!important;color:white!important;border:none!important;border-radius:12px!important;font-family:var(--ff-body)!important;font-size:15.5px!important;font-weight:700!important;height:52px!important;letter-spacing:.4px!important;transition:all .2s!important;box-shadow:0 4px 18px rgba(196,98,45,0.32)!important;}
div[data-testid="stButton"]>button:hover{background:#b05527!important;transform:translateY(-1px)!important;box-shadow:0 7px 24px rgba(196,98,45,0.42)!important;}
div[data-testid="stButton"]>button:active{transform:translateY(0)!important;}

div[data-baseweb="tab-list"]{background:var(--cream)!important;border-radius:12px!important;padding:4px!important;gap:2px!important;border:1px solid var(--border)!important;flex-wrap:wrap!important;}
button[data-baseweb="tab"]{font-family:var(--ff-body)!important;font-size:13px!important;font-weight:500!important;border-radius:9px!important;color:var(--ink-soft)!important;padding:8px 16px!important;transition:all .2s!important;}
button[data-baseweb="tab"][aria-selected="true"]{background:var(--white)!important;color:var(--accent)!important;font-weight:700!important;box-shadow:0 1px 8px rgba(26,23,20,0.08)!important;}
div[data-baseweb="tab-highlight"],div[data-baseweb="tab-border"]{display:none!important;}

.v-section{padding:36px 32px 16px;}
.v-section-head{display:flex;align-items:baseline;gap:12px;margin-bottom:20px;}
.v-section-head h2{font-family:var(--ff-head);font-size:26px;font-weight:600;color:var(--ink);letter-spacing:-0.4px;}
.v-section-head span{font-size:13px;color:var(--ink-soft);}

.v-dest-card{border-radius:14px;overflow:hidden;height:200px;position:relative;cursor:pointer;background-size:cover;background-position:center;transition:transform .3s cubic-bezier(.34,1.56,.64,1);}
.v-dest-card:hover{transform:translateY(-5px);}
.v-dest-gradient{position:absolute;inset:0;background:linear-gradient(to top,rgba(26,23,20,0.76) 0%,transparent 55%);}
.v-dest-info{position:absolute;bottom:0;left:0;right:0;padding:14px;}
.v-dest-name{font-family:var(--ff-head);font-size:17px;font-weight:600;color:white;margin-bottom:2px;}
.v-dest-sub{font-size:11px;color:rgba(255,255,255,0.7);letter-spacing:.4px;}

.v-overview{background:var(--ink);border-radius:16px;padding:18px 24px;margin:0 32px 8px;display:flex;align-items:center;flex-wrap:wrap;gap:12px;}
.v-overview-item{flex:1;min-width:100px;padding:0 16px;border-right:1px solid rgba(255,255,255,0.11);}
.v-overview-item:first-child{padding-left:0;}
.v-overview-item:last-child{border-right:none;}
.v-ov-label{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:rgba(255,255,255,0.42);margin-bottom:4px;}
.v-ov-value{font-size:14px;font-weight:500;color:white;}
.v-ov-value.accent{color:var(--gold);}

.v-hotel{background:var(--white);border:1px solid var(--border);border-radius:16px;overflow:hidden;display:flex;margin-bottom:16px;transition:box-shadow .2s,transform .2s;}
.v-hotel:hover{box-shadow:var(--shadow);transform:translateY(-2px);}
.v-hotel-img{width:200px;flex-shrink:0;background-size:cover;background-position:center;min-height:150px;}
.v-hotel-body{padding:20px 24px;flex:1;display:flex;flex-direction:column;justify-content:space-between;}
.v-hotel-name{font-family:var(--ff-head);font-size:19px;font-weight:600;color:var(--ink);margin-bottom:8px;}
.v-hotel-meta{display:flex;align-items:center;gap:12px;margin-bottom:10px;flex-wrap:wrap;}
.v-rating{background:#FFF8EC;color:#92600A;font-size:12px;font-weight:600;padding:4px 10px;border-radius:99px;border:1px solid #F5D98A;}
.v-hotel-addr{font-size:13px;color:var(--ink-soft);margin-bottom:14px;line-height:1.5;}
.v-hotel-footer{display:flex;align-items:center;justify-content:space-between;border-top:1px solid var(--border);padding-top:14px;margin-top:4px;flex-wrap:wrap;gap:10px;}
.v-price{font-size:22px;font-weight:700;color:var(--accent);}
.v-price small{font-size:13px;font-weight:400;color:var(--ink-soft);}
.v-book-btn{background:var(--ink);color:white;font-size:13px;font-weight:600;padding:10px 20px;border-radius:99px;text-decoration:none;transition:background .2s;}
.v-book-btn:hover{background:var(--accent);color:white;}

.v-plan-line{padding:11px 18px;border-left:3px solid var(--accent);border-radius:0 10px 10px 0;background:#F5EDE6;margin-bottom:9px;font-size:14px;color:var(--ink);line-height:1.6;}
.v-day-header{background:var(--ink);color:white;padding:10px 18px;border-radius:9px;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin:18px 0 10px;}

.v-links-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:18px;}
.v-link-card{background:var(--white);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center;text-decoration:none;color:var(--ink);font-size:13px;font-weight:500;transition:all .2s;display:block;}
.v-link-card:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-2px);box-shadow:0 4px 14px rgba(196,98,45,0.12);}
.v-link-icon{font-size:22px;margin-bottom:6px;}

.v-metric{background:var(--white);border:1px solid var(--border);border-radius:14px;padding:18px;text-align:center;}
.v-metric-label{font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--ink-soft);margin-bottom:8px;}
.v-metric-value{font-family:var(--ff-head);font-size:22px;font-weight:600;color:var(--ink);}

.v-place-card{background:var(--white);border:1px solid var(--border);border-radius:14px;overflow:hidden;margin-bottom:14px;transition:box-shadow .2s;}
.v-place-card:hover{box-shadow:var(--shadow);}
.v-place-img{width:100%;height:150px;background-size:cover;background-position:center;}
.v-place-info{padding:14px 16px;}
.v-place-name{font-weight:600;font-size:15px;color:var(--ink);margin-bottom:4px;}
.v-place-addr{font-size:12px;color:var(--ink-soft);line-height:1.4;}

.v-divider{height:1px;background:var(--border);margin:8px 0 20px;}
.stSpinner>div{border-top-color:var(--accent)!important;}
div[data-testid="stSuccess"]{background:#F0FAF4!important;border:1px solid #86EFAC!important;border-radius:12px!important;border-left:4px solid #22C55E!important;}
div[data-testid="stWarning"]{border-radius:12px!important;border-left:4px solid #F59E0B!important;}

.v-footer{background:var(--ink);color:rgba(255,255,255,0.45);text-align:center;padding:28px 20px;font-size:13px;margin-top:64px;line-height:1.8;}
.v-footer strong{color:rgba(255,255,255,0.8);font-weight:500;}

@media (max-width:900px){
  :root{--nav-h:60px;}
  .v-nav{padding:0 20px;}
  .v-nav-links .hide-tab{display:none;}
  .v-hero{height:420px;}
  .v-hero-text{padding:0 24px 36px;}
  .v-hero-text h1{font-size:38px;letter-spacing:-0.8px;}
  .v-hero-text p{font-size:14px;}
  .v-search-wrap{padding:0 16px;margin-top:-36px;}
  .v-search-panel{padding:18px 18px 14px;border-radius:16px;}
  .v-section{padding:28px 16px 12px;}
  .v-overview{margin:0 16px 8px;padding:14px 16px;}
  .v-overview-item{min-width:80px;padding:0 10px;}
  .v-hotel-img{width:160px;}
  .v-hotel-body{padding:16px 18px;}
  .v-hotel-name{font-size:16px;}
  .v-links-grid{grid-template-columns:repeat(2,1fr);}
  .v-dots{right:20px;}
}

@media (max-width:600px){
  :root{--nav-h:56px;}
  .v-nav{padding:0 14px;}
  .v-nav-links{display:none;}
  .v-mobile-menu-btn{display:flex!important;}
  .v-hero{height:340px;}
  .v-hero-text{padding:0 16px 28px;}
  .v-hero-text h1{font-size:28px;letter-spacing:-0.5px;margin-bottom:10px;}
  .v-hero-text p{font-size:13px;max-width:100%;}
  .v-hero-tag{font-size:10px;padding:5px 12px;}
  .v-search-wrap{padding:0 10px;margin-top:-28px;}
  .v-search-panel{padding:14px 14px 12px;border-radius:14px;}
  .v-search-eyebrow{font-size:12px;margin-bottom:12px;}
  .v-section{padding:22px 10px 10px;}
  .v-section-head h2{font-size:21px;}
  .v-overview{margin:0 10px 8px;padding:12px 14px;gap:8px;}
  .v-overview-item{min-width:calc(50% - 16px);padding:0 8px;border-right:none;border-bottom:1px solid rgba(255,255,255,0.11);padding-bottom:8px;}
  .v-overview-item:nth-child(odd){border-right:1px solid rgba(255,255,255,0.11)!important;}
  .v-overview-item:last-child,.v-overview-item:nth-last-child(2):nth-child(odd){border-bottom:none!important;}
  .v-ov-value{font-size:13px;}
  .v-hotel{flex-direction:column;}
  .v-hotel-img{width:100%;height:180px;}
  .v-hotel-body{padding:14px 16px;}
  .v-hotel-name{font-size:16px;}
  .v-hotel-footer{flex-direction:column;align-items:flex-start;}
  .v-book-btn{width:100%;text-align:center;}
  .v-links-grid{grid-template-columns:repeat(2,1fr);gap:8px;}
  .v-link-card{padding:12px 8px;font-size:12px;}
  .v-dots{display:none;}
  div[data-baseweb="tab-list"]{overflow-x:auto!important;flex-wrap:nowrap!important;}
  button[data-baseweb="tab"]{font-size:12px!important;padding:7px 12px!important;white-space:nowrap!important;}
  .v-footer{font-size:12px;padding:20px 14px;}
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────

st.markdown("""
<div class="v-nav">
  <div class="v-logo">✈ Voyag<span>r</span></div>
  <div class="v-nav-links">
    <a href="#" class="hide-tab">Explore</a>
    <a href="#" class="hide-tab">Hotels</a>
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

    st.markdown("<div style='padding:20px 32px 0;'>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["  🗺️  Itinerary  ", "  🛣️  Route Places  ", "  🏨  Hotels  ", "  📊  Summary  "]
    )

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

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Attractions Along Your Route")
        st.markdown("<div class='v-divider'></div>", unsafe_allow_html=True)
        if not route_places:
            st.warning("⚠️ No attractions found along this route. This may be due to API limits or an unsupported route. Your itinerary above still covers key stops!")
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
  Built with Gemini AI &nbsp;·&nbsp; Hotel data via Booking.com &nbsp;·&nbsp;
  Maps by Geoapify &nbsp;·&nbsp; Bot powered by make.com<br><br>
  © 2026 Voyagr · All rights reserved
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# FLOATING CHAT BUBBLE
# ─────────────────────────────────────────

import streamlit.components.v1 as components

_dest = destination if (generate and destination) else "your destination"

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:transparent;font-family:'DM Sans',system-ui,sans-serif;}}
</style>
<script>
(function(){{
  const WEBHOOK = "{MAKE_WEBHOOK_URL}";
  const DEST    = "{_dest}";

  const style = document.createElement('style');
  style.textContent = `
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:wght@600;700&display=swap');
    #voy-fab {{
      position:fixed; bottom:20px; right:16px; z-index:99999;
      width:56px; height:56px; border-radius:50%;
      background:#1A1714; color:white; font-size:22px;
      display:flex; align-items:center; justify-content:center;
      cursor:pointer;
      box-shadow:0 6px 28px rgba(26,23,20,0.38);
      border:none; outline:none;
      transition:transform .25s cubic-bezier(.34,1.56,.64,1), background .2s;
    }}
    #voy-fab:hover  {{ transform:scale(1.1); background:#C4622D; }}
    #voy-fab.open   {{ background:#C4622D; }}
    #voy-badge {{
      position:absolute; top:-2px; right:-2px;
      width:18px; height:18px; background:#ef4444;
      border-radius:50%; font-size:10px; font-weight:700;
      color:white; display:none; align-items:center; justify-content:center;
      border:2px solid white;
    }}
    #voy-badge.show {{ display:flex; }}
    #voy-chatwin {{
      position:fixed; bottom:86px; right:16px; z-index:99998;
      width:min(370px, calc(100vw - 24px));
      height:min(570px, calc(100dvh - 110px));
      background:#FAF8F5; border-radius:20px;
      box-shadow:0 14px 60px rgba(26,23,20,0.24);
      border:1px solid #E8E4DE;
      display:flex; flex-direction:column; overflow:hidden;
      opacity:0; transform:translateY(24px) scale(0.94);
      pointer-events:none;
      transition:opacity .28s ease, transform .3s cubic-bezier(.34,1.56,.64,1);
    }}
    #voy-chatwin.open {{ opacity:1; transform:translateY(0) scale(1); pointer-events:all; }}
    @media (max-width:600px) {{
      #voy-chatwin {{
        bottom:0; right:0; left:0;
        width:100%; height:min(100dvh, 100vh);
        border-radius:20px 20px 0 0;
        transform:translateY(100%);
      }}
      #voy-chatwin.open {{ transform:translateY(0); }}
      #voy-fab {{ bottom:16px; right:14px; width:52px; height:52px; font-size:20px; }}
    }}
    .vt {{ background:#1A1714; padding:14px 16px; display:flex; align-items:center; justify-content:space-between; flex-shrink:0; }}
    .vt-l {{ display:flex; align-items:center; gap:10px; }}
    .vt-av {{ width:38px; height:38px; border-radius:50%; background:#C4622D; display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0; }}
    .vt-name {{ font-size:15px; font-weight:600; color:white; font-family:'Playfair Display',serif; }}
    .vt-st {{ font-size:11px; color:rgba(255,255,255,.5); display:flex; align-items:center; gap:5px; margin-top:1px; }}
    .vt-st::before {{ content:""; width:6px; height:6px; background:#4ade80; border-radius:50%; display:inline-block; animation:vblink 2s infinite; }}
    @keyframes vblink{{ 0%,100%{{opacity:1;}} 50%{{opacity:.35;}} }}
    .vt-x {{ background:rgba(255,255,255,.1); border:none; color:white; width:30px; height:30px; border-radius:50%; cursor:pointer; font-size:15px; display:flex; align-items:center; justify-content:center; transition:background .2s; flex-shrink:0; }}
    .vt-x:hover {{ background:rgba(255,255,255,.22); }}
    .vt-safe {{ padding-top:env(safe-area-inset-top, 0); }}
    #voy-chips-bar {{ padding:10px 14px 6px; background:#fff; border-bottom:1px solid #E8E4DE; flex-shrink:0; }}
    .vc-label {{ font-size:10px; font-weight:700; letter-spacing:.7px; text-transform:uppercase; color:#5A5550; margin-bottom:6px; }}
    .vc-row {{ display:flex; flex-wrap:wrap; gap:6px; }}
    .vc {{ background:#FAF8F5; border:1px solid #E8E4DE; padding:5px 11px; border-radius:99px; font-size:11.5px; color:#1A1714; cursor:pointer; transition:all .15s; white-space:nowrap; }}
    .vc:hover,.vc:active {{ background:#C4622D; color:white; border-color:#C4622D; }}
    #voy-msgs {{ flex:1; overflow-y:auto; padding:14px 12px; display:flex; flex-direction:column; gap:11px; scroll-behavior:smooth; -webkit-overflow-scrolling:touch; }}
    #voy-msgs::-webkit-scrollbar {{ width:3px; }}
    #voy-msgs::-webkit-scrollbar-thumb {{ background:#E8E4DE; border-radius:99px; }}
    .ve {{ flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:20px; }}
    .ve-i {{ font-size:44px; margin-bottom:12px; }}
    .ve h4 {{ font-size:15px; font-weight:600; color:#1A1714; margin-bottom:6px; font-family:'Playfair Display',serif; }}
    .ve p  {{ font-size:12.5px; color:#5A5550; line-height:1.6; }}
    .vr {{ display:flex; align-items:flex-end; gap:8px; }}
    .vr.u {{ flex-direction:row-reverse; }}
    .vi {{ width:26px; height:26px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; flex-shrink:0; }}
    .vi.ai {{ background:#C4622D; color:white; }}
    .vi.hu {{ background:#1A1714; color:white; }}
    .vb {{ max-width:78%; padding:9px 13px; border-radius:15px; font-size:13.5px; line-height:1.6; word-wrap:break-word; }}
    .vb.ai {{ background:white; color:#1A1714; border:1px solid #E8E4DE; border-bottom-left-radius:3px; box-shadow:0 1px 4px rgba(0,0,0,.06); }}
    .vb.u  {{ background:#1A1714; color:white; border-bottom-right-radius:3px; }}
    .vbt {{ font-size:10px; color:#9a9590; margin-top:3px; }}
    .vr.u .vbt {{ text-align:right; }}
    .vdots {{ display:flex; align-items:center; gap:4px; padding:6px 10px; }}
    .vdots span {{ width:6px; height:6px; background:#9a9590; border-radius:50%; animation:vdt 1.2s ease-in-out infinite; }}
    .vdots span:nth-child(2) {{ animation-delay:.2s; }}
    .vdots span:nth-child(3) {{ animation-delay:.4s; }}
    @keyframes vdt {{ 0%,60%,100%{{transform:translateY(0);opacity:.35;}} 30%{{transform:translateY(-5px);opacity:1;}} }}
    #voy-bar {{
      padding:10px 12px;
      padding-bottom:max(10px, env(safe-area-inset-bottom, 10px));
      background:white; border-top:1px solid #E8E4DE;
      flex-shrink:0; display:flex; gap:8px; align-items:center;
    }}
    #voy-in {{
      flex:1; border:1px solid #E8E4DE; border-radius:99px;
      padding:10px 15px; font-size:14px; outline:none;
      background:#FAF8F5; color:#1A1714;
      -webkit-appearance:none; appearance:none;
      transition:border-color .2s; font-family:'DM Sans',sans-serif;
      min-height:44px;
    }}
    #voy-in:focus {{ border-color:#C4622D; background:white; }}
    #voy-in::placeholder {{ color:#b0ada9; }}
    #voy-go {{
      width:40px; height:40px; border-radius:50%; background:#1A1714;
      color:white; border:none; cursor:pointer; font-size:15px;
      display:flex; align-items:center; justify-content:center; flex-shrink:0;
      transition:background .2s, transform .15s; -webkit-tap-highlight-color:transparent;
    }}
    #voy-go:hover {{ background:#C4622D; transform:scale(1.08); }}
    #voy-go:disabled {{ background:#ccc; cursor:not-allowed; transform:none; }}
    #voy-clr {{ background:none; border:none; color:#b0ada9; font-size:16px; cursor:pointer; padding:0 2px; transition:color .15s; flex-shrink:0; -webkit-tap-highlight-color:transparent; }}
    #voy-clr:hover {{ color:#ef4444; }}
    @media (min-width:601px) and (max-width:900px) {{
      #voy-chatwin {{
        width:min(340px, calc(100vw - 20px));
        height:min(520px, calc(100dvh - 100px));
        right:14px; bottom:82px;
      }}
    }}
  `;
  parent.document.head.appendChild(style);

  const wrap = parent.document.createElement('div');
  wrap.id = 'voy-root';
  wrap.innerHTML = `
    <button id="voy-fab" onclick="voyToggle()" title="Chat with Voyagr AI">
      ✈️<span id="voy-badge"></span>
    </button>
    <div id="voy-chatwin">
      <div class="vt vt-safe">
        <div class="vt-l">
          <div class="vt-av">✈️</div>
          <div>
            <div class="vt-name">Voyagr AI</div>
            <div class="vt-st">Online · Travel Assistant</div>
          </div>
        </div>
        <button class="vt-x" onclick="voyToggle()">✕</button>
      </div>
      <div id="voy-chips-bar">
        <div class="vc-label">💡 Quick questions</div>
        <div class="vc-row" id="voy-cr"></div>
      </div>
      <div id="voy-msgs">
        <div class="ve">
          <div class="ve-i">🌍</div>
          <h4>Your travel assistant is ready</h4>
          <p>Ask anything — destinations, visa, packing, food, safety, hidden gems.</p>
        </div>
      </div>
      <div id="voy-bar">
        <button id="voy-clr" onclick="voyClr()" title="Clear">🗑️</button>
        <input id="voy-in" type="text" placeholder="Ask about your trip..."
               onkeydown="if(event.key==='Enter')voyGo()" autocomplete="off"/>
        <button id="voy-go" onclick="voyGo()">➤</button>
      </div>
    </div>
  `;
  parent.document.body.appendChild(wrap);

  const pd = parent.document;
  let isOpen=false, msgs=[], typing=false, unread=0, typEl=null;

  const chips = [
    `Best time to visit ${{DEST}}?`,
    `What to pack for ${{DEST}}?`,
    `Local food in ${{DEST}}`,
    `Safety tips for ${{DEST}}`,
    `Hidden gems in ${{DEST}}`,
    `Visa info for ${{DEST}}`,
  ];
  chips.forEach(c => {{
    const b = pd.createElement('button');
    b.className='vc'; b.textContent=c;
    b.onclick = () => send(c);
    pd.getElementById('voy-cr').appendChild(b);
  }});

  parent.addEventListener('click', function(e){{
    if(isOpen && !e.target.closest('#voy-chatwin') && !e.target.closest('#voy-fab')){{
      voyClose();
    }}
  }}, true);

  parent.voyToggle = function(){{ isOpen ? voyClose() : voyOpen(); }};
  function voyOpen(){{
    isOpen=true;
    pd.getElementById('voy-chatwin').classList.add('open');
    pd.getElementById('voy-fab').classList.add('open');
    unread=0; badge();
    parent.document.body.style.overflow='hidden';
    setTimeout(()=>pd.getElementById('voy-in').focus(), 300);
  }}
  function voyClose(){{
    isOpen=false;
    pd.getElementById('voy-chatwin').classList.remove('open');
    pd.getElementById('voy-fab').classList.remove('open');
    parent.document.body.style.overflow='';
  }}

  parent.voyClr = function(){{ msgs=[]; render(); pd.getElementById('voy-chips-bar').style.display=''; }};
  parent.voyGo  = function(){{
    const el=pd.getElementById('voy-in'), t=el.value.trim();
    if(!t||typing) return; el.value=''; send(t);
  }};

  function send(text){{
    msgs.push({{r:'u', t:text, ts:ts()}});
    pd.getElementById('voy-chips-bar').style.display='none';
    render(); showDots();
    pd.getElementById('voy-go').disabled=true;
    fetch(WEBHOOK, {{
      method:'POST',
      headers:{{'Content-Type':'application/json'}},
      body:JSON.stringify({{message:text}})
    }})
    .then(r=>r.text())
    .then(rep=>{{
      hideDots();
      msgs.push({{r:'ai', t:rep.trim()||"Sorry, no response. Please try again.", ts:ts()}});
      render();
      if(!isOpen){{unread++;badge();}}
    }})
    .catch(()=>{{
      hideDots();
      msgs.push({{r:'ai', t:'⚠️ Connection error. Please try again.', ts:ts()}});
      render();
    }})
    .finally(()=>{{pd.getElementById('voy-go').disabled=false;}});
  }}

  function render(){{
    const box=pd.getElementById('voy-msgs');
    box.innerHTML='';
    if(!msgs.length){{
      box.innerHTML=`<div class="ve"><div class="ve-i">🌍</div><h4>Your travel assistant is ready</h4><p>Ask anything — destinations, visa, packing, food, safety, hidden gems.</p></div>`;
      return;
    }}
    msgs.forEach(m=>{{
      const row=pd.createElement('div');
      row.className='vr'+(m.r==='u'?' u':'');
      const ic = m.r==='u'
        ? '<div class="vi hu">👤</div>'
        : '<div class="vi ai">✈️</div>';
      const bc = m.r==='u'?'u':'ai';
      const lb = m.r==='u'?'You':'Voyagr AI';
      row.innerHTML=`${{ic}}<div><div class="vb ${{bc}}">${{m.t}}</div><div class="vbt">${{lb}} · ${{m.ts}}</div></div>`;
      if(typEl) box.insertBefore(row,typEl);
      else box.appendChild(row);
    }});
    scroll();
  }}

  function showDots(){{
    typing=true;
    const box=pd.getElementById('voy-msgs');
    typEl=pd.createElement('div');
    typEl.className='vr';
    typEl.innerHTML='<div class="vi ai">✈️</div><div class="vb ai"><div class="vdots"><span></span><span></span><span></span></div></div>';
    box.appendChild(typEl); scroll();
  }}
  function hideDots(){{ typing=false; if(typEl){{typEl.remove();typEl=null;}} }}
  function scroll(){{
    const b=pd.getElementById('voy-msgs');
    setTimeout(()=>b.scrollTop=b.scrollHeight, 60);
  }}
  function ts(){{
    return new Date().toLocaleTimeString([],{{hour:'2-digit',minute:'2-digit'}});
  }}
  function badge(){{
    const b=pd.getElementById('voy-badge');
    if(unread>0){{b.textContent=unread>9?'9+':unread;b.classList.add('show');}}
    else b.classList.remove('show');
  }}

}})();
</script>
</head>
<body></body>
</html>
""", height=0, scrolling=False)