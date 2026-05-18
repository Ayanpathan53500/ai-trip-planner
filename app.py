# import os
# import streamlit as st
# import google.generativeai as genai
# from tavily import TavilyClient
# import os
# import streamlit as st
# from dotenv import load_dotenv
# from google import genai
# from tavily import TavilyClient
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet



# # API setup
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# client = genai.Client(api_key=GOOGLE_API_KEY)
# tavily = TavilyClient(api_key=TAVILY_API_KEY)
# # genai.configure(api_key=GOOGLE_API_KEY)
# # tavily = TavilyClient(api_key=TAVILY_API_KEY)

# # model = genai.GenerativeModel("gemini-2.5-flash")

# # -------- FUNCTIONS -------- #

# def get_route_places(source, destination):
#     res = tavily.search(
#         f"best places to visit between {source} and {destination}",
#         max_results=5
#     )
#     return res["results"]

# def get_hotels(destination):
#     res = tavily.search(
#         f"best hotels in {destination} with price and booking",
#         max_results=6
#     )
#     return res["results"]


# def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places):
#     names = [p["title"] for p in route_places]

#     prompt = f"""
#     Create a complete travel plan:

#     From: {source}
#     To: {destination}
#     Days: {days}
#     Budget: {budget_min} to {budget_max} INR
#     Travel Mode: {travel_mode}

#     Include:
#     - Route journey plan
#     - Places between route: {', '.join(names)}
#     - Day-wise itinerary
#     - Budget breakdown (transport + hotel + food)
#     - Travel tips
#     """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text

# # def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places):
# #     names = [p["title"] for p in route_places]

# #     prompt = f"""
# #     Create a complete travel plan:

# #     From: {source}
# #     To: {destination}
# #     Days: {days}
# #     Budget: {budget_min} to {budget_max} INR
# #     Travel Mode: {travel_mode}

# #     Include:
# #     - Route journey plan
# #     - Places between route: {', '.join(names)}
# #     - Day-wise itinerary
# #     - Budget breakdown (transport + hotel + food)
# #     - Travel tips

# #     Keep it structured.
# #     """

# #     return model.generate_content(prompt).text


# # -------- UI -------- #

# st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")

# st.markdown("<h1 style='text-align:center;'>🌍 AI Travel Planner Pro</h1>", unsafe_allow_html=True)

# # Sidebar Inputs
# st.sidebar.header("✈️ Plan Your Trip")

# source = st.sidebar.text_input("📍 From (Starting City)")
# destination = st.sidebar.text_input("🏁 To (Destination City)")
# days = st.sidebar.slider("📅 Days", 1, 15, 3)

# budget_min = st.sidebar.number_input("💰 Min Budget (₹)", value=5000)
# budget_max = st.sidebar.number_input("💰 Max Budget (₹)", value=20000)

# travel_mode = st.sidebar.selectbox(
#     "🚆 Travel Mode",
#     ["Bus", "Train", "Flight", "Car"]
# )

# generate = st.sidebar.button("✨ Generate Plan")

# # -------- MAIN -------- #

# if generate and source and destination:

#     with st.spinner("🔍 Planning your smart trip..."):

#         route_places = get_route_places(source, destination)
#         hotels = get_hotels(destination)
#         plan = generate_plan(
#             source, destination, days,
#             budget_min, budget_max,
#             travel_mode, route_places
#         )

#     st.success("✅ Trip Ready!")

#     # -------- TABS -------- #
#     tab1, tab2, tab3, tab4 = st.tabs(
#         ["🗺️ Plan", "🛣️ Route Places", "🏨 Hotels", "📊 Summary"]
#     )

#     # -------- PLAN -------- #
#     with tab1:
#         st.subheader("📅 AI Itinerary")
#         for line in plan.split("\n"):
#             if line.strip():
#                 st.markdown(f"- {line}")

#     # -------- ROUTE PLACES -------- #
#     with tab2:
#         st.subheader("🛣️ Places Between Your Route")

#         for p in route_places:
#             st.markdown(f"### 📍 {p['title']}")
#             if "image" in p:
#                 st.image(p["image"], use_container_width=True)
#             st.write(p.get("content", ""))

#     # -------- HOTELS -------- #
#     with tab3:
#         st.subheader("🏨 Hotels + Booking")

#         for h in hotels:
#             st.markdown(f"### 🏨 {h['title']}")
#             if "image" in h:
#                 st.image(h["image"], use_container_width=True)
#             st.write(h.get("content", ""))

#         st.markdown("### 🔗 Booking Platforms")
#         st.markdown("""
#         - 🛏️ Hotels: [MakeMyTrip](https://www.makemytrip.com), [Booking.com](https://www.booking.com)
#         - 🚆 Train: [IRCTC](https://www.irctc.co.in)
#         - 🚌 Bus: [RedBus](https://www.redbus.in)
#         - ✈️ Flights: [Goibibo](https://www.goibibo.com)
#         """)

#     # -------- SUMMARY -------- #
#     with tab4:
#         st.subheader("📊 Trip Summary")

#         st.markdown(f"""
#         - 📍 From: {source}  
#         - 🏁 To: {destination}  
#         - 📅 Days: {days}  
#         - 💰 Budget: ₹{budget_min} - ₹{budget_max}  
#         - 🚆 Travel Mode: {travel_mode}  
#         """)

# else:
#     st.info("👈 Fill details from sidebar and click Generate")

# --------------------------------------------------------------------------------------------------------------------------------------------
# import os
# import streamlit as st
# from dotenv import load_dotenv
# from google import genai
# from tavily import TavilyClient
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet



# # API setup
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# client = genai.Client(api_key=GOOGLE_API_KEY)
# tavily = TavilyClient(api_key=TAVILY_API_KEY)
# # genai.configure(api_key=GOOGLE_API_KEY)
# # tavily = TavilyClient(api_key=TAVILY_API_KEY)

# # model = genai.GenerativeModel("gemini-2.5-flash")

# # -------- FUNCTIONS -------- #

# def get_route_places(source, destination):
#     res = tavily.search(
#         f"best places to visit between {source} and {destination}",
#         max_results=5
#     )
#     return res["results"]

# def get_hotels(destination):
#     try:
#         res = tavily.search(
#             f"top hotels in {destination} with name rating price",
#             max_results=10
#         )

#         hotels = []

#         for r in res["results"]:

#             title = r.get("title", "")
#             desc = r.get("content", "")

#             # ❌ Skip useless results
#             if any(x in title.lower() for x in ["best", "top", "guide", "list"]):
#                 continue

#             # ✅ Extract only meaningful hotel-like entries
#             if len(title) < 5:
#                 continue

#             import random

#             hotels.append({
#                 "name": title.strip(),
#                 "desc": desc.strip(),
#                 "image": r.get("image"),
#                 "rating": round(random.uniform(3.5, 5.0), 1),
#                 "price": random.randint(2000, 8000),
#                 "url": "https://www.booking.com"
#             })

#         return hotels[:6]

#     except Exception as e:
#         print("Hotel error:", e)
#         return []
# # def get_hotels(destination):
# #     res = tavily.search(
# #         f"best hotels in {destination} with price and booking",
# #         max_results=6
# #     )
# #     return res["results"]


# def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places):
#     names = [p["title"] for p in route_places]

#     prompt = f"""
#     Create a complete travel plan:

#     From: {source}
#     To: {destination}
#     Days: {days}
#     Budget: {budget_min} to {budget_max} INR
#     Travel Mode: {travel_mode}

#     Include:
#     - Route journey plan
#     - Places between route: {', '.join(names)}
#     - Day-wise itinerary
#     - Budget breakdown (transport + hotel + food)
#     - Travel tips
#     """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text



# # -------- UI -------- #

# st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")

# st.markdown("<h1 style='text-align:center;'>🌍 AI Travel Planner Pro</h1>", unsafe_allow_html=True)

# # Sidebar Inputs
# st.sidebar.header("✈️ Plan Your Trip")

# source = st.sidebar.text_input("📍 From (Starting City)")
# destination = st.sidebar.text_input("🏁 To (Destination City)")
# days = st.sidebar.slider("📅 Days", 1, 15, 3)

# budget_min = st.sidebar.number_input("💰 Min Budget (₹)", value=5000)
# budget_max = st.sidebar.number_input("💰 Max Budget (₹)", value=20000)

# travel_mode = st.sidebar.selectbox(
#     "🚆 Travel Mode",
#     ["Bus", "Train", "Flight", "Car"]
# )

# generate = st.sidebar.button("✨ Generate Plan")

# # -------- MAIN -------- #

# if generate and source and destination:

#     with st.spinner("🔍 Planning your smart trip..."):

#         route_places = get_route_places(source, destination)
#         hotels = get_hotels(destination)
#         plan = generate_plan(
#             source, destination, days,
#             budget_min, budget_max,
#             travel_mode, route_places
#         )

#     st.success("✅ Trip Ready!")
#     st.markdown(f"""
#     ### ✈️ Trip Overview  
#     **From:** {source} → **To:** {destination}  
#     📅 {days} Days | 💰 ₹{budget_min}-{budget_max} | 🚆 {travel_mode}
#     """)

#     # -------- TABS -------- #
#     tab1, tab2, tab3, tab4 = st.tabs(
#         ["🗺️ Plan", "🛣️ Route Places", "🏨 Hotels", "📊 Summary"]
#     )

#     # -------- PLAN -------- #
#     with tab1:
#         st.subheader("📅 AI Itinerary")
#         for line in plan.split("\n"):
#             if line.strip():
#                 st.markdown(f"- {line}")


#     # -------- ROUTE PLACES -------- #
#     with tab2:
#         st.subheader("🛣️ Places Between Your Route")

#         cols = st.columns(3)

#         for i, p in enumerate(route_places):
#             with cols[i % 3]:
#                 st.markdown(f"""
#                 <div style="background:#f9fafc;padding:10px;border-radius:10px;
#                 box-shadow:0px 2px 8px rgba(0,0,0,0.1);">
#                 <b>📍 {p['title']}</b>
#                 </div>
#                 """, unsafe_allow_html=True)

#                 if "image" in p:
#                     st.image(p["image"], use_container_width=True)

#                 st.caption(p.get("content", "")[:120] + "...")

#     # -------- HOTELS -------- #
#     with tab3:
#         st.subheader("🏨 Hotel Suggestions")

#         if not hotels:
#             st.warning("⚠️ No hotels found. Try another city.")
#         else:
#             for h in hotels:

#                 col1, col2 = st.columns([1, 2])

#                 # IMAGE
#                 with col1:
#                     if h.get("image"):
#                         st.image(h["image"], use_container_width=True)
#                     else:
#                         st.image("https://via.placeholder.com/300x200")

#                 # DETAILS
#                 with col2:
#                     st.markdown(f"""
#                     ### 🏨 {h['name']}

#                     {h['desc'][:120]}...

#                     ⭐ **Rating:** {h['rating']} / 5  
#                     💰 **Price:** ₹{h['price']} / night  
#                     """)

#                     st.markdown(f"[🔘 Book Now]({h['url']})")

#                 st.markdown("---")
#                 st.markdown("### 🔗 Booking Platforms")
#                 st.markdown("""
#                     - 🛏️ Hotels: [MakeMyTrip](https://www.makemytrip.com), [Booking.com](https://www.booking.com)
#                     - 🚆 Train: [IRCTC](https://www.irctc.co.in)
#                     - 🚌 Bus: [RedBus](https://www.redbus.in)
#                     - ✈️ Flights: [Goibibo](https://www.goibibo.com)
#                     """)

    
#     # with tab3:
#     #     st.subheader("🏨 Recommended Hotels")

#     #     cols = st.columns(3)

#     #     for i, h in enumerate(hotels):
#     #         with cols[i % 3]:
#     #             st.markdown(f"""
#     #             <div style="background:white;padding:12px;border-radius:12px;
#     #             box-shadow:0px 4px 12px rgba(0,0,0,0.15);">
#     #             <h4>🏨 {h['title']}</h4>
#     #             </div>
#     #             """, unsafe_allow_html=True)

#     #             if "image" in h:
#     #                 st.image(h["image"], use_container_width=True)

#     #             st.caption(h.get("content", "")[:120] + "...")

#     #     st.markdown("### 🔗 Booking Platforms")
#     #     st.markdown("""
#     #         - 🛏️ Hotels: [MakeMyTrip](https://www.makemytrip.com), [Booking.com](https://www.booking.com)
#     #         - 🚆 Train: [IRCTC](https://www.irctc.co.in)
#     #         - 🚌 Bus: [RedBus](https://www.redbus.in)
#     #         - ✈️ Flights: [Goibibo](https://www.goibibo.com)
#     #         """)



#     # -------- SUMMARY -------- #
#     with tab4:
#         st.subheader("📊 Trip Summary")

#         st.markdown(f"""
#         - 📍 From: {source}  
#         - 🏁 To: {destination}  
#         - 📅 Days: {days}  
#         - 💰 Budget: ₹{budget_min} - ₹{budget_max}  
#         - 🚆 Travel Mode: {travel_mode}  
#         """)

# else:
#     st.info("👈 Fill details from sidebar and click Generate")

# -------------------------------------------------------------------------------------------------------------------------------------------------------


# import os
# import streamlit as st
# from dotenv import load_dotenv
# from google import genai
# from tavily import TavilyClient
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet
# import requests


# # API setup
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# client = genai.Client(api_key=GOOGLE_API_KEY)
# tavily = TavilyClient(api_key=TAVILY_API_KEY)
# # genai.configure(api_key=GOOGLE_API_KEY)
# # tavily = TavilyClient(api_key=TAVILY_API_KEY)

# # model = genai.GenerativeModel("gemini-2.5-flash")

# # -------- FUNCTIONS -------- #


# RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# headers = {
#     "X-RapidAPI-Key": RAPIDAPI_KEY,
#     "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
# }


# def get_destination_id(city):
#     try:
#         url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

#         params = {
#             "name": city,
#             "locale": "en-gb"
#         }

#         res = requests.get(url, headers=headers, params=params, timeout=10)

#         if res.status_code != 200:
#             print("Location API error:", res.status_code)
#             return None, None

#         data = res.json()

#         if not data:
#             return None, None

#         return data[0]["dest_id"], data[0]["dest_type"]

#     except Exception as e:
#         print("Destination error:", e)
#         return None, None


# def get_route_places(source, destination):
#     res = tavily.search(
#         f"best places to visit between {source} and {destination}",
#         max_results=5
#     )
#     return res["results"]

# def get_hotels(destination):
#     try:
#         dest_id, dest_type = get_destination_id(destination)

#         if not dest_id:
#             print("❌ No destination found")
#             return []

#         url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

#         params = {
#         "dest_id": dest_id,
#         "dest_type": dest_type,   # dynamic (VERY IMPORTANT)
        
#         "checkin_date": "2026-05-01",
#         "checkout_date": "2026-05-03",
        
#         "adults_number": 2,
#         "room_number": 1,

#         "order_by": "popularity",

#         "locale": "en-gb",
#         "units": "metric",

#         # ✅ REQUIRED FIX
#         "filter_by_currency": "INR"
#         }
#         res = requests.get(url, headers=headers, params=params, timeout=15)

#         if res.status_code != 200:
#             print("❌ Hotel API error:", res.status_code)
#             print(res.text)
#             return []

#         data = res.json()

#         hotels = []

#         for h in data.get("result", [])[:10]:

#             try:
#                 hotels.append({
#                     "name": h.get("hotel_name"),
#                     "price": h.get("min_total_price"),
#                     "rating": h.get("review_score"),
#                     "review": h.get("review_score_word"),
#                     "image": h.get("main_photo_url"),
#                     "address": h.get("address"),
#                     "distance": h.get("distance_to_cc"),
#                     "lat": h.get("latitude"),
#                     "lon": h.get("longitude"),
#                     "url": h.get("url")
#                 })
#             except:
#                 continue

#         return hotels

#     except Exception as e:
#         print("Hotel API crash:", e)
#         return []

#     except Exception as e:
#         print("Hotel error:", e)
#         return []


# def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places):
#     names = [p["title"] for p in route_places]

#     prompt = f"""
#     Create a complete travel plan:

#     From: {source}
#     To: {destination}
#     Days: {days}
#     Budget: {budget_min} to {budget_max} INR
#     Travel Mode: {travel_mode}

#     Include:
#     - Route journey plan
#     - Places between route: {', '.join(names)}
#     - Day-wise itinerary
#     - Budget breakdown (transport + hotel + food)
#     - Travel tips
#     """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text



# # -------- UI -------- #

# st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")

# st.markdown("<h1 style='text-align:center;'>🌍 AI Travel Planner Pro</h1>", unsafe_allow_html=True)

# # Sidebar Inputs
# st.sidebar.header("✈️ Plan Your Trip")

# source = st.sidebar.text_input("📍 From (Starting City)")
# destination = st.sidebar.text_input("🏁 To (Destination City)")
# days = st.sidebar.slider("📅 Days", 1, 15, 3)

# budget_min = st.sidebar.number_input("💰 Min Budget (₹)", value=5000)
# budget_max = st.sidebar.number_input("💰 Max Budget (₹)", value=20000)

# travel_mode = st.sidebar.selectbox(
#     "🚆 Travel Mode",
#     ["Bus", "Train", "Flight", "Car"]
# )

# generate = st.sidebar.button("✨ Generate Plan")

# # -------- MAIN -------- #

# if generate and source and destination:

#     with st.spinner("🔍 Planning your smart trip..."):

#         route_places = get_route_places(source, destination)
#         hotels = get_hotels(destination)
#         plan = generate_plan(
#             source, destination, days,
#             budget_min, budget_max,
#             travel_mode, route_places
#         )

#     st.success("✅ Trip Ready!")
#     st.markdown(f"""
#     ### ✈️ Trip Overview  
#     **From:** {source} → **To:** {destination}  
#     📅 {days} Days | 💰 ₹{budget_min}-{budget_max} | 🚆 {travel_mode}
#     """)

#     # -------- TABS -------- #
#     tab1, tab2, tab3, tab4 = st.tabs(
#         ["🗺️ Plan", "🛣️ Route Places", "🏨 Hotels", "📊 Summary"]
#     )

#     # -------- PLAN -------- #
#     with tab1:
#         st.subheader("📅 AI Itinerary")
#         for line in plan.split("\n"):
#             if line.strip():
#                 st.markdown(f"- {line}")

#         st.markdown("### 🔗 Booking Platforms")
#         st.markdown("""
#                     - 🛏️ Hotels: [MakeMyTrip](https://www.makemytrip.com), [Booking.com](https://www.booking.com)
#                     - 🚆 Train: [IRCTC](https://www.irctc.co.in)
#                     - 🚌 Bus: [RedBus](https://www.redbus.in)
#                     - ✈️ Flights: [Goibibo](https://www.goibibo.com)
#                             """)
#     # -------- ROUTE PLACES -------- #
#     with tab2:
#         st.subheader("🛣️ Places Between Your Route")

#         cols = st.columns(3)

#         for i, p in enumerate(route_places):
#             with cols[i % 3]:
#                 st.markdown(f"""
#                 <div style="background:#f9fafc;padding:10px;border-radius:10px;
#                 box-shadow:0px 2px 8px rgba(0,0,0,0.1);">
#                 <b>📍 {p['title']}</b>
#                 </div>
#                 """, unsafe_allow_html=True)

#                 if "image" in p:
#                     st.image(p["image"], use_container_width=True)

#                 st.caption(p.get("content", "")[:120] + "...")

#     # -------- HOTELS -------- #
#     with tab3:
#         st.subheader("🏨 Real Hotels (Live Data)")

#         if not hotels:
#             st.warning("⚠️ No hotels found")
#         else:
#             for h in hotels:

#                 col1, col2 = st.columns([1, 2])

#                 with col1:
#                     if h["image"]:
#                         st.image(h["image"], use_container_width=True)

#                 with col2:
#                     st.markdown(f"""
#                     ### 🏨 {h['name']}

#                     ⭐ {h['rating']} / 10 ({h['review']})  
#                     📍 {h['address']}  
#                     📏 {h['distance']} from center  

#                     💰 **₹{h['price']} total stay**
#                     """)

#                     st.markdown(f"[🔘 Book Now]({h['url']})")

#                 st.markdown("---")
                
   

#     # -------- SUMMARY -------- #
#     with tab4:
#         st.subheader("📊 Trip Summary")

#         st.markdown(f"""
#         - 📍 From: {source}  
#         - 🏁 To: {destination}  
#         - 📅 Days: {days}  
#         - 💰 Budget: ₹{budget_min} - ₹{budget_max}  
#         - 🚆 Travel Mode: {travel_mode}  
#         """)

# else:
#     st.info("👈 Fill details from sidebar and click Generate")
# =============================================================================================================


# import os
# import streamlit as st
# from dotenv import load_dotenv
# from google import genai
# from tavily import TavilyClient
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet
# import requests


# # API setup
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# client = genai.Client(api_key=GOOGLE_API_KEY)
# tavily = TavilyClient(api_key=TAVILY_API_KEY)
# # genai.configure(api_key=GOOGLE_API_KEY)
# # tavily = TavilyClient(api_key=TAVILY_API_KEY)

# # model = genai.GenerativeModel("gemini-2.5-flash")

# # -------- FUNCTIONS -------- #


# RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# headers = {
#     "X-RapidAPI-Key": RAPIDAPI_KEY,
#     "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
# }


# def get_destination_id(city):
#     try:
#         url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

#         params = {
#             "name": city,
#             "locale": "en-gb"
#         }

#         res = requests.get(url, headers=headers, params=params, timeout=10)

#         if res.status_code != 200:
#             print("Location API error:", res.status_code)
#             return None, None

#         data = res.json()

#         if not data:
#             return None, None

#         return data[0]["dest_id"], data[0]["dest_type"]

#     except Exception as e:
#         print("Destination error:", e)
#         return None, None

# GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

# def get_route_places(destination):
#     try:
#         # Step 1: Get coordinates of city
#         geo_url = "https://api.geoapify.com/v1/geocode/search"

#         geo_params = {
#             "text": destination,
#             "apiKey": GEOAPIFY_API_KEY
#         }

#         geo_res = requests.get(geo_url, params=geo_params).json()

#         if not geo_res.get("features"):
#             return []

#         lat = geo_res["features"][0]["properties"]["lat"]
#         lon = geo_res["features"][0]["properties"]["lon"]

#         # Step 2: Get tourist places nearby
#         places_url = "https://api.geoapify.com/v2/places"

#         params = {
#             "categories": "tourism.sights,tourism.attraction",
#             "filter": f"circle:{lon},{lat},10000",  # 10km radius
#             "limit": 9,
#             "apiKey": GEOAPIFY_API_KEY
#         }

#         res = requests.get(places_url, params=params).json()

#         places = []

#         for p in res.get("features", []):

#             prop = p["properties"]

#             # ✅ Static Map Image (VERY IMPORTANT)
#             map_img = f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=400&height=300&center=lonlat:{prop['lon']},{prop['lat']}&zoom=15&apiKey={GEOAPIFY_API_KEY}"

#             places.append({
#                 "title": prop.get("name", "Tourist Place"),
#                 "address": prop.get("formatted", ""),
#                 "lat": prop.get("lat"),
#                 "lon": prop.get("lon"),
#                 "image": map_img
#             })

#         return places

#     except Exception as e:
#         print("Geoapify Error:", e)
#         return []
    
# def get_hotels(destination):
#     try:
#         dest_id, dest_type = get_destination_id(destination)

#         if not dest_id:
#             print("❌ No destination found")
#             return []

#         url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

#         params = {
#         "dest_id": dest_id,
#         "dest_type": dest_type,   # dynamic (VERY IMPORTANT)
        
#         "checkin_date": "2026-05-01",
#         "checkout_date": "2026-05-03",
        
#         "adults_number": 2,
#         "room_number": 1,

#         "order_by": "popularity",

#         "locale": "en-gb",
#         "units": "metric",

#         # ✅ REQUIRED FIX
#         "filter_by_currency": "INR"
#         }
#         res = requests.get(url, headers=headers, params=params, timeout=15)

#         if res.status_code != 200:
#             print("❌ Hotel API error:", res.status_code)
#             print(res.text)
#             return []

#         data = res.json()

#         hotels = []

#         for h in data.get("result", [])[:10]:

#             try:
#                 hotels.append({
#                     "name": h.get("hotel_name"),
#                     "price": h.get("min_total_price"),
#                     "rating": h.get("review_score"),
#                     "review": h.get("review_score_word"),
#                     "image": h.get("main_photo_url"),
#                     "address": h.get("address"),
#                     "distance": h.get("distance_to_cc"),
#                     "lat": h.get("latitude"),
#                     "lon": h.get("longitude"),
#                     "url": h.get("url")
#                 })
#             except:
#                 continue

#         return hotels

#     except Exception as e:
#         print("Hotel API crash:", e)
#         return []

#     except Exception as e:
#         print("Hotel error:", e)
#         return []


# def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places):
#     names = [p["title"] for p in route_places]

#     prompt = f"""
#     Create a complete travel plan:

#     From: {source}
#     To: {destination}
#     Days: {days}
#     Budget: {budget_min} to {budget_max} INR
#     Travel Mode: {travel_mode}

#     Include:
#     - Route journey plan
#     - Places between route: {', '.join(names)}
#     - Day-wise itinerary
#     - Budget breakdown (transport + hotel + food)
#     - Travel tips
#     """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text



# # -------- UI -------- #

# st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")

# st.markdown("<h1 style='text-align:center;'>🌍 AI Travel Planner Pro</h1>", unsafe_allow_html=True)

# # Sidebar Inputs
# st.sidebar.header("✈️ Plan Your Trip")

# source = st.sidebar.text_input("📍 From (Starting City)")
# destination = st.sidebar.text_input("🏁 To (Destination City)")
# days = st.sidebar.slider("📅 Days", 1, 15, 3)

# budget_min = st.sidebar.number_input("💰 Min Budget (₹)", value=5000)
# budget_max = st.sidebar.number_input("💰 Max Budget (₹)", value=20000)

# travel_mode = st.sidebar.selectbox(
#     "🚆 Travel Mode",
#     ["Bus", "Train", "Flight", "Car"]
# )

# generate = st.sidebar.button("✨ Generate Plan")

# # -------- MAIN -------- #

# if generate and source and destination:

#     with st.spinner("🔍 Planning your smart trip..."):

#         route_places = get_route_places(destination) 
#         hotels = get_hotels(destination)
#         plan = generate_plan(
#             source, destination, days,
#             budget_min, budget_max,
#             travel_mode, route_places
#         )

#     st.success("✅ Trip Ready!")
#     st.markdown(f"""
#     ### ✈️ Trip Overview  
#     **From:** {source} → **To:** {destination}  
#     📅 {days} Days | 💰 ₹{budget_min}-{budget_max} | 🚆 {travel_mode}
#     """)

#     # -------- TABS -------- #
#     tab1, tab2, tab3, tab4 = st.tabs(
#         ["🗺️ Plan", "🛣️ Route Places", "🏨 Hotels", "📊 Summary"]
#     )

#     # -------- PLAN -------- #
#     with tab1:
#         st.subheader("📅 AI Itinerary")
#         for line in plan.split("\n"):
#             if line.strip():
#                 st.markdown(f"- {line}")

#         st.markdown("### 🔗 Booking Platforms")
#         st.markdown("""
#                     - 🛏️ Hotels: [MakeMyTrip](https://www.makemytrip.com), [Booking.com](https://www.booking.com)
#                     - 🚆 Train: [IRCTC](https://www.irctc.co.in)
#                     - 🚌 Bus: [RedBus](https://www.redbus.in)
#                     - ✈️ Flights: [Goibibo](https://www.goibibo.com)
#                             """)
#     # -------- ROUTE PLACES -------- #
#     with tab2:
#         st.subheader("🛣️ Top Tourist Places")

#         if not route_places:
#             st.warning("⚠️ No places found")
#         else:
#             cols = st.columns(3)

#             for i, p in enumerate(route_places):

#                 with cols[i % 3]:

#                     st.image(p["image"], width="stretch")

#                     st.markdown(f"""
#                     <div style="
#                         background:white;
#                         padding:12px;
#                         border-radius:12px;
#                         box-shadow:0px 4px 12px rgba(0,0,0,0.15);
#                     ">
#                         <h4>📍 {p['title']}</h4>
#                         <p>{p['address']}</p>
#                     </div>
#                     """, unsafe_allow_html=True)
#     # -------- HOTELS -------- #
#     with tab3:
#         st.subheader("🏨 Real Hotels (Live Data)")

#         if not hotels:
#             st.warning("⚠️ No hotels found")
#         else:
#             for h in hotels:

#                 col1, col2 = st.columns([1, 2])

#                 with col1:
#                     if h["image"]:
#                         st.image(h["image"], use_container_width=True)

#                 with col2:
#                     st.markdown(f"""
#                     ### 🏨 {h['name']}

#                     ⭐ {h['rating']} / 10 ({h['review']})  
#                     📍 {h['address']}  
#                     📏 {h['distance']} from center  

#                     💰 **₹{h['price']} total stay**
#                     """)

#                     st.markdown(f"[🔘 Book Now]({h['url']})")

#                 st.markdown("---")
                
   

#     # -------- SUMMARY -------- #
#     with tab4:
#         st.subheader("📊 Trip Summary")

#         st.markdown(f"""
#         - 📍 From: {source}  
#         - 🏁 To: {destination}  
#         - 📅 Days: {days}  
#         - 💰 Budget: ₹{budget_min} - ₹{budget_max}  
#         - 🚆 Travel Mode: {travel_mode}  
#         """)

# else:
#     st.info("👈 Fill details from sidebar and click Generate")
# ========================================================================

# import os
# import streamlit as st
# from dotenv import load_dotenv
# from google import genai
# from tavily import TavilyClient
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet
# import requests


# # API setup
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# client = genai.Client(api_key=GOOGLE_API_KEY)
# tavily = TavilyClient(api_key=TAVILY_API_KEY)
# # genai.configure(api_key=GOOGLE_API_KEY)
# # tavily = TavilyClient(api_key=TAVILY_API_KEY)

# # model = genai.GenerativeModel("gemini-2.5-flash")

# # -------- FUNCTIONS -------- #


# RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# headers = {
#     "X-RapidAPI-Key": RAPIDAPI_KEY,
#     "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
# }


# def get_destination_id(city):
#     try:
#         url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

#         params = {
#             "name": city,
#             "locale": "en-gb"
#         }

#         res = requests.get(url, headers=headers, params=params, timeout=10)

#         if res.status_code != 200:
#             print("Location API error:", res.status_code)
#             return None, None

#         data = res.json()

#         if not data:
#             return None, None

#         return data[0]["dest_id"], data[0]["dest_type"]

#     except Exception as e:
#         print("Destination error:", e)
#         return None, None

# GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

# def get_lat_lon(city):
#     url = "https://api.geoapify.com/v1/geocode/search"

#     params = {
#         "text": city,
#         "apiKey": GEOAPIFY_API_KEY
#     }

#     res = requests.get(url, params=params).json()

#     if not res.get("features"):
#         return None, None

#     lat = res["features"][0]["properties"]["lat"]
#     lon = res["features"][0]["properties"]["lon"]

#     return lat, lon


# def get_route_places(source, destination):
#     try:
#         # STEP 1: Convert cities → coordinates
#         geo_url = "https://api.geoapify.com/v1/geocode/search"

#         def get_coords(city):
#             res = requests.get(geo_url, params={
#                 "text": city,
#                 "apiKey": GEOAPIFY_API_KEY
#             }).json()

#             if not res.get("features"):
#                 return None

#             prop = res["features"][0]["properties"]
#             return prop["lon"], prop["lat"]

#         start = get_coords(source)
#         end = get_coords(destination)

#         if not start or not end:
#             print("❌ Geocoding failed")
#             return []

#         # STEP 2: Get route
#         route_url = "https://api.geoapify.com/v1/routing"

#         params = {
#             "waypoints": f"{start[1]},{start[0]}|{end[1]},{end[0]}",
#             "mode": "drive",
#             "apiKey": GEOAPIFY_API_KEY
#         }

#         route_res = requests.get(route_url, params=params).json()

#         if "features" not in route_res:
#             print("❌ Route API error:", route_res)
#             return []

#         coords = route_res["features"][0]["geometry"]["coordinates"]

#         # FIX: flatten nested coordinates
#         if isinstance(coords[0][0], list):
#             coords = coords[0]

#         # STEP 3: Pick sample points (safe)
#         step = max(1, len(coords) // 6)
#         sample_points = coords[::step]

#         places = []
#         seen = set()

#         # STEP 4: Get places near each point
#         for lon, lat in sample_points:

#             places_url = "https://api.geoapify.com/v2/places"

#             params = {
#                 "categories": "tourism.sights,tourism.attraction",
#                 "filter": f"circle:{lon},{lat},4000",
#                 "limit": 2,
#                 "apiKey": GEOAPIFY_API_KEY
#             }

#             res = requests.get(places_url, params=params).json()

#             for item in res.get("features", []):
#                 prop = item["properties"]

#                 name = prop.get("name", "Place")

#                 # avoid duplicates
#                 if name in seen:
#                     continue
#                 seen.add(name)

#                 places.append({
#                     "title": name,
#                     "address": prop.get("formatted", ""),
#                     "lat": prop.get("lat"),
#                     "lon": prop.get("lon"),
#                     "image": f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=400&height=300&center=lonlat:{prop.get('lon')},{prop.get('lat')}&zoom=14&apiKey={GEOAPIFY_API_KEY}"
#                 })

#         return places[:10]

#     except Exception as e:
#         print("❌ Route System Error:", e)
#         return []

# # def get_route_places(source, destination):
# #     try:
# #         # ✅ Step 1: Convert cities → coordinates
# #         lat1, lon1 = get_lat_lon(source)
# #         lat2, lon2 = get_lat_lon(destination)

# #         if not lat1 or not lat2:
# #             print("❌ Location conversion failed")
# #             return []

# #         # ✅ Step 2: Get route
# #         route_url = "https://api.geoapify.com/v1/routing"

# #         params = {
# #             "waypoints": f"{lat1},{lon1}|{lat2},{lon2}",
# #             "mode": "drive",
# #             "apiKey": GEOAPIFY_API_KEY
# #         }

# #         route_res = requests.get(route_url, params=params).json()

# #         # ✅ SAFE CHECK (VERY IMPORTANT)
# #         if "features" not in route_res:
# #             print("Routing API Error:", route_res)
# #             return []

# #         coords = route_res["features"][0]["geometry"]["coordinates"]

# #         # ✅ Step 3: Pick points from route
# #         step = max(1, len(coords)//5)
# #         sample_points = coords[::step]

# #         places = []

# #         # ✅ Step 4: Get places near route
# #         for lon, lat in sample_points:

# #             places_url = "https://api.geoapify.com/v2/places"

# #             p = {
# #                 "categories": "tourism.sights,tourism.attraction",
# #                 "filter": f"circle:{lon},{lat},5000",
# #                 "limit": 2,
# #                 "apiKey": GEOAPIFY_API_KEY
# #             }

# #             res = requests.get(places_url, params=p).json()

# #             for item in res.get("features", []):
# #                 prop = item["properties"]

# #                 places.append({
# #                     "title": prop.get("name", "Tourist Place"),
# #                     "address": prop.get("formatted", ""),
# #                     "image": f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=400&height=300&center=lonlat:{prop['lon']},{prop['lat']}&zoom=14&apiKey={GEOAPIFY_API_KEY}"
# #                 })

# #         return places[:10]

# #     except Exception as e:
# #         print("Route Error:", e)
# #         return []

# # def get_route_places(source, destination):

# #     # 1. Get route
# #     route_url = "https://api.geoapify.com/v1/routing"

# #     params = {
# #         "waypoints": f"{source}|{destination}",
# #         "mode": "drive",
# #         "apiKey": GEOAPIFY_API_KEY
# #     }

# #     route_res = requests.get(route_url, params=params).json()

# #     coords = route_res["features"][0]["geometry"]["coordinates"]

# #     # 2. Pick few points
# #     sample_points = coords[::len(coords)//5]   # 5 points

# #     places = []

# #     for lon, lat in sample_points:

# #         # 3. Get places near each point
# #         places_url = "https://api.geoapify.com/v2/places"

# #         p = {
# #             "categories": "tourism.sights,tourism.attraction",
# #             "filter": f"circle:{lon},{lat},5000",
# #             "limit": 2,
# #             "apiKey": GEOAPIFY_API_KEY
# #         }

# #         res = requests.get(places_url, params=p).json()

# #         for item in res.get("features", []):
# #             prop = item["properties"]

# #             places.append({
# #                 "title": prop.get("name", "Place"),
# #                 "address": prop.get("formatted", ""),
# #                 "lat": prop.get("lat"),
# #                 "lon": prop.get("lon"),
# #                 "image": f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=400&height=300&center=lonlat:{prop['lon']},{prop['lat']}&zoom=14&apiKey={GEOAPIFY_API_KEY}"
# #             })

# #     return places[:10]


# def get_hotels(destination):
#     try:
#         dest_id, dest_type = get_destination_id(destination)

#         if not dest_id:
#             print("❌ No destination found")
#             return []

#         url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

#         params = {
#         "dest_id": dest_id,
#         "dest_type": dest_type,   # dynamic (VERY IMPORTANT)
        
#         "checkin_date": "2026-05-01",
#         "checkout_date": "2026-05-03",
        
#         "adults_number": 2,
#         "room_number": 1,

#         "order_by": "popularity",

#         "locale": "en-gb",
#         "units": "metric",

#         # ✅ REQUIRED FIX
#         "filter_by_currency": "INR"
#         }
#         res = requests.get(url, headers=headers, params=params, timeout=15)

#         if res.status_code != 200:
#             print("❌ Hotel API error:", res.status_code)
#             print(res.text)
#             return []

#         data = res.json()

#         hotels = []

#         for h in data.get("result", [])[:10]:

#             try:
#                 hotels.append({
#                     "name": h.get("hotel_name"),
#                     "price": h.get("min_total_price"),
#                     "rating": h.get("review_score"),
#                     "review": h.get("review_score_word"),
#                     "image": h.get("main_photo_url"),
#                     "address": h.get("address"),
#                     "distance": h.get("distance_to_cc"),
#                     "lat": h.get("latitude"),
#                     "lon": h.get("longitude"),
#                     "url": h.get("url")
#                 })
#             except:
#                 continue

#         return hotels

#     except Exception as e:
#         print("Hotel API crash:", e)
#         return []

#     except Exception as e:
#         print("Hotel error:", e)
#         return []


# def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places):
#     names = [p["title"] for p in route_places]

#     prompt = f"""
#     Create a complete travel plan:

#     From: {source}
#     To: {destination}
#     Days: {days}
#     Budget: {budget_min} to {budget_max} INR
#     Travel Mode: {travel_mode}

#     Include:
#     - Route journey plan
#     - Places between route: {', '.join(names)}
#     - Day-wise itinerary
#     - Budget breakdown (transport + hotel + food)
#     - Travel tips
#     """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text



# # -------- UI -------- #

# st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")

# st.markdown("<h1 style='text-align:center;'>🌍 AI Travel Planner Pro</h1>", unsafe_allow_html=True)

# # Sidebar Inputs
# st.sidebar.header("✈️ Plan Your Trip")

# source = st.sidebar.text_input("📍 From (Starting City)")
# destination = st.sidebar.text_input("🏁 To (Destination City)")
# days = st.sidebar.slider("📅 Days", 1, 15, 3)

# budget_min = st.sidebar.number_input("💰 Min Budget (₹)", value=5000)
# budget_max = st.sidebar.number_input("💰 Max Budget (₹)", value=20000)

# travel_mode = st.sidebar.selectbox(
#     "🚆 Travel Mode",
#     ["Bus", "Train", "Flight", "Car"]
# )

# generate = st.sidebar.button("✨ Generate Plan")

# # -------- MAIN -------- #

# if generate and source and destination:

#     with st.spinner("🔍 Planning your smart trip..."):

#         route_places = get_route_places(source, destination)
    
#         hotels = get_hotels(destination)
#         plan = generate_plan(
#             source, destination, days,
#             budget_min, budget_max,
#             travel_mode, route_places
#         )

#     st.success("✅ Trip Ready!")
#     st.markdown(f"""
#     ### ✈️ Trip Overview  
#     **From:** {source} → **To:** {destination}  
#     📅 {days} Days | 💰 ₹{budget_min}-{budget_max} | 🚆 {travel_mode}
#     """)

#     # -------- TABS -------- #
#     tab1, tab2, tab3, tab4 = st.tabs(
#         ["🗺️ Plan", "🛣️ Route Places", "🏨 Hotels", "📊 Summary"]
#     )

#     # -------- PLAN -------- #
#     with tab1:
#         st.subheader("📅 AI Itinerary")
#         for line in plan.split("\n"):
#             if line.strip():
#                 st.markdown(f"- {line}")

#         st.markdown("### 🔗 Booking Platforms")
#         st.markdown("""
#                     - 🛏️ Hotels: [MakeMyTrip](https://www.makemytrip.com), [Booking.com](https://www.booking.com)
#                     - 🚆 Train: [IRCTC](https://www.irctc.co.in)
#                     - 🚌 Bus: [RedBus](https://www.redbus.in)
#                     - ✈️ Flights: [Goibibo](https://www.goibibo.com)
#                             """)
#     # -------- ROUTE PLACES -------- #
#     with tab2:
#         st.subheader("🛣️ Places Between Your Journey")

#         if not route_places:
#             st.warning("⚠️ No route places found")
#         else:
#             cols = st.columns(2)

#             for i, p in enumerate(route_places):
#                 with cols[i % 2]:
#                     st.image(p["image"], width="stretch")
#                     st.markdown(f"""
#                     **📍 {p['title']}**  
#                     {p['address']}
#                     """)
#     # with tab2:
#     #     st.subheader("🛣️ Top Tourist Places")

#     #     if not route_places:
#     #         st.warning("⚠️ No places found")
#     #     else:
#     #         cols = st.columns(3)

#     #         for i, p in enumerate(route_places):

#     #             with cols[i % 3]:

#     #                 st.image(p["image"], width="stretch")

#     #                 st.markdown(f"""
#     #                 <div style="
#     #                     background:white;
#     #                     padding:12px;
#     #                     border-radius:12px;
#     #                     box-shadow:0px 4px 12px rgba(0,0,0,0.15);
#     #                 ">
#     #                     <h4>📍 {p['title']}</h4>
#     #                     <p>{p['address']}</p>
#     #                 </div>
#     #                 """, unsafe_allow_html=True)
#     # -------- HOTELS -------- #
#     with tab3:
#         st.subheader("🏨 Real Hotels (Live Data)")

#         if not hotels:
#             st.warning("⚠️ No hotels found")
#         else:
#             for h in hotels:

#                 col1, col2 = st.columns([1, 2])

#                 with col1:
#                     if h["image"]:
#                         st.image(h["image"], use_container_width=True)

#                 with col2:
#                     st.markdown(f"""
#                     ### 🏨 {h['name']}

#                     ⭐ {h['rating']} / 10 ({h['review']})  
#                     📍 {h['address']}  
#                     📏 {h['distance']} from center  

#                     💰 **₹{h['price']} total stay**
#                     """)

#                     st.markdown(f"[🔘 Book Now]({h['url']})")

#                 st.markdown("---")
                
   

#     # -------- SUMMARY -------- #
#     with tab4:
#         st.subheader("📊 Trip Summary")

#         st.markdown(f"""
#         - 📍 From: {source}  
#         - 🏁 To: {destination}  
#         - 📅 Days: {days}  
#         - 💰 Budget: ₹{budget_min} - ₹{budget_max}  
#         - 🚆 Travel Mode: {travel_mode}  
#         """)

# else:
#     st.info("👈 Fill details from sidebar and click Generate")


# ===========================***************************************************************======================================================

# import os
# import streamlit as st
# from dotenv import load_dotenv
# from google import genai
# from tavily import TavilyClient
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet
# import requests


# # API setup
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# client = genai.Client(api_key=GOOGLE_API_KEY)
# tavily = TavilyClient(api_key=TAVILY_API_KEY)
# # genai.configure(api_key=GOOGLE_API_KEY)
# # tavily = TavilyClient(api_key=TAVILY_API_KEY)

# # model = genai.GenerativeModel("gemini-2.5-flash")

# # -------- FUNCTIONS -------- #


# RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# headers = {
#     "X-RapidAPI-Key": RAPIDAPI_KEY,
#     "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
# }


# def get_destination_id(city):
#     try:
#         url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

#         params = {
#             "name": city,
#             "locale": "en-gb"
#         }

#         res = requests.get(url, headers=headers, params=params, timeout=10)

#         if res.status_code != 200:
#             print("Location API error:", res.status_code)
#             return None, None

#         data = res.json()

#         if not data:
#             return None, None

#         return data[0]["dest_id"], data[0]["dest_type"]

#     except Exception as e:
#         print("Destination error:", e)
#         return None, None

# GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

# def get_lat_lon(city):
#     url = "https://api.geoapify.com/v1/geocode/search"

#     params = {
#         "text": city,
#         "apiKey": GEOAPIFY_API_KEY
#     }

#     res = requests.get(url, params=params).json()

#     if not res.get("features"):
#         return None, None

#     lat = res["features"][0]["properties"]["lat"]
#     lon = res["features"][0]["properties"]["lon"]

#     return lat, lon


# def get_route_places(source, destination):
#     try:
#         # STEP 1: Convert cities → coordinates
#         geo_url = "https://api.geoapify.com/v1/geocode/search"

#         def get_coords(city):
#             res = requests.get(geo_url, params={
#                 "text": city,
#                 "apiKey": GEOAPIFY_API_KEY
#             }).json()

#             if not res.get("features"):
#                 return None

#             prop = res["features"][0]["properties"]
#             return prop["lon"], prop["lat"]

#         start = get_coords(source)
#         end = get_coords(destination)

#         if not start or not end:
#             print("❌ Geocoding failed")
#             return []

#         # STEP 2: Get route
#         route_url = "https://api.geoapify.com/v1/routing"

#         params = {
#             "waypoints": f"{start[1]},{start[0]}|{end[1]},{end[0]}",
#             "mode": "drive",
#             "apiKey": GEOAPIFY_API_KEY
#         }

#         route_res = requests.get(route_url, params=params).json()

#         if "features" not in route_res:
#             print("❌ Route API error:", route_res)
#             return []

#         coords = route_res["features"][0]["geometry"]["coordinates"]

#         # FIX: flatten nested coordinates
#         if isinstance(coords[0][0], list):
#             coords = coords[0]

#         # STEP 3: Pick sample points (safe)
#         step = max(1, len(coords) // 6)
#         sample_points = coords[::step]

#         places = []
#         seen = set()

#         # STEP 4: Get places near each point
#         for lon, lat in sample_points:

#             places_url = "https://api.geoapify.com/v2/places"

#             params = {
#                 "categories": "tourism.sights,tourism.attraction",
#                 "filter": f"circle:{lon},{lat},4000",
#                 "limit": 2,
#                 "apiKey": GEOAPIFY_API_KEY
#             }

#             res = requests.get(places_url, params=params).json()

#             for item in res.get("features", []):
#                 prop = item["properties"]

#                 name = prop.get("name", "Place")

#                 # avoid duplicates
#                 if name in seen:
#                     continue
#                 seen.add(name)

#                 places.append({
#                     "title": name,
#                     "address": prop.get("formatted", ""),
#                     "lat": prop.get("lat"),
#                     "lon": prop.get("lon"),
#                     "image": f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=400&height=300&center=lonlat:{prop.get('lon')},{prop.get('lat')}&zoom=14&apiKey={GEOAPIFY_API_KEY}"
#                 })

#         return places[:10]

#     except Exception as e:
#         print("❌ Route System Error:", e)
#         return []


# def get_hotels(destination):
#     try:
#         dest_id, dest_type = get_destination_id(destination)

#         if not dest_id:
#             print("❌ No destination found")
#             return []

#         url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

#         params = {
#         "dest_id": dest_id,
#         "dest_type": dest_type,   # dynamic (VERY IMPORTANT)
        
#         "checkin_date": "2026-05-01",
#         "checkout_date": "2026-05-03",
        
#         "adults_number": 2,
#         "room_number": 1,

#         "order_by": "popularity",

#         "locale": "en-gb",
#         "units": "metric",

#         # ✅ REQUIRED FIX
#         "filter_by_currency": "INR"
#         }
#         res = requests.get(url, headers=headers, params=params, timeout=15)

#         if res.status_code != 200:
#             print("❌ Hotel API error:", res.status_code)
#             print(res.text)
#             return []

#         data = res.json()

#         hotels = []

#         for h in data.get("result", [])[:10]:

#             try:
#                 hotels.append({
#                     "name": h.get("hotel_name"),
#                     "price": h.get("min_total_price"),
#                     "rating": h.get("review_score"),
#                     "review": h.get("review_score_word"),
#                     "image": h.get("main_photo_url"),
#                     "address": h.get("address"),
#                     "distance": h.get("distance_to_cc"),
#                     "lat": h.get("latitude"),
#                     "lon": h.get("longitude"),
#                     "url": h.get("url")
#                 })
#             except:
#                 continue

#         return hotels

#     except Exception as e:
#         print("Hotel API crash:", e)
#         return []

#     except Exception as e:
#         print("Hotel error:", e)
#         return []


# def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places):
#     names = [p["title"] for p in route_places]

#     prompt = f"""
#     Create a complete travel plan:

#     From: {source}
#     To: {destination}
#     Days: {days}
#     Budget: {budget_min} to {budget_max} INR
#     Travel Mode: {travel_mode}

#     Include:
#     - Route journey plan
#     - Places between route: {', '.join(names)}
#     - Day-wise itinerary
#     - Budget breakdown (transport + hotel + food)
#     - Travel tips
#     """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text



# # -------- UI -------- #

# st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")

# st.markdown("<h1 style='text-align:center;'>🌍 AI Travel Planner Pro</h1>", unsafe_allow_html=True)

# # Sidebar Inputs
# st.sidebar.header("✈️ Plan Your Trip")

# source = st.sidebar.text_input("📍 From (Starting City)")
# destination = st.sidebar.text_input("🏁 To (Destination City)")
# days = st.sidebar.slider("📅 Days", 1, 15, 3)

# budget_min = st.sidebar.number_input("💰 Min Budget (₹)", value=5000)
# budget_max = st.sidebar.number_input("💰 Max Budget (₹)", value=20000)

# travel_mode = st.sidebar.selectbox(
#     "🚆 Travel Mode",
#     ["Bus", "Train", "Flight", "Car"]
# )

# generate = st.sidebar.button("✨ Generate Plan")

# # -------- MAIN -------- #

# if generate and source and destination:

#     with st.spinner("🔍 Planning your smart trip..."):

#         route_places = get_route_places(source, destination)
    
#         hotels = get_hotels(destination)
#         plan = generate_plan(
#             source, destination, days,
#             budget_min, budget_max,
#             travel_mode, route_places
#         )

#     st.success("✅ Trip Ready!")
#     st.markdown(f"""
#     ### ✈️ Trip Overview  
#     **From:** {source} → **To:** {destination}  
#     📅 {days} Days | 💰 ₹{budget_min}-{budget_max} | 🚆 {travel_mode}
#     """)

#     # -------- TABS -------- #
#     tab1, tab2, tab3, tab4 = st.tabs(
#         ["🗺️ Plan", "🛣️ Route Places", "🏨 Hotels", "📊 Summary"]
#     )

#     # -------- PLAN -------- #
#     with tab1:
#         st.subheader("📅 AI Itinerary")
#         for line in plan.split("\n"):
#             if line.strip():
#                 st.markdown(f"- {line}")

#         st.markdown("### 🔗 Booking Platforms")
#         st.markdown("""
#                     - 🛏️ Hotels: [MakeMyTrip](https://www.makemytrip.com), [Booking.com](https://www.booking.com)
#                     - 🚆 Train: [IRCTC](https://www.irctc.co.in)
#                     - 🚌 Bus: [RedBus](https://www.redbus.in)
#                     - ✈️ Flights: [Goibibo](https://www.goibibo.com)
#                             """)
#     # -------- ROUTE PLACES -------- #
#     with tab2:
#         st.subheader("🛣️ Places Between Your Journey")

#         if not route_places:
#             st.warning("⚠️ No route places found")
#         else:
#             cols = st.columns(2)

#             for i, p in enumerate(route_places):
#                 with cols[i % 2]:
#                     st.image(p["image"], width="stretch")
#                     st.markdown(f"""
#                     **📍 {p['title']}**  
#                     {p['address']}
#                     """)
#     # with tab2:
#     #     st.subheader("🛣️ Top Tourist Places")

#     #     if not route_places:
#     #         st.warning("⚠️ No places found")
#     #     else:
#     #         cols = st.columns(3)

#     #         for i, p in enumerate(route_places):

#     #             with cols[i % 3]:

#     #                 st.image(p["image"], width="stretch")

#     #                 st.markdown(f"""
#     #                 <div style="
#     #                     background:white;
#     #                     padding:12px;
#     #                     border-radius:12px;
#     #                     box-shadow:0px 4px 12px rgba(0,0,0,0.15);
#     #                 ">
#     #                     <h4>📍 {p['title']}</h4>
#     #                     <p>{p['address']}</p>
#     #                 </div>
#     #                 """, unsafe_allow_html=True)
#     # -------- HOTELS -------- #
#     with tab3:
#         st.subheader("🏨 Real Hotels (Live Data)")

#         if not hotels:
#             st.warning("⚠️ No hotels found")
#         else:
#             for h in hotels:

#                 col1, col2 = st.columns([1, 2])

#                 with col1:
#                     if h["image"]:
#                         st.image(h["image"], use_container_width=True)

#                 with col2:
#                     st.markdown(f"""
#                     ### 🏨 {h['name']}

#                     ⭐ {h['rating']} / 10 ({h['review']})  
#                     📍 {h['address']}  
#                     📏 {h['distance']} from center  

#                     💰 **₹{h['price']} total stay**
#                     """)

#                     st.markdown(f"[🔘 Book Now]({h['url']})")

#                 st.markdown("---")
                
   

#     # -------- SUMMARY -------- #
#     with tab4:
#         st.subheader("📊 Trip Summary")

#         st.markdown(f"""
#         - 📍 From: {source}  
#         - 🏁 To: {destination}  
#         - 📅 Days: {days}  
#         - 💰 Budget: ₹{budget_min} - ₹{budget_max}  
#         - 🚆 Travel Mode: {travel_mode}  
#         """)

# else:
#     st.info("👈 Fill details from sidebar and click Generate")                

# ===================================**********************************====================================================================================



# import os
# import streamlit as st
# from dotenv import load_dotenv
# from google import genai
# from tavily import TavilyClient
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet
# import requests


# # API setup
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# client = genai.Client(api_key=GOOGLE_API_KEY)
# tavily = TavilyClient(api_key=TAVILY_API_KEY)
# # genai.configure(api_key=GOOGLE_API_KEY)
# # tavily = TavilyClient(api_key=TAVILY_API_KEY)

# # model = genai.GenerativeModel("gemini-2.5-flash")

# # -------- FUNCTIONS -------- #


# RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# headers = {
#     "X-RapidAPI-Key": RAPIDAPI_KEY,
#     "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
# }


# def get_destination_id(city):
#     try:
#         url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

#         params = {
#             "name": city,
#             "locale": "en-gb"
#         }

#         res = requests.get(url, headers=headers, params=params, timeout=10)

#         if res.status_code != 200:
#             print("Location API error:", res.status_code)
#             return None, None

#         data = res.json()

#         if not data:
#             return None, None

#         return data[0]["dest_id"], data[0]["dest_type"]

#     except Exception as e:
#         print("Destination error:", e)
#         return None, None

# GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

# def get_lat_lon(city):
#     url = "https://api.geoapify.com/v1/geocode/search"

#     params = {
#         "text": city,
#         "apiKey": GEOAPIFY_API_KEY
#     }

#     res = requests.get(url, params=params).json()

#     if not res.get("features"):
#         return None, None

#     lat = res["features"][0]["properties"]["lat"]
#     lon = res["features"][0]["properties"]["lon"]

#     return lat, lon


# def get_route_places(source, destination):
#     try:
#         # STEP 1: Convert cities → coordinates
#         geo_url = "https://api.geoapify.com/v1/geocode/search"

#         def get_coords(city):
#             res = requests.get(geo_url, params={
#                 "text": city,
#                 "apiKey": GEOAPIFY_API_KEY
#             }).json()

#             if not res.get("features"):
#                 return None

#             prop = res["features"][0]["properties"]
#             return prop["lon"], prop["lat"]

#         start = get_coords(source)
#         end = get_coords(destination)

#         if not start or not end:
#             print("❌ Geocoding failed")
#             return []

#         # STEP 2: Get route
#         route_url = "https://api.geoapify.com/v1/routing"

#         params = {
#             "waypoints": f"{start[1]},{start[0]}|{end[1]},{end[0]}",
#             "mode": "drive",
#             "apiKey": GEOAPIFY_API_KEY
#         }

#         route_res = requests.get(route_url, params=params).json()

#         if "features" not in route_res:
#             print("❌ Route API error:", route_res)
#             return []

#         coords = route_res["features"][0]["geometry"]["coordinates"]

#         # FIX: flatten nested coordinates
#         if isinstance(coords[0][0], list):
#             coords = coords[0]

#         # STEP 3: Pick sample points (safe)
#         step = max(1, len(coords) // 6)
#         sample_points = coords[::step]

#         places = []
#         seen = set()

#         # STEP 4: Get places near each point
#         for lon, lat in sample_points:

#             places_url = "https://api.geoapify.com/v2/places"

#             params = {
#                 "categories": "tourism.sights,tourism.attraction",
#                 "filter": f"circle:{lon},{lat},4000",
#                 "limit": 2,
#                 "apiKey": GEOAPIFY_API_KEY
#             }

#             res = requests.get(places_url, params=params).json()

#             for item in res.get("features", []):
#                 prop = item["properties"]

#                 name = prop.get("name", "Place")

#                 # avoid duplicates
#                 if name in seen:
#                     continue
#                 seen.add(name)

#                 places.append({
#                     "title": name,
#                     "address": prop.get("formatted", ""),
#                     "lat": prop.get("lat"),
#                     "lon": prop.get("lon"),
#                     "image": f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=400&height=300&center=lonlat:{prop.get('lon')},{prop.get('lat')}&zoom=14&apiKey={GEOAPIFY_API_KEY}"
#                 })

#         return places[:10]

#     except Exception as e:
#         print("❌ Route System Error:", e)
#         return []


# def get_hotels(destination):
#     try:
#         dest_id, dest_type = get_destination_id(destination)

#         if not dest_id:
#             print("❌ No destination found")
#             return []

#         url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

#         params = {
#         "dest_id": dest_id,
#         "dest_type": dest_type,   # dynamic (VERY IMPORTANT)
        
#         "checkin_date": "2026-05-01",
#         "checkout_date": "2026-05-03",
        
#         "adults_number": 2,
#         "room_number": 1,

#         "order_by": "popularity",

#         "locale": "en-gb",
#         "units": "metric",

#         # ✅ REQUIRED FIX
#         "filter_by_currency": "INR"
#         }
#         res = requests.get(url, headers=headers, params=params, timeout=15)

#         if res.status_code != 200:
#             print("❌ Hotel API error:", res.status_code)
#             print(res.text)
#             return []

#         data = res.json()

#         hotels = []

#         for h in data.get("result", [])[:10]:

#             try:
#                 hotels.append({
#                     "name": h.get("hotel_name"),
#                     "price": h.get("min_total_price"),
#                     "rating": h.get("review_score"),
#                     "review": h.get("review_score_word"),
#                     "image": h.get("main_photo_url"),
#                     "address": h.get("address"),
#                     "distance": h.get("distance_to_cc"),
#                     "lat": h.get("latitude"),
#                     "lon": h.get("longitude"),
#                     "url": h.get("url")
#                 })
#             except:
#                 continue

#         return hotels

#     except Exception as e:
#         print("Hotel API crash:", e)
#         return []

#     except Exception as e:
#         print("Hotel error:", e)
#         return []


# def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places):
#     names = [p["title"] for p in route_places]

#     prompt = f"""
#     Create a complete travel plan:

#     From: {source}
#     To: {destination}
#     Days: {days}
#     Budget: {budget_min} to {budget_max} INR
#     Travel Mode: {travel_mode}

#     Include:
#     - Route journey plan
#     - Places between route: {', '.join(names)}
#     - Day-wise itinerary
#     - Budget breakdown (transport + hotel + food)
#     - Travel tips
#     """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text



# # -------- UI -------- #
# import streamlit as st

# st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")

# # ---------- CUSTOM CSS ----------
# st.markdown("""
# <style>

# .main {
#     background-color: #eef2f7;
# }

# /* HERO SECTION */
# .hero {
#     background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');
#     background-size: cover;
#     background-position: center;
#     padding: 80px 20px;
#     border-radius: 20px;
#     color: white;
#     text-align: center;
#     margin-bottom: 20px;
#     position: relative;
# }

# .hero::after {
#     content: "";
#     position: absolute;
#     top: 0;
#     left: 0;
#     right: 0;
#     bottom: 0;
#     background: rgba(0,0,0,0.5);
#     border-radius: 20px;
# }

# .hero-content {
#     position: relative;
#     z-index: 2;
# }

# .title {
#     font-size: 42px;
#     font-weight: bold;
# }

# .subtitle {
#     font-size: 18px;
#     margin-top: 10px;
# }

# /* SEARCH BOX */
# .search-box {
#     background: white;
#     padding: 25px;
#     border-radius: 20px;
#     box-shadow: 0px 6px 25px rgba(0,0,0,0.1);
#     margin-top: -40px;
# }

# /* DESTINATION CARDS */
# .card {
#     background: white;
#     border-radius: 15px;
#     overflow: hidden;
#     box-shadow: 0px 5px 20px rgba(0,0,0,0.1);
#     transition: 0.3s;
# }

# .card:hover {
#     transform: translateY(-5px);
# }

# .card img {
#     width: 100%;
#     height: 160px;
#     object-fit: cover;
# }

# .card-title {
#     padding: 10px;
#     font-weight: bold;
# }

# /* BUTTON */
# button[kind="primary"] {
#     background: linear-gradient(90deg, #ff4b4b, #ff7b7b);
#     border-radius: 12px;
#     height: 50px;
#     font-size: 18px;
# }

# </style>
# """, unsafe_allow_html=True)

# # ---------- HERO SECTION ----------
# st.markdown("""
# <div class="hero">
#     <div class="hero-content">
#         <div class="title">🌍 AI Travel Planner Pro</div>
#         <div class="subtitle">Discover • Plan • Travel ✈️</div>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # ---------- SEARCH BOX ----------
# with st.container():
#     st.markdown("<div class='search-box'>", unsafe_allow_html=True)

#     col1, col2, col3, col4, col5 = st.columns([2,2,1,2,1])

#     with col1:
#         source = st.text_input("From", placeholder="Enter city", label_visibility="collapsed")

#     with col2:
#         destination = st.text_input("To", placeholder="Enter destination", label_visibility="collapsed")

#     with col3:
#         days = st.number_input("Days", min_value=1, max_value=15, value=3)

#     with col4:
#         budget = st.slider("Budget (₹)", 1000, 100000, (5000, 20000))
#         budget_min, budget_max = budget

#     with col5:
#         travel_mode = st.selectbox("Mode", ["🚗 Car", "✈️ Flight", "🚆 Train", "🚌 Bus"])

#     generate = st.button("✨ Generate Plan", use_container_width=True)

#     st.markdown("</div>", unsafe_allow_html=True)

# # ---------- POPULAR DESTINATIONS ----------
# st.subheader("🔥 Popular Destinations")

# col1, col2, col3, col4 = st.columns(4)

# destinations = [
#     ("Goa", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"),
#     ("Manali", "https://images.unsplash.com/photo-1501785888041-af3ef285b470"),
#     ("Jaipur", "https://images.unsplash.com/photo-1599661046827-dacff0c0f09c"),
#     ("Kerala", "https://images.unsplash.com/photo-1501785888041-af3ef285b470")
# ]

# for i, (name, img) in enumerate(destinations):
#     with [col1, col2, col3, col4][i]:
#         st.markdown(f"""
#         <div class="card">
#             <img src="{img}">
#             <div class="card-title">📍 {name}</div>
#         </div>
#         """, unsafe_allow_html=True)
# # -------- MAIN -------- #

# if generate and source and destination:

#     with st.spinner("🔍 Planning your smart trip..."):

#         route_places = get_route_places(source, destination)
    
#         hotels = get_hotels(destination)
#         plan = generate_plan(
#             source, destination, days,
#             budget_min, budget_max,
#             travel_mode, route_places
#         )

#     st.success("✅ Trip Ready!")
#     st.markdown(f"""
#     ### ✈️ Trip Overview  
#     **From:** {source} → **To:** {destination}  
#     📅 {days} Days | 💰 ₹{budget_min}-{budget_max} | 🚆 {travel_mode}
#     """)

#     # -------- TABS -------- #
#     tab1, tab2, tab3, tab4 = st.tabs(
#         ["🗺️ Plan", "🛣️ Route Places", "🏨 Hotels", "📊 Summary"]
#     )

#     # -------- PLAN -------- #
#     with tab1:
#         st.subheader("📅 AI Itinerary")
#         for line in plan.split("\n"):
#             if line.strip():
#                 st.markdown(f"- {line}")

#         st.markdown("### 🔗 Booking Platforms")
#         st.markdown("""
#                     - 🛏️ Hotels: [MakeMyTrip](https://www.makemytrip.com), [Booking.com](https://www.booking.com)
#                     - 🚆 Train: [IRCTC](https://www.irctc.co.in)
#                     - 🚌 Bus: [RedBus](https://www.redbus.in)
#                     - ✈️ Flights: [Goibibo](https://www.goibibo.com)
#                             """)
#     # -------- ROUTE PLACES -------- #
#     with tab2:
#         st.subheader("🛣️ Places Between Your Journey")

#         if not route_places:
#             st.warning("⚠️ No route places found")
#         else:
#             cols = st.columns(2)

#             for i, p in enumerate(route_places):
#                 with cols[i % 2]:
#                     st.image(p["image"], width="stretch")
#                     st.markdown(f"""
#                     **📍 {p['title']}**  
#                     {p['address']}
#                     """)
#     # with tab2:
#     #     st.subheader("🛣️ Top Tourist Places")

#     #     if not route_places:
#     #         st.warning("⚠️ No places found")
#     #     else:
#     #         cols = st.columns(3)

#     #         for i, p in enumerate(route_places):

#     #             with cols[i % 3]:

#     #                 st.image(p["image"], width="stretch")

#     #                 st.markdown(f"""
#     #                 <div style="
#     #                     background:white;
#     #                     padding:12px;
#     #                     border-radius:12px;
#     #                     box-shadow:0px 4px 12px rgba(0,0,0,0.15);
#     #                 ">
#     #                     <h4>📍 {p['title']}</h4>
#     #                     <p>{p['address']}</p>
#     #                 </div>
#     #                 """, unsafe_allow_html=True)
#     # -------- HOTELS -------- #
#     with tab3:
#         st.subheader("🏨 Real Hotels (Live Data)")

#         if not hotels:
#             st.warning("⚠️ No hotels found")
#         else:
#             for h in hotels:

#                 col1, col2 = st.columns([1, 2])

#                 with col1:
#                     if h["image"]:
#                         st.image(h["image"], use_container_width=True)

#                 with col2:
#                     st.markdown(f"""
#                     ### 🏨 {h['name']}

#                     ⭐ {h['rating']} / 10 ({h['review']})  
#                     📍 {h['address']}  
#                     📏 {h['distance']} from center  

#                     💰 **₹{h['price']} total stay**
#                     """)

#                     st.markdown(f"[🔘 Book Now]({h['url']})")

#                 st.markdown("---")
                
   

#     # -------- SUMMARY -------- #
#     with tab4:
#         st.subheader("📊 Trip Summary")

#         st.markdown(f"""
#         - 📍 From: {source}  
#         - 🏁 To: {destination}  
#         - 📅 Days: {days}  
#         - 💰 Budget: ₹{budget_min} - ₹{budget_max}  
#         - 🚆 Travel Mode: {travel_mode}  
#         """)

# else:
#     st.info("👈 Fill details from sidebar and click Generate")                 


# ===========================================================================================================



# import os
# import streamlit as st
# from dotenv import load_dotenv
# from google import genai
# from tavily import TavilyClient
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet
# import requests


# # API setup
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# client = genai.Client(api_key=GOOGLE_API_KEY)
# tavily = TavilyClient(api_key=TAVILY_API_KEY)
# # genai.configure(api_key=GOOGLE_API_KEY)
# # tavily = TavilyClient(api_key=TAVILY_API_KEY)

# # model = genai.GenerativeModel("gemini-2.5-flash")

# # -------- FUNCTIONS -------- #


# RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# headers = {
#     "X-RapidAPI-Key": RAPIDAPI_KEY,
#     "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
# }


# def get_destination_id(city):
#     try:
#         url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

#         params = {
#             "name": city,
#             "locale": "en-gb"
#         }

#         res = requests.get(url, headers=headers, params=params, timeout=10)

#         if res.status_code != 200:
#             print("Location API error:", res.status_code)
#             return None, None

#         data = res.json()

#         if not data:
#             return None, None

#         return data[0]["dest_id"], data[0]["dest_type"]

#     except Exception as e:
#         print("Destination error:", e)
#         return None, None

# GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

# def get_lat_lon(city):
#     url = "https://api.geoapify.com/v1/geocode/search"

#     params = {
#         "text": city,
#         "apiKey": GEOAPIFY_API_KEY
#     }

#     res = requests.get(url, params=params).json()

#     if not res.get("features"):
#         return None, None

#     lat = res["features"][0]["properties"]["lat"]
#     lon = res["features"][0]["properties"]["lon"]

#     return lat, lon


# def get_route_places(source, destination):
#     try:
#         # STEP 1: Convert cities → coordinates
#         geo_url = "https://api.geoapify.com/v1/geocode/search"

#         def get_coords(city):
#             res = requests.get(geo_url, params={
#                 "text": city,
#                 "apiKey": GEOAPIFY_API_KEY
#             }).json()

#             if not res.get("features"):
#                 return None

#             prop = res["features"][0]["properties"]
#             return prop["lon"], prop["lat"]

#         start = get_coords(source)
#         end = get_coords(destination)

#         if not start or not end:
#             print("❌ Geocoding failed")
#             return []

#         # STEP 2: Get route
#         route_url = "https://api.geoapify.com/v1/routing"

#         params = {
#             "waypoints": f"{start[1]},{start[0]}|{end[1]},{end[0]}",
#             "mode": "drive",
#             "apiKey": GEOAPIFY_API_KEY
#         }

#         route_res = requests.get(route_url, params=params).json()

#         if "features" not in route_res:
#             print("❌ Route API error:", route_res)
#             return []

#         coords = route_res["features"][0]["geometry"]["coordinates"]

#         # FIX: flatten nested coordinates
#         if isinstance(coords[0][0], list):
#             coords = coords[0]

#         # STEP 3: Pick sample points (safe)
#         step = max(1, len(coords) // 6)
#         sample_points = coords[::step]

#         places = []
#         seen = set()

#         # STEP 4: Get places near each point
#         for lon, lat in sample_points:

#             places_url = "https://api.geoapify.com/v2/places"

#             params = {
#                 "categories": "tourism.sights,tourism.attraction",
#                 "filter": f"circle:{lon},{lat},4000",
#                 "limit": 2,
#                 "apiKey": GEOAPIFY_API_KEY
#             }

#             res = requests.get(places_url, params=params).json()

#             for item in res.get("features", []):
#                 prop = item["properties"]

#                 name = prop.get("name", "Place")

#                 # avoid duplicates
#                 if name in seen:
#                     continue
#                 seen.add(name)

#                 places.append({
#                     "title": name,
#                     "address": prop.get("formatted", ""),
#                     "lat": prop.get("lat"),
#                     "lon": prop.get("lon"),
#                     "image": f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=400&height=300&center=lonlat:{prop.get('lon')},{prop.get('lat')}&zoom=14&apiKey={GEOAPIFY_API_KEY}"
#                 })

#         return places[:10]

#     except Exception as e:
#         print("❌ Route System Error:", e)
#         return []


# def get_hotels(destination):
#     try:
#         dest_id, dest_type = get_destination_id(destination)

#         if not dest_id:
#             print("❌ No destination found")
#             return []

#         url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

#         params = {
#         "dest_id": dest_id,
#         "dest_type": dest_type,   # dynamic (VERY IMPORTANT)
        
#         "checkin_date": "2026-05-01",
#         "checkout_date": "2026-05-03",
        
#         "adults_number": 2,
#         "room_number": 1,

#         "order_by": "popularity",

#         "locale": "en-gb",
#         "units": "metric",

#         # ✅ REQUIRED FIX
#         "filter_by_currency": "INR"
#         }
#         res = requests.get(url, headers=headers, params=params, timeout=15)

#         if res.status_code != 200:
#             print("❌ Hotel API error:", res.status_code)
#             print(res.text)
#             return []

#         data = res.json()

#         hotels = []

#         for h in data.get("result", [])[:10]:

#             try:
#                 hotels.append({
#                     "name": h.get("hotel_name"),
#                     "price": h.get("min_total_price"),
#                     "rating": h.get("review_score"),
#                     "review": h.get("review_score_word"),
#                     "image": h.get("main_photo_url"),
#                     "address": h.get("address"),
#                     "distance": h.get("distance_to_cc"),
#                     "lat": h.get("latitude"),
#                     "lon": h.get("longitude"),
#                     "url": h.get("url")
#                 })
#             except:
#                 continue

#         return hotels

#     except Exception as e:
#         print("Hotel API crash:", e)
#         return []

#     except Exception as e:
#         print("Hotel error:", e)
#         return []


# def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places):
#     names = [p["title"] for p in route_places]

#     prompt = f"""
#     Create a complete travel plan:

#     From: {source}
#     To: {destination}
#     Days: {days}
#     Budget: {budget_min} to {budget_max} INR
#     Travel Mode: {travel_mode}

#     Include:
#     - Route journey plan
#     - Places between route: {', '.join(names)}
#     - Day-wise itinerary
#     - Budget breakdown (transport + hotel + food)
#     - Travel tips
#     """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text



# # -------- UI -------- #
# import streamlit as st

# st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")

# # ---------- MODERN COMPACT CSS ----------
# st.markdown("""
# <style>

# /* GLOBAL */
# .block-container {
#     padding-top: 1rem;
#     padding-bottom: 1rem;
#     padding-left: 2rem;
#     padding-right: 2rem;
# }

# /* HERO */
# .hero {
#     background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');
#     background-size: cover;
#     background-position: center;
#     height: 220px;
#     border-radius: 18px;
#     position: relative;
#     margin-bottom: 10px;
# }

# .hero-overlay {
#     position: absolute;
#     inset: 0;
#     background: linear-gradient(to right, rgba(0,0,0,0.7), rgba(0,0,0,0.2));
#     border-radius: 18px;
# }

# .hero-text {
#     position: absolute;
#     left: 30px;
#     bottom: 30px;
#     color: white;
# }

# .hero-text h1 {
#     font-size: 32px;
#     margin: 0;
# }

# .hero-text p {
#     margin: 0;
#     opacity: 0.9;
# }

# /* SEARCH BOX */
# .search-box {
#     background: white;
#     padding: 15px;
#     border-radius: 14px;
#     box-shadow: 0 4px 20px rgba(0,0,0,0.08);
#     margin-top: -30px;
# }

# /* INPUTS */
# div[data-baseweb="input"] input {
#     background-color: #f5f7fb !important;
#     border-radius: 10px !important;
#     border: 1px solid #ddd !important;
#     padding: 10px !important;
# }

# /* SELECT BOX */
# div[data-baseweb="select"] {
#     background-color: #f5f7fb !important;
#     border-radius: 10px !important;
# }

# /* SLIDER */
# .stSlider {
#     padding-top: 0px;
# }

# /* BUTTON */
# button[kind="primary"] {
#     background: linear-gradient(90deg, #ff4b4b, #ff7b7b);
#     border-radius: 10px;
#     height: 45px;
#     font-weight: bold;
# }

# /* DESTINATION CARDS */
# .card {
#     border-radius: 12px;
#     overflow: hidden;
#     position: relative;
#     height: 140px;
# }

# .card img {
#     width: 100%;
#     height: 100%;
#     object-fit: cover;
# }

# .card-title {
#     position: absolute;
#     bottom: 10px;
#     left: 10px;
#     color: white;
#     font-weight: bold;
#     background: rgba(0,0,0,0.5);
#     padding: 5px 10px;
#     border-radius: 8px;
# }

# </style>
# """, unsafe_allow_html=True)

# # ---------- HERO ----------
# st.markdown("""
# <div class="hero">
#     <div class="hero-overlay"></div>
#     <div class="hero-text">
#         <h1>🌍 AI Travel Planner Pro</h1>
#         <p>Discover • Plan • Travel ✈️</p>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # ---------- SEARCH BOX ----------
# st.markdown("<div class='search-box'>", unsafe_allow_html=True)

# col1, col2 = st.columns(2)
# with col1:
#     source = st.text_input("From", placeholder="Enter city")
# with col2:
#     destination = st.text_input("To", placeholder="Enter destination")

# col3, col4, col5 = st.columns([1,2,1])

# with col3:
#     days = st.number_input("Days", min_value=1, max_value=15, value=3)

# with col4:
#     budget = st.slider("Budget (₹)", 1000, 100000, (5000, 20000))
#     budget_min, budget_max = budget

# with col5:
#     travel_mode = st.selectbox("Mode", ["🚗 Car", "✈️ Flight", "🚆 Train", "🚌 Bus"])

# generate = st.button("✨ Generate Smart Plan", use_container_width=True)

# st.markdown("</div>", unsafe_allow_html=True)

# # ---------- DESTINATIONS ----------
# st.subheader("🔥 Popular Destinations")

# col1, col2, col3, col4 = st.columns(4)

# destinations = [
#     ("Goa", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"),
#     ("Manali", "https://images.unsplash.com/photo-1501785888041-af3ef285b470"),
#     ("Jaipur", "https://images.unsplash.com/photo-1599661046827-dacff0c0f09c"),
#     ("Kerala", "https://images.unsplash.com/photo-1501785888041-af3ef285b470")
# ]

# for i, (name, img) in enumerate(destinations):
#     with [col1, col2, col3, col4][i]:
#         st.markdown(f"""
#         <div class="card">
#             <img src="{img}">
#             <div class="card-title">📍 {name}</div>
#         </div>
#         """, unsafe_allow_html=True)
# # -------- MAIN -------- #

# if generate and source and destination:

#     with st.spinner("🔍 Planning your smart trip..."):

#         route_places = get_route_places(source, destination)
    
#         hotels = get_hotels(destination)
#         plan = generate_plan(
#             source, destination, days,
#             budget_min, budget_max,
#             travel_mode, route_places
#         )

#     st.success("✅ Trip Ready!")
#     st.markdown(f"""
#     ### ✈️ Trip Overview  
#     **From:** {source} → **To:** {destination}  
#     📅 {days} Days | 💰 ₹{budget_min}-{budget_max} | 🚆 {travel_mode}
#     """)

#     # -------- TABS -------- #
#     tab1, tab2, tab3, tab4 = st.tabs(
#         ["🗺️ Plan", "🛣️ Route Places", "🏨 Hotels", "📊 Summary"]
#     )

#     # -------- PLAN -------- #
#     with tab1:
#         st.subheader("📅 AI Itinerary")
#         for line in plan.split("\n"):
#             if line.strip():
#                 st.markdown(f"- {line}")

#         st.markdown("### 🔗 Booking Platforms")
#         st.markdown("""
#                     - 🛏️ Hotels: [MakeMyTrip](https://www.makemytrip.com), [Booking.com](https://www.booking.com)
#                     - 🚆 Train: [IRCTC](https://www.irctc.co.in)
#                     - 🚌 Bus: [RedBus](https://www.redbus.in)
#                     - ✈️ Flights: [Goibibo](https://www.goibibo.com)
#                             """)
#     # -------- ROUTE PLACES -------- #
#     with tab2:
#         st.subheader("🛣️ Places Between Your Journey")

#         if not route_places:
#             st.warning("⚠️ No route places found")
#         else:
#             cols = st.columns(2)

#             for i, p in enumerate(route_places):
#                 with cols[i % 2]:
#                     st.image(p["image"], width="stretch")
#                     st.markdown(f"""
#                     **📍 {p['title']}**  
#                     {p['address']}
#                     """)
#     # with tab2:
#     #     st.subheader("🛣️ Top Tourist Places")

#     #     if not route_places:
#     #         st.warning("⚠️ No places found")
#     #     else:
#     #         cols = st.columns(3)

#     #         for i, p in enumerate(route_places):

#     #             with cols[i % 3]:

#     #                 st.image(p["image"], width="stretch")

#     #                 st.markdown(f"""
#     #                 <div style="
#     #                     background:white;
#     #                     padding:12px;
#     #                     border-radius:12px;
#     #                     box-shadow:0px 4px 12px rgba(0,0,0,0.15);
#     #                 ">
#     #                     <h4>📍 {p['title']}</h4>
#     #                     <p>{p['address']}</p>
#     #                 </div>
#     #                 """, unsafe_allow_html=True)
#     # -------- HOTELS -------- #
#     with tab3:
#         st.subheader("🏨 Real Hotels (Live Data)")

#         if not hotels:
#             st.warning("⚠️ No hotels found")
#         else:
#             for h in hotels:

#                 col1, col2 = st.columns([1, 2])

#                 with col1:
#                     if h["image"]:
#                         st.image(h["image"], use_container_width=True)

#                 with col2:
#                     st.markdown(f"""
#                     ### 🏨 {h['name']}

#                     ⭐ {h['rating']} / 10 ({h['review']})  
#                     📍 {h['address']}  
#                     📏 {h['distance']} from center  

#                     💰 **₹{h['price']} total stay**
#                     """)

#                     st.markdown(f"[🔘 Book Now]({h['url']})")

#                 st.markdown("---")
                
   

#     # -------- SUMMARY -------- #
#     with tab4:
#         st.subheader("📊 Trip Summary")

#         st.markdown(f"""
#         - 📍 From: {source}  
#         - 🏁 To: {destination}  
#         - 📅 Days: {days}  
#         - 💰 Budget: ₹{budget_min} - ₹{budget_max}  
#         - 🚆 Travel Mode: {travel_mode}  
#         """)

# =======================================================================================================




# import os
# import streamlit as st
# from dotenv import load_dotenv
# from google import genai
# from tavily import TavilyClient
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet
# import requests
# from datetime import datetime, timedelta


# # API setup
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# client = genai.Client(api_key=GOOGLE_API_KEY)
# tavily = TavilyClient(api_key=TAVILY_API_KEY)
# # genai.configure(api_key=GOOGLE_API_KEY)
# # tavily = TavilyClient(api_key=TAVILY_API_KEY)

# # model = genai.GenerativeModel("gemini-2.5-flash")

# # -------- FUNCTIONS -------- #


# RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# headers = {
#     "X-RapidAPI-Key": RAPIDAPI_KEY,
#     "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
# }


# def get_destination_id(city):
#     try:
#         url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

#         params = {
#             "name": city,
#             "locale": "en-gb"
#         }

#         res = requests.get(url, headers=headers, params=params, timeout=10)

#         if res.status_code != 200:
#             print("Location API error:", res.status_code)
#             return None, None

#         data = res.json()

#         if not data:
#             return None, None

#         return data[0]["dest_id"], data[0]["dest_type"]

#     except Exception as e:
#         print("Destination error:", e)
#         return None, None

# GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

# def get_lat_lon(city):
#     url = "https://api.geoapify.com/v1/geocode/search"

#     params = {
#         "text": city,
#         "apiKey": GEOAPIFY_API_KEY
#     }

#     res = requests.get(url, params=params).json()

#     if not res.get("features"):
#         return None, None

#     lat = res["features"][0]["properties"]["lat"]
#     lon = res["features"][0]["properties"]["lon"]

#     return lat, lon


# def get_route_places(source, destination):
#     try:
#         # STEP 1: Convert cities → coordinates
#         geo_url = "https://api.geoapify.com/v1/geocode/search"

#         def get_coords(city):
#             res = requests.get(geo_url, params={
#                 "text": city,
#                 "apiKey": GEOAPIFY_API_KEY
#             }).json()

#             if not res.get("features"):
#                 return None

#             prop = res["features"][0]["properties"]
#             return prop["lon"], prop["lat"]

#         start = get_coords(source)
#         end = get_coords(destination)

#         if not start or not end:
#             print("❌ Geocoding failed")
#             return []

#         # STEP 2: Get route
#         route_url = "https://api.geoapify.com/v1/routing"

#         params = {
#             "waypoints": f"{start[1]},{start[0]}|{end[1]},{end[0]}",
#             "mode": "drive",
#             "apiKey": GEOAPIFY_API_KEY
#         }

#         route_res = requests.get(route_url, params=params).json()

#         if "features" not in route_res:
#             print("❌ Route API error:", route_res)
#             return []

#         coords = route_res["features"][0]["geometry"]["coordinates"]

#         # FIX: flatten nested coordinates
#         if isinstance(coords[0][0], list):
#             coords = coords[0]

#         # STEP 3: Pick sample points (safe)
#         step = max(1, len(coords) // 6)
#         sample_points = coords[::step]

#         places = []
#         seen = set()

#         # STEP 4: Get places near each point
#         for lon, lat in sample_points:

#             places_url = "https://api.geoapify.com/v2/places"

#             params = {
#                 "categories": "tourism.sights,tourism.attraction",
#                 "filter": f"circle:{lon},{lat},4000",
#                 "limit": 2,
#                 "apiKey": GEOAPIFY_API_KEY
#             }

#             res = requests.get(places_url, params=params).json()

#             for item in res.get("features", []):
#                 prop = item["properties"]

#                 name = prop.get("name", "Place")

#                 # avoid duplicates
#                 if name in seen:
#                     continue
#                 seen.add(name)

#                 places.append({
#                     "title": name,
#                     "address": prop.get("formatted", ""),
#                     "lat": prop.get("lat"),
#                     "lon": prop.get("lon"),
#                     "image": f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=400&height=300&center=lonlat:{prop.get('lon')},{prop.get('lat')}&zoom=14&apiKey={GEOAPIFY_API_KEY}"
#                 })

#         return places[:10]

#     except Exception as e:
#         print("❌ Route System Error:", e)
#         return []


# def get_hotels(destination, days, budget_max):
#     try:
#         # ✅ FIXED MIN VALUE
#         budget_min = 1000

#         dest_id, dest_type = get_destination_id(destination)

#         if not dest_id:
#             return []

#         # ✅ AUTO VALID DATES
#         today = datetime.today()
#         checkin = today + timedelta(days=1)
#         checkout = checkin + timedelta(days=max(days, 1))

#         url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

#         params = {
#             "dest_id": dest_id,
#             "dest_type": dest_type,
#             "checkin_date": checkin.strftime("%Y-%m-%d"),
#             "checkout_date": checkout.strftime("%Y-%m-%d"),
#             "adults_number": 2,
#             "room_number": 1,
#             "order_by": "popularity",
#             "locale": "en-gb",
#             "units": "metric",
#             "filter_by_currency": "INR",
#             "currency": "INR"
#         }

#         res = requests.get(url, headers=headers, params=params, timeout=15)

#         if res.status_code != 200:
#             print("API Error:", res.status_code, res.text)
#             return []

#         data = res.json()

#         hotels = []
#         all_hotels = []

#         for h in data.get("result", [])[:40]:

#             price_data = h.get("price_breakdown", {})
#             total_price = price_data.get("gross_price")

#             if not total_price:
#                 continue

#             try:
#                 total_price = float(total_price)
#             except:
#                 continue

#             if total_price <= 0:
#                 continue

#             # ✅ PER NIGHT PRICE ONLY
#             price_per_night = int(total_price / max(days, 1))

#             hotel = {
#                 "name": h.get("hotel_name"),
#                 "price_per_night": price_per_night,
#                 "currency": price_data.get("currency", "INR"),
#                 "rating": h.get("review_score"),
#                 "review": h.get("review_score_word"),
#                 "image": h.get("main_photo_url"),
#                 "address": h.get("address"),
#                 "distance": h.get("distance_to_cc"),
#                 "url": h.get("url")
#             }

#             all_hotels.append(hotel)

#             # ✅ FILTER (ONLY PER NIGHT)
#             if budget_min <= price_per_night <= budget_max:
#                 hotels.append(hotel)

#         # ✅ SMART FALLBACK (NO EMPTY SCREEN)
#         if not hotels:
#             all_hotels.sort(key=lambda x: x["price_per_night"])
#             return all_hotels[:5]

#         return hotels

#     except Exception as e:
#         print("Hotel error:", e)
#         return []
# # from datetime import datetime, timedelta
# # import requests

# # def get_hotels(destination, days, budget_max):
# #     try:
# #         # ✅ FIX MIN VALUE
# #         budget_min = 1000

# #         dest_id, dest_type = get_destination_id(destination)

# #         if not dest_id:
# #             return []

# #         # ✅ AUTO DATES
# #         today = datetime.today()
# #         checkin = today + timedelta(days=1)
# #         checkout = checkin + timedelta(days=max(days, 1))

# #         url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

# #         params = {
# #             "dest_id": dest_id,
# #             "dest_type": dest_type,
# #             "checkin_date": checkin.strftime("%Y-%m-%d"),
# #             "checkout_date": checkout.strftime("%Y-%m-%d"),
# #             "adults_number": 2,
# #             "room_number": 1,
# #             "order_by": "popularity",
# #             "locale": "en-gb",
# #             "units": "metric",
# #             "filter_by_currency": "INR",
# #             "currency": "INR"
# #         }

# #         res = requests.get(url, headers=headers, params=params, timeout=15)

# #         if res.status_code != 200:
# #             print("API Error:", res.status_code, res.text)
# #             return []

# #         data = res.json()

# #         hotels = []
# #         all_hotels = []

# #         for h in data.get("result", [])[:40]:

# #             price_data = h.get("price_breakdown", {})
# #             total_price = price_data.get("gross_price")

# #             if not total_price:
# #                 continue

# #             try:
# #                 total_price = float(total_price)
# #             except:
# #                 continue

# #             if total_price <= 0:
# #                 continue

# #             # ✅ ONLY PER NIGHT PRICE
# #             price_per_night = int(total_price / days)

# #             hotel = {
# #                 "name": h.get("hotel_name"),
# #                 "price_per_night": price_per_night,
# #                 "currency": price_data.get("currency", "INR"),
# #                 "rating": h.get("review_score"),
# #                 "review": h.get("review_score_word"),
# #                 "image": h.get("main_photo_url"),
# #                 "address": h.get("address"),
# #                 "distance": h.get("distance_to_cc"),
# #                 "url": h.get("url")
# #             }

# #             all_hotels.append(hotel)

# #             # ✅ FILTER ONLY PER NIGHT (₹1000 → budget_max)
# #             if 1000 <= price_per_night <= budget_max:
# #                 hotels.append(hotel)

# #         # ✅ fallback if nothing found
# #         if not hotels:
# #             return all_hotels[:5]

# #         return hotels

# #     except Exception as e:
# #         print("Hotel error:", e)
# #         return []
# # from datetime import datetime, timedelta
# # import requests

# # def get_hotels(destination, days, budget_min, budget_max):
# #     try:
# #         dest_id, dest_type = get_destination_id(destination)

# #         if not dest_id:
# #             print("❌ No destination found")
# #             return []

# #         # ✅ AUTO-GENERATE VALID DATES
# #         today = datetime.today()
# #         checkin = today + timedelta(days=1)
# #         checkout = checkin + timedelta(days=days)

# #         url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

# #         params = {
# #             "dest_id": dest_id,
# #             "dest_type": dest_type,

# #             "checkin_date": checkin.strftime("%Y-%m-%d"),
# #             "checkout_date": checkout.strftime("%Y-%m-%d"),

# #             "adults_number": 2,
# #             "room_number": 1,

# #             "order_by": "popularity",
# #             "locale": "en-gb",
# #             "units": "metric",

# #             # ⚠️ sometimes works better than filter_by_currency
# #             "filter_by_currency": "INR",
# #             "currency": "INR"
# #         }

# #         res = requests.get(url, headers=headers, params=params, timeout=15)

# #         if res.status_code != 200:
# #             print("❌ Hotel API error:", res.status_code)
# #             print(res.text)
# #             return []

# #         data = res.json()

# #         hotels = []

# #         # 👉 take more results, then filter
# #         for h in data.get("result", [])[:30]:

# #             # ✅ SAFE PRICE FETCH (better than min_total_price)
# #             price_data = h.get("price_breakdown", {})
# #             total_price = price_data.get("gross_price")

# #             if not total_price:
# #                 continue  # skip invalid price

# #             try:
# #                 total_price = float(total_price)
# #             except:
# #                 continue

# #             # ❌ skip zero or garbage prices
# #             if total_price <= 0:
# #                 continue

# #             # ✅ PRICE PER NIGHT
# #             price_per_night = round(total_price / days, 2) if days > 0 else 0

# #             # ✅ BUDGET FILTER
# #             if total_price < budget_min or total_price > budget_max:
# #                 continue

# #             hotels.append({
# #                 "name": h.get("hotel_name"),
# #                 "total_price": total_price,
# #                 "price_per_night": price_per_night,
# #                 "currency": price_data.get("currency", "INR"),
# #                 "rating": h.get("review_score"),
# #                 "review": h.get("review_score_word"),
# #                 "image": h.get("main_photo_url"),
# #                 "address": h.get("address"),
# #                 "distance": h.get("distance_to_cc"),
# #                 "lat": h.get("latitude"),
# #                 "lon": h.get("longitude"),
# #                 "url": h.get("url")
# #             })

# #         return hotels

# #     except Exception as e:
# #         print("❌ Hotel error:", e)
# #         return []
# # from datetime import datetime, timedelta
# # import requests

# # def get_hotels(destination, days):
# #     try:
# #         dest_id, dest_type = get_destination_id(destination)

# #         if not dest_id:
# #             print("❌ No destination found")
# #             return []

# #         # ✅ Safe days
# #         days = max(days, 1)

# #         # ✅ AUTO DATES (REQUIRED BY API)
# #         today = datetime.today()
# #         checkin = today + timedelta(days=1)
# #         checkout = checkin + timedelta(days=days)

# #         url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

# #         params = {
# #             "dest_id": dest_id,
# #             "dest_type": dest_type,
# #             "checkin_date": checkin.strftime("%Y-%m-%d"),
# #             "checkout_date": checkout.strftime("%Y-%m-%d"),
# #             "adults_number": 2,
# #             "room_number": 1,
# #             "order_by": "popularity",
# #             "locale": "en-gb",
# #             "units": "metric",
# #             "filter_by_currency": "INR"
# #         }

# #         res = requests.get(url, headers=headers, params=params, timeout=15)

# #         if res.status_code != 200:
# #             print("❌ Hotel API error:", res.status_code)
# #             print(res.text)
# #             return []

# #         data = res.json()

# #         hotels = []

# #         for h in data.get("result", [])[:15]:

# #             # ✅ Better price extraction
# #             price_data = h.get("price_breakdown", {})
# #             total_price = price_data.get("gross_price")

# #             if not total_price:
# #                 continue

# #             try:
# #                 total_price = float(total_price)
# #             except:
# #                 continue

# #             if total_price <= 0:
# #                 continue

# #             # ✅ PER NIGHT CALCULATION
# #             price_per_night = int(total_price / days)

# #             hotels.append({
# #                 "name": h.get("hotel_name"),
# #                 "price_per_night": price_per_night,   # 🔥 IMPORTANT
# #                 "rating": h.get("review_score"),
# #                 "review": h.get("review_score_word"),
# #                 "image": h.get("main_photo_url"),
# #                 "address": h.get("address"),
# #                 "distance": h.get("distance_to_cc"),
# #                 "lat": h.get("latitude"),
# #                 "lon": h.get("longitude"),
# #                 "url": h.get("url")
# #             })

# #         return hotels

# #     except Exception as e:
# #         print("Hotel error:", e)
# #         return []
# # from datetime import datetime, timedelta

# # def get_hotels(destination, days):
# #     try:
# #         dest_id, dest_type = get_destination_id(destination)

# #         if not dest_id:
# #             print("❌ No destination found")
# #             return []

# #         # 👉 AUTO-GENERATE DATES (user doesn't see this)
# #         today = datetime.today()
# #         checkin = today + timedelta(days=1)
# #         checkout = checkin + timedelta(days=days)

# #         url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

# #         params = {
# #             "dest_id": dest_id,
# #             "dest_type": dest_type,

# #             "checkin_date": checkin.strftime("%Y-%m-%d"),
# #             "checkout_date": checkout.strftime("%Y-%m-%d"),

# #             "adults_number": 2,
# #             "room_number": 1,
# #             "order_by": "popularity",
# #             "locale": "en-gb",
# #             "units": "metric",
# #             "filter_by_currency": "INR"
# #         }

# #         res = requests.get(url, headers=headers, params=params, timeout=15)

# #         if res.status_code != 200:
# #             print("❌ Hotel API error:", res.status_code)
# #             print(res.text)
# #             return []

# #         data = res.json()

# #         hotels = []
# #         for h in data.get("result", [])[:10]:
# #             hotels.append({
# #                 "name": h.get("hotel_name"),
# #                 "price": h.get("min_total_price"),
# #                 "rating": h.get("review_score"),
# #                 "review": h.get("review_score_word"),
# #                 "image": h.get("main_photo_url"),
# #                 "address": h.get("address"),
# #                 "distance": h.get("distance_to_cc"),
# #                 "lat": h.get("latitude"),
# #                 "lon": h.get("longitude"),
# #                 "url": h.get("url")
# #             })

# #         return hotels

# #     except Exception as e:
# #         print("Hotel error:", e)
# #         return []
# # def get_hotels(destination):
# #     try:
# #         dest_id, dest_type = get_destination_id(destination)

# #         if not dest_id:
# #             print("❌ No destination found")
# #             return []

# #         url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

# #         params = {
# #         "dest_id": dest_id,
# #         "dest_type": dest_type,   # dynamic (VERY IMPORTANT)
        
# #         "checkin_date": "2026-05-01",
# #         "checkout_date": "2026-05-03",
        
# #         "adults_number": 2,
# #         "room_number": 1,

# #         "order_by": "popularity",

# #         "locale": "en-gb",
# #         "units": "metric",

# #         # ✅ REQUIRED FIX
# #         "filter_by_currency": "INR"
# #         }
# #         res = requests.get(url, headers=headers, params=params, timeout=15)

# #         if res.status_code != 200:
# #             print("❌ Hotel API error:", res.status_code)
# #             print(res.text)
# #             return []

# #         data = res.json()

# #         hotels = []

# #         for h in data.get("result", [])[:10]:

# #             try:
# #                 hotels.append({
# #                     "name": h.get("hotel_name"),
# #                     "price": h.get("min_total_price"),
# #                     "rating": h.get("review_score"),
# #                     "review": h.get("review_score_word"),
# #                     "image": h.get("main_photo_url"),
# #                     "address": h.get("address"),
# #                     "distance": h.get("distance_to_cc"),
# #                     "lat": h.get("latitude"),
# #                     "lon": h.get("longitude"),
# #                     "url": h.get("url")
# #                 })
# #             except:
# #                 continue

# #         return hotels

# #     except Exception as e:
# #         print("Hotel API crash:", e)
# #         return []

# #     except Exception as e:
# #         print("Hotel error:", e)
# #         return []


# def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places):
#     names = [p["title"] for p in route_places]

#     prompt = f"""
#     Create a complete travel plan:

#     From: {source}
#     To: {destination}
#     Days: {days}
#     Budget: {budget_min} to {budget_max} INR
#     Travel Mode: {travel_mode}

#     Include:
#     - Route journey plan
#     - Places between route: {', '.join(names)}
#     - Day-wise itinerary
#     - Budget breakdown (transport + hotel + food)
#     - Travel tips
#     """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text



# # -------- UI -------- #

# st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")

# # ---------- HIDE STREAMLIT DEFAULT ----------
# st.markdown("""
# <style>
# #MainMenu {visibility: hidden;}
# header {visibility: hidden;}
# footer {visibility: hidden;}
# </style>
# """, unsafe_allow_html=True)

# # ---------- PREMIUM CSS ----------
# st.markdown("""
# <style>

# /* GLOBAL */
# .block-container {
#     padding-top: 0rem;
#     padding-left: 2rem;
#     padding-right: 2rem;
# }

# /* NAVBAR */
# .navbar {
#     position: sticky;
#     top: 0;
#     z-index: 999;
#     background: white;
#     padding: 12px 25px;
#     border-radius: 0 0 12px 12px;
#     display: flex;
#     justify-content: space-between;
#     box-shadow: 0 4px 15px rgba(0,0,0,0.08);
# }

# .logo {
#     font-weight: bold;
#     font-size: 20px;
#     color: #ff4b4b;
# }

# /* HERO */
# .hero {
#     height: 260px;
#     border-radius: 20px;
#     margin-top: 10px;
#     background-size: cover;
#     background-position: center;
#     animation: slide 12s infinite;
#     position: relative;
# }

# @keyframes slide {
#     0% {background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');}
#     33% {background-image: url('https://images.unsplash.com/photo-1501785888041-af3ef285b470');}
#     66% {background-image: url('https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1');}
#     100% {background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');}
# }

# .hero::after {
#     content: "";
#     position: absolute;
#     inset: 0;
#     background: rgba(0,0,0,0.5);
#     border-radius: 20px;
# }

# .hero-text {
#     position: absolute;
#     bottom: 30px;
#     left: 30px;
#     color: white;
#     z-index: 2;
# }

# .hero-text h1 {
#     margin: 0;
#     font-size: 34px;
# }

# /* SEARCH BOX */
# .search-box {
#     margin-top: -40px;
#     background: white;
#     padding: 18px;
#     border-radius: 18px;
#     box-shadow: 0 10px 30px rgba(0,0,0,0.1);
# }

# /* INPUTS ALIGN FIX */
# div[data-baseweb="input"], div[data-baseweb="select"] {
#     margin-top: -6px;
# }

# /* INPUT STYLE */
# div[data-baseweb="input"] input {
#     background: #f3f6fb !important;
#     border-radius: 10px !important;
#     border: none !important;
# }

# div[data-baseweb="select"] {
#     background: #f3f6fb !important;
#     border-radius: 10px !important;
# }

# /* BUTTON */
# button[kind="primary"] {
#     background: linear-gradient(90deg, #ff4b4b, #ff7b7b);
#     border-radius: 12px;
#     height: 48px;
#     font-weight: 600;
# }

# /* CARDS */
# .card {
#     border-radius: 14px;
#     overflow: hidden;
#     height: 160px;
#     position: relative;
#     transition: 0.3s;
# }

# .card:hover {
#     transform: scale(1.05);
# }

# .card img {
#     width: 100%;
#     height: 100%;
#     object-fit: cover;
# }

# .card-title {
#     position: absolute;
#     bottom: 10px;
#     left: 10px;
#     color: white;
#     font-weight: bold;
#     background: rgba(0,0,0,0.6);
#     padding: 6px 12px;
#     border-radius: 8px;
# }

# </style>
# """, unsafe_allow_html=True)

# # ---------- NAVBAR ----------
# st.markdown("""
# <div class="navbar">
#     <div class="logo">🌍 TravelAI</div>
#     <div>Flights | Hotels | Packages</div>
# </div>
# """, unsafe_allow_html=True)

# # ---------- HERO ----------
# st.markdown("""
# <div class="hero">
#     <div class="hero-text">
#         <h1>AI Travel Planner Pro</h1>
#         <p>Plan smarter journeys with AI ✈️</p>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # ---------- SEARCH ----------
# st.markdown("<div class='search-box'>", unsafe_allow_html=True)

# # ROW 1
# c1, c2 = st.columns(2)
# with c1:
#     source = st.text_input("From", placeholder="Enter city")

# with c2:
#     destination = st.text_input("To", placeholder="Enter destination")

# # ROW 2 (FIXED ALIGNMENT)
# c3, c4, c5 = st.columns([1,2,1])

# with c3:
#     st.markdown("**Days**")
#     days = st.number_input("Days", 1, 15, 3, label_visibility="collapsed")

# with c4:
#     st.markdown("**💰 Budget (₹)**")

#     b1, b2 = st.columns(2)

#     with b1:
#         budget_min = st.number_input(
#             "Min",
#             min_value=0,
#             value=5000,
#             step=1000,
#             label_visibility="collapsed"
#         )

#     with b2:
#         budget_max = st.number_input(
#             "Max",
#             min_value=0,
#             value=20000,
#             step=1000,
#             label_visibility="collapsed"
#         )

#     if budget_min > budget_max:
#         st.warning("⚠️ Min should be less than Max")

# with c5:
#     st.markdown("**Mode**")
#     travel_mode = st.selectbox(
#         "Travel Mode",
#         ["🚗 Car", "✈️ Flight", "🚆 Train", "🚌 Bus"],
#         label_visibility="collapsed"
#     )

# generate = st.button("✨ Generate Plan", use_container_width=True)

# st.markdown("</div>", unsafe_allow_html=True)

# # ---------- DESTINATIONS ----------
# st.markdown("## 🔥 Popular Destinations")

# cols = st.columns(4)

# destinations = [
#     ("Goa", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"),
#     ("Manali", "https://images.unsplash.com/photo-1501785888041-af3ef285b470"),
#     ("Jaipur", "https://images.unsplash.com/photo-1548013146-72479768bada"),
#     ("Kerala", "https://images.unsplash.com/photo-1593693411515-c20261bcad6e")
# ]

# for i, (name, img) in enumerate(destinations):
#     with cols[i]:
#         st.markdown(f"""
#         <div class="card">
#             <img src="{img}">
#             <div class="card-title">{name}</div>
#         </div>
#         """, unsafe_allow_html=True)
# # -------- MAIN -------- #

# if generate and source and destination:

#     with st.spinner("🔍 Planning your smart trip..."):

#         route_places = get_route_places(source, destination)
    
#         # hotels = get_hotels(destination)
#         # hotels = get_hotels(destination, days)
#         # hotels = get_hotels(destination, days, budget_min or 0, budget_max or 100000)
#         hotels = get_hotels(destination, days, budget_max)
#         plan = generate_plan(
#             source, destination, days,
#             budget_min, budget_max,
#             travel_mode, route_places
#         )

#     st.success("✅ Trip Ready!")
#     st.markdown(f"""
#     ### ✈️ Trip Overview  
#     **From:** {source} → **To:** {destination}  
#     📅 {days} Days | 💰 ₹{budget_min}-{budget_max} | 🚆 {travel_mode}
#     """)

#     # -------- TABS -------- #
#     tab1, tab2, tab3, tab4 = st.tabs(
#         ["🗺️ Plan", "🛣️ Route Places", "🏨 Hotels", "📊 Summary"]
#     )

#     # -------- PLAN -------- #
#     with tab1:
#         st.subheader("📅 AI Itinerary")
#         for line in plan.split("\n"):
#             if line.strip():
#                 st.markdown(f"- {line}")

#         st.markdown("### 🔗 Booking Platforms")
#         st.markdown("""
#                     - 🛏️ Hotels: [MakeMyTrip](https://www.makemytrip.com), [Booking.com](https://www.booking.com)
#                     - 🚆 Train: [IRCTC](https://www.irctc.co.in)
#                     - 🚌 Bus: [RedBus](https://www.redbus.in)
#                     - ✈️ Flights: [Goibibo](https://www.goibibo.com)
#                             """)
#     # -------- ROUTE PLACES -------- #
#     with tab2:
#         st.subheader("🛣️ Places Between Your Journey")

#         if not route_places:
#             st.warning("⚠️ No route places found")
#         else:
#             cols = st.columns(2)

#             for i, p in enumerate(route_places):
#                 with cols[i % 2]:
#                     st.image(p["image"], width="stretch")
#                     st.markdown(f"""
#                     **📍 {p['title']}**  
#                     {p['address']}
#                     """)

#     # -------- HOTELS -------- #
#     with tab3:
#         st.subheader("🏨 Real Hotels (Live Data)")

#         if not hotels:
#             st.warning("⚠️ No hotels found in your budget. Try increasing budget.")
#         else:
#             for h in hotels:

#                 col1, col2 = st.columns([1, 2])

#                 with col1:
#                     if h.get("image"):
#                         st.image(h["image"], width="stretch")

#                 with col2:
#                     price = h.get("price_per_night", "N/A")

#                     st.markdown(f"""
#                     ### 🏨 {h.get('name', 'Hotel')}

#                     ⭐ {h.get('rating', 'N/A')} / 10 ({h.get('review', '')})  
#                     📍 {h.get('address', 'No address')}  
#                     📏 {h.get('distance', 'N/A')} from center  

#                     💰 **₹{price} / night**
#                     """)

#                     if h.get("url"):
#                         st.markdown(f"[🔘 Book Now]({h['url']})")

#                 st.markdown("---")
#     # with tab3:
#     #     st.subheader("🏨 Real Hotels (Live Data)")

#     #     if not hotels:
#     #         st.warning("⚠️ No hotels found in your budget. Try increasing budget.")
#     #     else:
#     #         for h in hotels:

#     #             col1, col2 = st.columns([1, 2])

#     #             with col1:
#     #                 if h["image"]:
#     #                     st.image(h["image"], use_container_width=True)

#     #             with col2:
#     #                 st.markdown(f"""
#     #                 ### 🏨 {h['name']}

#     #                 ⭐ {h['rating']} / 10 ({h['review']})  
#     #                 📍 {h['address']}  
#     #                 📏 {h['distance']} from center  

#     #                 💰 **₹{h['price_per_night']} / night**
#     #                 """)

#     #                 st.markdown(f"[🔘 Book Now]({h['url']})")

#     #             st.markdown("---")

#     # with tab3:
#     #     st.subheader("🏨 Real Hotels (Live Data)")

#     #     if not hotels:
#     #         st.warning("⚠️ No hotels found in your budget. Try increasing budget.")
#     #     else:
#     #         for h in hotels:

#     #             col1, col2 = st.columns([1, 2])

#     #             with col1:
#     #                 if h.get("image"):
#     #                     st.image(h["image"], use_container_width=True)

#     #             with col2:
#     #                 # ✅ SAFE VALUES
#     #                 name = h.get("name", "Hotel")
#     #                 rating = h.get("rating", "N/A")
#     #                 review = h.get("review", "")
#     #                 address = h.get("address", "Location not available")
#     #                 distance = h.get("distance", "N/A")
#     #                 total_price = h.get("total_price", "N/A")
#     #                 per_night = h.get("price_per_night", "N/A")
#     #                 currency = h.get("currency", "₹")

#     #                 st.markdown(f"""
#     #                 ### 🏨 {name}

#     #                 ⭐ {rating} / 10 ({review})  
#     #                 📍 {address}  
#     #                 📏 {distance} from center  

#     #                 💰 **{currency} {total_price} total stay**  
#     #                 🌙 **{currency} {per_night} per night**
#     #                 """)

#     #                 if h.get("url"):
#     #                     st.markdown(f"[🔘 Book Now]({h['url']})")

#     #             st.markdown("---")
#     # with tab3:
#     #     st.subheader("🏨 Real Hotels (Live Data)")

#     #     if not hotels:
#     #         st.warning("⚠️ No hotels found")
#     #     else:
#     #         for h in hotels:

#     #             col1, col2 = st.columns([1, 2])

#     #             with col1:
#     #                 if h["image"]:
#     #                     st.image(h["image"], use_container_width=True)

#     #             with col2:
#     #                 st.markdown(f"""
#     #                 ### 🏨 {h['name']}

#     #                 ⭐ {h['rating']} / 10 ({h['review']})  
#     #                 📍 {h['address']}  
#     #                 📏 {h['distance']} from center  

#     #                 💰 **₹{h['price']} total stay**
#     #                 """)

#     #                 st.markdown(f"[🔘 Book Now]({h['url']})")

#     #             st.markdown("---")
                
   

#     # -------- SUMMARY -------- #
#     with tab4:
#         st.subheader("📊 Trip Summary")

#         st.markdown(f"""
#         - 📍 From: {source}  
#         - 🏁 To: {destination}  
#         - 📅 Days: {days}  
#         - 💰 Budget: ₹{budget_min} - ₹{budget_max}  
#         - 🚆 Travel Mode: {travel_mode}  
#         """)

# ====================================================================================================================================================
# ===============================================================================================================================================================

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
        res = requests.get(
            "https://booking-com.p.rapidapi.com/v1/hotels/locations",
            headers=headers, params={"name": city, "locale": "en-gb"}, timeout=10
        )
        if res.status_code != 200: return None, None
        data = res.json()
        return (data[0]["dest_id"], data[0]["dest_type"]) if data else (None, None)
    except: return None, None


def get_route_places(source, destination):
    try:
        geo_url = "https://api.geoapify.com/v1/geocode/search"
        def get_coords(city):
            res = requests.get(geo_url, params={"text": city, "apiKey": GEOAPIFY_API_KEY}).json()
            if not res.get("features"): return None
            p = res["features"][0]["properties"]
            return p["lon"], p["lat"]
        start = get_coords(source)
        end   = get_coords(destination)
        if not start or not end: return []
        rr = requests.get("https://api.geoapify.com/v1/routing", params={
            "waypoints": f"{start[1]},{start[0]}|{end[1]},{end[0]}",
            "mode": "drive", "apiKey": GEOAPIFY_API_KEY
        }).json()
        if "features" not in rr: return []
        coords = rr["features"][0]["geometry"]["coordinates"]
        if isinstance(coords[0][0], list): coords = coords[0]
        step = max(1, len(coords) // 6)
        places, seen = [], set()
        for lon, lat in coords[::step]:
            res = requests.get("https://api.geoapify.com/v2/places", params={
                "categories": "tourism.sights,tourism.attraction",
                "filter": f"circle:{lon},{lat},4000", "limit": 2, "apiKey": GEOAPIFY_API_KEY
            }).json()
            for item in res.get("features", []):
                prop = item["properties"]
                name = prop.get("name", "Place")
                if name in seen: continue
                seen.add(name)
                places.append({
                    "title": name, "address": prop.get("formatted", ""),
                    "image": f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=400&height=300&center=lonlat:{prop.get('lon')},{prop.get('lat')}&zoom=14&apiKey={GEOAPIFY_API_KEY}"
                })
        return places[:10]
    except: return []

def get_hotels(destination, days, budget_max):
    try:
        dest_id, dest_type = get_destination_id(destination)
        if not dest_id:
            st.warning(f"⚠️ Could not find destination: {destination}")
            return []

        today    = datetime.today()
        checkin  = today + timedelta(days=1)
        checkout = checkin + timedelta(days=max(days, 1))

        res = requests.get(
            "https://booking-com.p.rapidapi.com/v1/hotels/search",
            headers=headers,
            params={
                "dest_id":          dest_id,
                "dest_type":        dest_type,
                "checkin_date":     checkin.strftime("%Y-%m-%d"),
                "checkout_date":    checkout.strftime("%Y-%m-%d"),
                "adults_number":    2,
                "room_number":      1,
                "order_by":         "popularity",
                "locale":           "en-gb",
                "units":            "metric",
                "filter_by_currency": "INR",
                "currency":         "INR",
                "page_number":      0,
            },
            timeout=20
        )

        if res.status_code != 200:
            print(f"Hotel API error: {res.status_code} — {res.text[:300]}")
            return []

        results = res.json().get("result", [])
        
        if not results:
            print("No results from API")
            return []

        hotels = []

        for h in results[:30]:
            
            # Try multiple price fields
            price = None
            
            # Method 1: price_breakdown
            pb = h.get("price_breakdown", {})
            if pb:
                price = pb.get("gross_price") or pb.get("all_inclusive_price")
            
            # Method 2: min_total_price
            if not price:
                price = h.get("min_total_price")
            
            # Method 3: composite_price_breakdown
            if not price:
                cpb = h.get("composite_price_breakdown", {})
                gp  = cpb.get("gross_amount_per_night", {})
                price = gp.get("value")

            # Skip if still no price
            if not price:
                continue

            try:
                price = float(price)
            except:
                continue

            if price <= 0:
                continue

            # Calculate per night
            price_per_night = int(price / max(days, 1))

            hotels.append({
                "name":           h.get("hotel_name", "Unknown Hotel"),
                "price_per_night": price_per_night,
                "total_price":    int(price),
                "rating":         h.get("review_score", "N/A"),
                "review":         h.get("review_score_word", ""),
                "image":          h.get("main_photo_url", ""),
                "address":        h.get("address", ""),
                "city":           h.get("city", destination),
                "distance":       h.get("distance_to_cc", "N/A"),
                "url":            h.get("url", "#"),
            })

        # if not hotels:
            # return []
        # DEBUG — remove after testing
        if not hotels:
            st.error(f"Debug: dest={destination}, days={days}, budget_max={budget_max}")

        # Sort by price
        hotels.sort(key=lambda x: x["price_per_night"])

        # Filter by budget — generous range
        filtered = [h for h in hotels if h["price_per_night"] <= budget_max]

        # If nothing fits budget, return cheapest 5
        return filtered[:8] if filtered else hotels[:5]

    except Exception as e:
        print(f"Hotel function error: {e}")
        import traceback
        traceback.print_exc()
        return []
# def get_hotels(destination, days, budget_max):
#     try:
#         dest_id, dest_type = get_destination_id(destination)
#         if not dest_id: return []
#         today   = datetime.today()
#         checkin = today + timedelta(days=1)
#         checkout= checkin + timedelta(days=max(days, 1))
#         res = requests.get("https://booking-com.p.rapidapi.com/v1/hotels/search", headers=headers, params={
#             "dest_id": dest_id, "dest_type": dest_type,
#             "checkin_date": checkin.strftime("%Y-%m-%d"),
#             "checkout_date": checkout.strftime("%Y-%m-%d"),
#             "adults_number": 2, "room_number": 1,
#             "order_by": "popularity", "locale": "en-gb",
#             "units": "metric", "filter_by_currency": "INR", "currency": "INR"
#         }, timeout=15)
#         if res.status_code != 200: return []
#         hotels, all_h = [], []
#         for h in res.json().get("result", [])[:40]:
#             pd_ = h.get("price_breakdown", {})
#             tp  = pd_.get("gross_price")
#             if not tp: continue
#             try: tp = float(tp)
#             except: continue
#             if tp <= 0: continue
#             ppn = int(tp / max(days, 1))
#             hotel = {
#                 "name": h.get("hotel_name"), "price_per_night": ppn,
#                 "rating": h.get("review_score"), "review": h.get("review_score_word"),
#                 "image": h.get("main_photo_url"), "address": h.get("address"),
#                 "distance": h.get("distance_to_cc"), "url": h.get("url")
#             }
#             all_h.append(hotel)
#             if 1000 <= ppn <= budget_max: hotels.append(hotel)
#         if not hotels:
#             all_h.sort(key=lambda x: x["price_per_night"])
#             return all_h[:5]
#         return hotels
#     except: return []


# def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places):
#     names = [p["title"] for p in route_places]
#     response = client.models.generate_content(model="gemini-2.5-flash", contents=f"""
#     Create a complete travel plan:
#     From: {source} | To: {destination} | Days: {days}
#     Budget: Rs.{budget_min} to Rs.{budget_max} | Mode: {travel_mode}
#     Include: Route plan, Places: {', '.join(names)}, Day-wise itinerary, Budget breakdown, Travel tips
#     """)
#     return response.text
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

# ─────────────────────────────────────────
# CSS  — hero uses background-image (NO <img> tags — that's what caused raw HTML display)
# ─────────────────────────────────────────

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
/* ── RESET ── */
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

/* ══════════════════════════════
   FIXED NAVBAR
══════════════════════════════ */
.v-nav{
  position:fixed;top:0;left:0;right:0;z-index:9999;
  background:rgba(255,255,255,0.96);
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  border-bottom:1px solid var(--border);
  height:64px;display:flex;align-items:center;
  justify-content:space-between;padding:0 48px;
  box-shadow:0 1px 0 var(--border),0 4px 16px rgba(26,23,20,0.04);
}
.v-logo{
  font-family:var(--ff-head);font-size:22px;font-weight:700;
  color:var(--ink);letter-spacing:-0.5px;
  display:flex;align-items:center;gap:8px;
}
.v-logo span{color:var(--accent);font-family:var(--ff-head);}
.v-nav-links{display:flex;gap:36px;font-size:13.5px;font-weight:500;color:var(--ink-soft);align-items:center;}
.v-nav-links a{color:var(--ink-soft);text-decoration:none;transition:color 0.2s;}
.v-nav-links a:hover{color:var(--accent);}
.v-nav-cta{
  background:var(--ink);color:var(--white)!important;
  padding:9px 22px;border-radius:99px;
  font-size:13px;font-weight:500;text-decoration:none;transition:background 0.2s;
}
.v-nav-cta:hover{background:var(--accent)!important;}
.v-spacer{height:64px;}

/* ══════════════════════════════
   HERO  — CSS background-image slider (no <img> tags!)
   Streamlit strips <img> inside markdown but leaves
   background-image in <style> completely untouched.
══════════════════════════════ */
.v-hero{
  position:relative;
  height:560px;
  overflow:hidden;
  background:#1A1714;   /* fallback while images load */
}

/* The 4 slide divs — each is position:absolute, opacity toggled by CSS animation */
.v-slide{
  position:absolute;inset:0;
  background-size:cover;
  background-position:center 40%;
  opacity:0;
  transition:opacity 1.2s ease-in-out;
}
/* Each slide fades in for ~5s out of a 20s cycle */
.v-s1{
  background-image:url('https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1600&q=80');
  animation:fade4 20s 0s infinite;
}
.v-s2{
  background-image:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&q=80');
  animation:fade4 20s 5s infinite;
}
.v-s3{
  background-image:url('https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1600&q=80');
  animation:fade4 20s 10s infinite;
}
.v-s4{
  background-image:url('https://images.unsplash.com/photo-1548013146-72479768bada?w=1600&q=80');
  animation:fade4 20s 15s infinite;
}

@keyframes fade4{
  0%   {opacity:0;}
  5%   {opacity:1;}
  25%  {opacity:1;}
  30%  {opacity:0;}
  100% {opacity:0;}
}

/* Dark gradient on top of slides */
.v-hero-overlay{
  position:absolute;inset:0;z-index:2;
  background:linear-gradient(
    to top,
    rgba(26,23,20,0.88) 0%,
    rgba(26,23,20,0.45) 45%,
    rgba(26,23,20,0.10) 100%
  );
}

/* Hero text */
.v-hero-text{
  position:absolute;bottom:0;left:0;right:0;
  z-index:3;padding:0 56px 56px;
  pointer-events:none;
}
.v-hero-tag{
  display:inline-flex;align-items:center;gap:7px;
  background:rgba(255,255,255,0.13);
  backdrop-filter:blur(8px);
  border:1px solid rgba(255,255,255,0.26);
  color:white;font-size:11.5px;font-weight:500;
  letter-spacing:1.4px;text-transform:uppercase;
  padding:7px 16px;border-radius:99px;margin-bottom:18px;
}
.v-hero-tag::before{
  content:"";width:7px;height:7px;
  background:#4ade80;border-radius:50%;
  animation:blink 2s infinite;
}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.4;}}
.v-hero-text h1{
  font-family:var(--ff-head);font-size:54px;font-weight:700;
  color:white;line-height:1.08;letter-spacing:-1.5px;margin-bottom:14px;
  text-shadow:0 2px 20px rgba(0,0,0,.3);
}
.v-hero-text h1 em{font-style:italic;color:var(--gold);}
.v-hero-text p{
  font-size:16px;color:rgba(255,255,255,0.76);
  font-weight:300;line-height:1.6;max-width:560px;
}

/* Animated indicator dots */
.v-dots{
  position:absolute;bottom:22px;right:48px;
  z-index:4;display:flex;gap:8px;align-items:center;
}
.v-dot{width:8px;height:8px;border-radius:99px;background:rgba(255,255,255,0.35);}
.v-dot.d1{animation:dot1 20s 0s  infinite;}
.v-dot.d2{animation:dot1 20s 5s  infinite;}
.v-dot.d3{animation:dot1 20s 10s infinite;}
.v-dot.d4{animation:dot1 20s 15s infinite;}
@keyframes dot1{
  0%,4%   {background:white;width:22px;}
  30%,100%{background:rgba(255,255,255,0.35);width:8px;}
}

/* ══════════════════════════════
   SEARCH CARD  (floats below hero)
══════════════════════════════ */
.v-search-wrap{
  padding:0 40px;
  margin-top:-48px;
  position:relative;z-index:50;
}
.v-search-panel{
  background:var(--white);
  border-radius:20px;
  border:1px solid var(--border);
  box-shadow:var(--shadow-lg);
  padding:26px 32px 22px;
}
.v-search-eyebrow{
  font-size:16px;font-weight:700;letter-spacing:1.6px;
  text-transform:uppercase;color:var(--ink-soft);
  margin-bottom:18px;display:flex;align-items:center;gap:10px;
}
.v-search-eyebrow::before{
  content:'';width:24px;height:2px;
  background:var(--accent);border-radius:2px;display:inline-block;
}
.v-field-label{
  font-size:12px;font-weight:700;letter-spacing:1px;
  text-transform:uppercase;color:var(--ink-soft);
  margin-bottom:6px;display:block;
}

/* ── INPUTS ── */
div[data-baseweb="input"] input{
  background:var(--cream)!important;
  border:1.5px solid var(--border)!important;
  border-radius:10px!important;
  font-family:var(--ff-body)!important;
  font-size:15px!important;color:var(--ink)!important;
  height:48px!important;padding:0 16px!important;
  transition:border-color .2s,box-shadow .2s!important;
}
div[data-baseweb="input"] input:focus{
  border-color:var(--accent)!important;
  background:white!important;
  box-shadow:0 0 0 3px rgba(196,98,45,0.11)!important;
}
div[data-baseweb="select"]>div{
  background:var(--cream)!important;
  border:1.5px solid var(--border)!important;
  border-radius:10px!important;
  font-family:var(--ff-body)!important;
  font-size:15px!important;min-height:48px!important;
}
div[data-testid="stNumberInput"] input{
  background:var(--cream)!important;
  border:1.5px solid var(--border)!important;
  border-radius:10px!important;
  font-size:15px!important;height:48px!important;
}

/* ── BUTTON ── */
div[data-testid="stButton"]>button{
  background:var(--accent)!important;color:white!important;
  border:none!important;border-radius:12px!important;
  font-family:var(--ff-body)!important;font-size:15.5px!important;
  font-weight:700!important;height:52px!important;
  letter-spacing:.4px!important;transition:all .2s!important;
  box-shadow:0 4px 18px rgba(196,98,45,0.32)!important;
}
div[data-testid="stButton"]>button:hover{
  background:#b05527!important;
  transform:translateY(-1px)!important;
  box-shadow:0 7px 24px rgba(196,98,45,0.42)!important;
}
div[data-testid="stButton"]>button:active{transform:translateY(0)!important;}

/* ── TABS ── */
div[data-baseweb="tab-list"]{
  background:var(--cream)!important;border-radius:12px!important;
  padding:4px!important;gap:2px!important;border:1px solid var(--border)!important;
}
button[data-baseweb="tab"]{
  font-family:var(--ff-body)!important;font-size:13.5px!important;
  font-weight:500!important;border-radius:9px!important;
  color:var(--ink-soft)!important;padding:9px 20px!important;transition:all .2s!important;
}
button[data-baseweb="tab"][aria-selected="true"]{
  background:var(--white)!important;color:var(--accent)!important;
  font-weight:700!important;box-shadow:0 1px 8px rgba(26,23,20,0.08)!important;
}
div[data-baseweb="tab-highlight"],div[data-baseweb="tab-border"]{display:none!important;}

/* ── SECTIONS ── */
.v-section{padding:40px 40px 16px;}
.v-section-head{display:flex;align-items:baseline;gap:12px;margin-bottom:22px;}
.v-section-head h2{
  font-family:var(--ff-head);font-size:26px;font-weight:600;
  color:var(--ink);letter-spacing:-0.4px;
}
.v-section-head span{font-size:13px;color:var(--ink-soft);}

/* ── DEST CARDS — background-image, no <img> ── */
.v-dest-card{
  border-radius:14px;overflow:hidden;
  height:210px;position:relative;cursor:pointer;
  background-size:cover;background-position:center;
  transition:transform .3s cubic-bezier(.34,1.56,.64,1);
}
.v-dest-card:hover{transform:translateY(-5px);}
.v-dest-gradient{
  position:absolute;inset:0;
  background:linear-gradient(to top,rgba(26,23,20,0.76) 0%,transparent 55%);
}
.v-dest-info{position:absolute;bottom:0;left:0;right:0;padding:16px;}
.v-dest-name{font-family:var(--ff-head);font-size:18px;font-weight:600;color:white;margin-bottom:2px;}
.v-dest-sub{font-size:11px;color:rgba(255,255,255,0.7);letter-spacing:.4px;}

/* ── OVERVIEW BAR ── */
.v-overview{
  background:var(--ink);border-radius:16px;
  padding:20px 28px;margin:0 40px 8px;
  display:flex;align-items:center;flex-wrap:wrap;
}
.v-overview-item{
  flex:1;min-width:110px;padding:0 20px;
  border-right:1px solid rgba(255,255,255,0.11);
}
.v-overview-item:first-child{padding-left:0;}
.v-overview-item:last-child{border-right:none;}
.v-ov-label{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:rgba(255,255,255,0.42);margin-bottom:4px;}
.v-ov-value{font-size:14.5px;font-weight:500;color:white;}
.v-ov-value.accent{color:var(--gold);}

/* ── HOTEL CARD ── */
.v-hotel{
  background:var(--white);border:1px solid var(--border);
  border-radius:16px;overflow:hidden;display:flex;
  margin-bottom:16px;transition:box-shadow .2s,transform .2s;
}
.v-hotel:hover{box-shadow:var(--shadow);transform:translateY(-2px);}
/* hotel image — background-image div, no <img> tag */
.v-hotel-img{
  width:210px;flex-shrink:0;
  background-size:cover;background-position:center;
  min-height:160px;
}
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

/* ── PLAN LINES ── */
.v-plan-line{padding:11px 18px;border-left:3px solid var(--accent);border-radius:0 10px 10px 0;background:#F5EDE6;margin-bottom:9px;font-size:14px;color:var(--ink);line-height:1.6;}
.v-day-header{background:var(--ink);color:white;padding:10px 18px;border-radius:9px;font-size:12.5px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin:18px 0 10px;}

/* ── BOOKING LINKS ── */
.v-links-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:18px;}
.v-link-card{background:var(--white);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center;text-decoration:none;color:var(--ink);font-size:13px;font-weight:500;transition:all .2s;display:block;}
.v-link-card:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-2px);box-shadow:0 4px 14px rgba(196,98,45,0.12);}
.v-link-icon{font-size:22px;margin-bottom:6px;}

/* ── METRICS ── */
.v-metric{background:var(--white);border:1px solid var(--border);border-radius:14px;padding:20px;text-align:center;}
.v-metric-label{font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--ink-soft);margin-bottom:8px;}
.v-metric-value{font-family:var(--ff-head);font-size:24px;font-weight:600;color:var(--ink);}

/* ── PLACE CARD ── */
.v-place-card{background:var(--white);border:1px solid var(--border);border-radius:14px;overflow:hidden;margin-bottom:14px;transition:box-shadow .2s;}
.v-place-card:hover{box-shadow:var(--shadow);}
/* place image — background-image div */
.v-place-img{width:100%;height:160px;background-size:cover;background-position:center;}
.v-place-info{padding:14px 16px;}
.v-place-name{font-weight:600;font-size:15px;color:var(--ink);margin-bottom:4px;}
.v-place-addr{font-size:12px;color:var(--ink-soft);line-height:1.4;}

/* ── MISC ── */
.v-divider{height:1px;background:var(--border);margin:8px 0 20px;}
.stSpinner>div{border-top-color:var(--accent)!important;}
div[data-testid="stSuccess"]{background:#F0FAF4!important;border:1px solid #86EFAC!important;border-radius:12px!important;border-left:4px solid #22C55E!important;}
div[data-testid="stWarning"]{border-radius:12px!important;border-left:4px solid #F59E0B!important;}

/* ── FOOTER ── */
.v-footer{background:var(--ink);color:rgba(255,255,255,0.45);text-align:center;padding:28px;font-size:13px;margin-top:64px;}
.v-footer strong{color:rgba(255,255,255,0.8);font-weight:500;}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# FIXED NAVBAR
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
# HERO — CSS background-image slider
# NO <img> tags used — that's what caused raw HTML
# ─────────────────────────────────────────

st.markdown("""
<div class="v-hero">

  <!-- 4 slides: each fades in/out via CSS animation offset by 5s -->
  <div class="v-slide v-s1"></div>
  <div class="v-slide v-s2"></div>
  <div class="v-slide v-s3"></div>
  <div class="v-slide v-s4"></div>

  <!-- Dark overlay -->
  <div class="v-hero-overlay"></div>

  <!-- Text content -->
  <div class="v-hero-text">
    <div class="v-hero-tag">AI-Powered Travel Planning</div>
    <h1>Your next <em>adventure</em>,<br>perfectly planned.</h1>
    <p>From itinerary to hotels — Voyagr builds your dream trip in seconds using AI.</p>
  </div>

  <!-- Indicator dots -->
  <div class="v-dots">
    <div class="v-dot d1"></div>
    <div class="v-dot d2"></div>
    <div class="v-dot d3"></div>
    <div class="v-dot d4"></div>
  </div>

</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SEARCH PANEL — 2 ROWS
# Row 1: From | To
# Row 2: Days | Min Budget | Max Budget | Mode | Button
# ─────────────────────────────────────────

st.markdown("<div class='v-search-wrap'><div class='v-search-panel'>", unsafe_allow_html=True)
st.markdown("<div class='v-search-eyebrow'>Plan your trip</div>", unsafe_allow_html=True)

# ── ROW 1: From & To ──
row1_c1, row1_c2 = st.columns(2)
with row1_c1:
    st.markdown("<span class='v-field-label'>📍 From</span>", unsafe_allow_html=True)
    source = st.text_input("From", placeholder="Enter origin city  (e.g. Indore)", label_visibility="collapsed")
with row1_c2:
    st.markdown("<span class='v-field-label'>🏁 To</span>", unsafe_allow_html=True)
    destination = st.text_input("To", placeholder="Enter destination  (e.g. Goa)", label_visibility="collapsed")

# Small gap between rows
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ── ROW 2: Days | Min Budget | Max Budget | Mode ──
# row2_c1, row2_c2, row2_c3, row2_c4 = st.columns([1, 1.4, 1.4, 1.4])
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
        [
            "👫 Couple",
            "👨‍👩‍👧‍👦 Family with Kids",
            "👯 Friends Group",
            "🧳 Solo Traveler",
            "💼 Business Traveler",
            "🧓 Senior Citizens",
            "🎒 Backpacker"
        ],
        label_visibility="collapsed"
    )

if budget_min > budget_max:
    st.warning("⚠️ Minimum budget cannot exceed maximum budget.")

# Generate button
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
generate = st.button("✦  Generate My Trip Plan", use_container_width=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# POPULAR DESTINATIONS — background-image cards
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
        # background-image in inline style — works in Streamlit
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
    # TEST DESTINATION ID
    test_id, test_type = get_destination_id(destination)
    st.write(f"Destination ID: {test_id}, Type: {test_type}")
    with st.spinner("Building your perfect trip plan..."):
        route_places = get_route_places(source, destination)
        hotels       = get_hotels(destination, days, budget_max)
        # plan         = generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places, traveler_type)
        plan = generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places, traveler_type)

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
    # st.markdown(f"""
    # <div class="v-overview">
    #   <div class="v-overview-item"><div class="v-ov-label">Journey</div><div class="v-ov-value accent">{source} → {destination}</div></div>
    #   <div class="v-overview-item"><div class="v-ov-label">Duration</div><div class="v-ov-value">{days} Days</div></div>
    #   <div class="v-overview-item"><div class="v-ov-label">Budget</div><div class="v-ov-value">₹{budget_min:,} – ₹{budget_max:,}</div></div>
    #   <div class="v-overview-item"><div class="v-ov-label">Travel Mode</div><div class="v-ov-value">{mode_clean}</div></div>
    #   <div class="v-overview-item"><div class="v-ov-label">Hotels Found</div><div class="v-ov-value">{len(hotels)} options</div></div>
    #   <div class="v-overview-item"><div class="v-ov-label">Attractions</div><div class="v-ov-value">{len(route_places)} places</div></div>
    # </div>
    # """, unsafe_allow_html=True)

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
            if not line: continue
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
                    # background-image div instead of <img> tag
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
            st.warning("No hotels found in this budget. Try increasing your max budget.")
        else:
            for h in hotels:
                price = h.get("price_per_night", 0)
                try: pf = f"₹{int(price):,}"
                except: pf = f"₹{price}"

                # Use background-image div for hotel image — no <img> tag
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
        for col, (lbl, val) in zip([m1,m2,m3,m4], [
            ("Origin", source), ("Destination", destination),
            ("Duration", f"{days} days"), ("Max Budget", f"₹{budget_max:,}")
        ]):
            with col:
                st.markdown(f'<div class="v-metric"><div class="v-metric-label">{lbl}</div><div class="v-metric-value">{val}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "Detail": ["From","To","Duration","Budget Range","Travel Mode","Traveling As","Hotels Found","Attractions"],
            "Value":  [source, destination, f"{days} days",
                    f"₹{budget_min:,} – ₹{budget_max:,}", travel_mode,
                    traveler_type, str(len(hotels)), str(len(route_places))]
        }), use_container_width=True, hide_index=True)
        # st.dataframe(pd.DataFrame({
        #     "Detail": ["From","To","Duration","Budget Range","Travel Mode","Hotels Found","Attractions"],
        #     "Value":  [source, destination, f"{days} days",
        #                f"₹{budget_min:,} – ₹{budget_max:,}", travel_mode,
        #                str(len(hotels)), str(len(route_places))]
        # }), use_container_width=True, hide_index=True)

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
