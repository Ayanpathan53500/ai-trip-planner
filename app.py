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




import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import requests


# API setup
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)
# genai.configure(api_key=GOOGLE_API_KEY)
# tavily = TavilyClient(api_key=TAVILY_API_KEY)

# model = genai.GenerativeModel("gemini-2.5-flash")

# -------- FUNCTIONS -------- #


RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
}


def get_destination_id(city):
    try:
        url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

        params = {
            "name": city,
            "locale": "en-gb"
        }

        res = requests.get(url, headers=headers, params=params, timeout=10)

        if res.status_code != 200:
            print("Location API error:", res.status_code)
            return None, None

        data = res.json()

        if not data:
            return None, None

        return data[0]["dest_id"], data[0]["dest_type"]

    except Exception as e:
        print("Destination error:", e)
        return None, None

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

def get_lat_lon(city):
    url = "https://api.geoapify.com/v1/geocode/search"

    params = {
        "text": city,
        "apiKey": GEOAPIFY_API_KEY
    }

    res = requests.get(url, params=params).json()

    if not res.get("features"):
        return None, None

    lat = res["features"][0]["properties"]["lat"]
    lon = res["features"][0]["properties"]["lon"]

    return lat, lon


def get_route_places(source, destination):
    try:
        # STEP 1: Convert cities → coordinates
        geo_url = "https://api.geoapify.com/v1/geocode/search"

        def get_coords(city):
            res = requests.get(geo_url, params={
                "text": city,
                "apiKey": GEOAPIFY_API_KEY
            }).json()

            if not res.get("features"):
                return None

            prop = res["features"][0]["properties"]
            return prop["lon"], prop["lat"]

        start = get_coords(source)
        end = get_coords(destination)

        if not start or not end:
            print("❌ Geocoding failed")
            return []

        # STEP 2: Get route
        route_url = "https://api.geoapify.com/v1/routing"

        params = {
            "waypoints": f"{start[1]},{start[0]}|{end[1]},{end[0]}",
            "mode": "drive",
            "apiKey": GEOAPIFY_API_KEY
        }

        route_res = requests.get(route_url, params=params).json()

        if "features" not in route_res:
            print("❌ Route API error:", route_res)
            return []

        coords = route_res["features"][0]["geometry"]["coordinates"]

        # FIX: flatten nested coordinates
        if isinstance(coords[0][0], list):
            coords = coords[0]

        # STEP 3: Pick sample points (safe)
        step = max(1, len(coords) // 6)
        sample_points = coords[::step]

        places = []
        seen = set()

        # STEP 4: Get places near each point
        for lon, lat in sample_points:

            places_url = "https://api.geoapify.com/v2/places"

            params = {
                "categories": "tourism.sights,tourism.attraction",
                "filter": f"circle:{lon},{lat},4000",
                "limit": 2,
                "apiKey": GEOAPIFY_API_KEY
            }

            res = requests.get(places_url, params=params).json()

            for item in res.get("features", []):
                prop = item["properties"]

                name = prop.get("name", "Place")

                # avoid duplicates
                if name in seen:
                    continue
                seen.add(name)

                places.append({
                    "title": name,
                    "address": prop.get("formatted", ""),
                    "lat": prop.get("lat"),
                    "lon": prop.get("lon"),
                    "image": f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=400&height=300&center=lonlat:{prop.get('lon')},{prop.get('lat')}&zoom=14&apiKey={GEOAPIFY_API_KEY}"
                })

        return places[:10]

    except Exception as e:
        print("❌ Route System Error:", e)
        return []

# from datetime import datetime, timedelta
# import requests

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
# from datetime import datetime, timedelta
# import requests

# def get_hotels(destination, days, budget_max):
#     try:
#         # ✅ FIX MIN VALUE
#         budget_min = 1000

#         dest_id, dest_type = get_destination_id(destination)

#         if not dest_id:
#             return []

#         # ✅ AUTO DATES
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

#             # ✅ ONLY PER NIGHT PRICE
#             price_per_night = int(total_price / days)

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

#             # ✅ FILTER ONLY PER NIGHT (₹1000 → budget_max)
#             if 1000 <= price_per_night <= budget_max:
#                 hotels.append(hotel)

#         # ✅ fallback if nothing found
#         if not hotels:
#             return all_hotels[:5]

#         return hotels

#     except Exception as e:
#         print("Hotel error:", e)
#         return []
# from datetime import datetime, timedelta
# import requests

# def get_hotels(destination, days, budget_min, budget_max):
#     try:
#         dest_id, dest_type = get_destination_id(destination)

#         if not dest_id:
#             print("❌ No destination found")
#             return []

#         # ✅ AUTO-GENERATE VALID DATES
#         today = datetime.today()
#         checkin = today + timedelta(days=1)
#         checkout = checkin + timedelta(days=days)

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

#             # ⚠️ sometimes works better than filter_by_currency
#             "filter_by_currency": "INR",
#             "currency": "INR"
#         }

#         res = requests.get(url, headers=headers, params=params, timeout=15)

#         if res.status_code != 200:
#             print("❌ Hotel API error:", res.status_code)
#             print(res.text)
#             return []

#         data = res.json()

#         hotels = []

#         # 👉 take more results, then filter
#         for h in data.get("result", [])[:30]:

#             # ✅ SAFE PRICE FETCH (better than min_total_price)
#             price_data = h.get("price_breakdown", {})
#             total_price = price_data.get("gross_price")

#             if not total_price:
#                 continue  # skip invalid price

#             try:
#                 total_price = float(total_price)
#             except:
#                 continue

#             # ❌ skip zero or garbage prices
#             if total_price <= 0:
#                 continue

#             # ✅ PRICE PER NIGHT
#             price_per_night = round(total_price / days, 2) if days > 0 else 0

#             # ✅ BUDGET FILTER
#             if total_price < budget_min or total_price > budget_max:
#                 continue

#             hotels.append({
#                 "name": h.get("hotel_name"),
#                 "total_price": total_price,
#                 "price_per_night": price_per_night,
#                 "currency": price_data.get("currency", "INR"),
#                 "rating": h.get("review_score"),
#                 "review": h.get("review_score_word"),
#                 "image": h.get("main_photo_url"),
#                 "address": h.get("address"),
#                 "distance": h.get("distance_to_cc"),
#                 "lat": h.get("latitude"),
#                 "lon": h.get("longitude"),
#                 "url": h.get("url")
#             })

#         return hotels

#     except Exception as e:
#         print("❌ Hotel error:", e)
#         return []
from datetime import datetime, timedelta
import requests

def get_hotels(destination, days):
    try:
        dest_id, dest_type = get_destination_id(destination)

        if not dest_id:
            print("❌ No destination found")
            return []

        # ✅ Safe days
        days = max(days, 1)

        # ✅ AUTO DATES (REQUIRED BY API)
        today = datetime.today()
        checkin = today + timedelta(days=1)
        checkout = checkin + timedelta(days=days)

        url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

        params = {
            "dest_id": dest_id,
            "dest_type": dest_type,
            "checkin_date": checkin.strftime("%Y-%m-%d"),
            "checkout_date": checkout.strftime("%Y-%m-%d"),
            "adults_number": 2,
            "room_number": 1,
            "order_by": "popularity",
            "locale": "en-gb",
            "units": "metric",
            "filter_by_currency": "INR"
        }

        res = requests.get(url, headers=headers, params=params, timeout=15)

        if res.status_code != 200:
            print("❌ Hotel API error:", res.status_code)
            print(res.text)
            return []

        data = res.json()

        hotels = []

        for h in data.get("result", [])[:15]:

            # ✅ Better price extraction
            price_data = h.get("price_breakdown", {})
            total_price = price_data.get("gross_price")

            if not total_price:
                continue

            try:
                total_price = float(total_price)
            except:
                continue

            if total_price <= 0:
                continue

            # ✅ PER NIGHT CALCULATION
            price_per_night = int(total_price / days)

            hotels.append({
                "name": h.get("hotel_name"),
                "price_per_night": price_per_night,   # 🔥 IMPORTANT
                "rating": h.get("review_score"),
                "review": h.get("review_score_word"),
                "image": h.get("main_photo_url"),
                "address": h.get("address"),
                "distance": h.get("distance_to_cc"),
                "lat": h.get("latitude"),
                "lon": h.get("longitude"),
                "url": h.get("url")
            })

        return hotels

    except Exception as e:
        print("Hotel error:", e)
        return []
# from datetime import datetime, timedelta

# def get_hotels(destination, days):
#     try:
#         dest_id, dest_type = get_destination_id(destination)

#         if not dest_id:
#             print("❌ No destination found")
#             return []

#         # 👉 AUTO-GENERATE DATES (user doesn't see this)
#         today = datetime.today()
#         checkin = today + timedelta(days=1)
#         checkout = checkin + timedelta(days=days)

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
#             "filter_by_currency": "INR"
#         }

#         res = requests.get(url, headers=headers, params=params, timeout=15)

#         if res.status_code != 200:
#             print("❌ Hotel API error:", res.status_code)
#             print(res.text)
#             return []

#         data = res.json()

#         hotels = []
#         for h in data.get("result", [])[:10]:
#             hotels.append({
#                 "name": h.get("hotel_name"),
#                 "price": h.get("min_total_price"),
#                 "rating": h.get("review_score"),
#                 "review": h.get("review_score_word"),
#                 "image": h.get("main_photo_url"),
#                 "address": h.get("address"),
#                 "distance": h.get("distance_to_cc"),
#                 "lat": h.get("latitude"),
#                 "lon": h.get("longitude"),
#                 "url": h.get("url")
#             })

#         return hotels

#     except Exception as e:
#         print("Hotel error:", e)
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


def generate_plan(source, destination, days, budget_min, budget_max, travel_mode, route_places):
    names = [p["title"] for p in route_places]

    prompt = f"""
    Create a complete travel plan:

    From: {source}
    To: {destination}
    Days: {days}
    Budget: {budget_min} to {budget_max} INR
    Travel Mode: {travel_mode}

    Include:
    - Route journey plan
    - Places between route: {', '.join(names)}
    - Day-wise itinerary
    - Budget breakdown (transport + hotel + food)
    - Travel tips
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text



# -------- UI -------- #

st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")

# ---------- HIDE STREAMLIT DEFAULT ----------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- PREMIUM CSS ----------
st.markdown("""
<style>

/* GLOBAL */
.block-container {
    padding-top: 0rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* NAVBAR */
.navbar {
    position: sticky;
    top: 0;
    z-index: 999;
    background: white;
    padding: 12px 25px;
    border-radius: 0 0 12px 12px;
    display: flex;
    justify-content: space-between;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

.logo {
    font-weight: bold;
    font-size: 20px;
    color: #ff4b4b;
}

/* HERO */
.hero {
    height: 260px;
    border-radius: 20px;
    margin-top: 10px;
    background-size: cover;
    background-position: center;
    animation: slide 12s infinite;
    position: relative;
}

@keyframes slide {
    0% {background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');}
    33% {background-image: url('https://images.unsplash.com/photo-1501785888041-af3ef285b470');}
    66% {background-image: url('https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1');}
    100% {background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');}
}

.hero::after {
    content: "";
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.5);
    border-radius: 20px;
}

.hero-text {
    position: absolute;
    bottom: 30px;
    left: 30px;
    color: white;
    z-index: 2;
}

.hero-text h1 {
    margin: 0;
    font-size: 34px;
}

/* SEARCH BOX */
.search-box {
    margin-top: -40px;
    background: white;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

/* INPUTS ALIGN FIX */
div[data-baseweb="input"], div[data-baseweb="select"] {
    margin-top: -6px;
}

/* INPUT STYLE */
div[data-baseweb="input"] input {
    background: #f3f6fb !important;
    border-radius: 10px !important;
    border: none !important;
}

div[data-baseweb="select"] {
    background: #f3f6fb !important;
    border-radius: 10px !important;
}

/* BUTTON */
button[kind="primary"] {
    background: linear-gradient(90deg, #ff4b4b, #ff7b7b);
    border-radius: 12px;
    height: 48px;
    font-weight: 600;
}

/* CARDS */
.card {
    border-radius: 14px;
    overflow: hidden;
    height: 160px;
    position: relative;
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.05);
}

.card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.card-title {
    position: absolute;
    bottom: 10px;
    left: 10px;
    color: white;
    font-weight: bold;
    background: rgba(0,0,0,0.6);
    padding: 6px 12px;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# ---------- NAVBAR ----------
st.markdown("""
<div class="navbar">
    <div class="logo">🌍 TravelAI</div>
    <div>Flights | Hotels | Packages</div>
</div>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <div class="hero-text">
        <h1>AI Travel Planner Pro</h1>
        <p>Plan smarter journeys with AI ✈️</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- SEARCH ----------
st.markdown("<div class='search-box'>", unsafe_allow_html=True)

# ROW 1
c1, c2 = st.columns(2)
with c1:
    source = st.text_input("From", placeholder="Enter city")

with c2:
    destination = st.text_input("To", placeholder="Enter destination")

# ROW 2 (FIXED ALIGNMENT)
c3, c4, c5 = st.columns([1,2,1])

with c3:
    st.markdown("**Days**")
    days = st.number_input("Days", 1, 15, 3, label_visibility="collapsed")

with c4:
    st.markdown("**💰 Budget (₹)**")

    b1, b2 = st.columns(2)

    with b1:
        budget_min = st.number_input(
            "Min",
            min_value=0,
            value=5000,
            step=1000,
            label_visibility="collapsed"
        )

    with b2:
        budget_max = st.number_input(
            "Max",
            min_value=0,
            value=20000,
            step=1000,
            label_visibility="collapsed"
        )

    if budget_min > budget_max:
        st.warning("⚠️ Min should be less than Max")

with c5:
    st.markdown("**Mode**")
    travel_mode = st.selectbox(
        "Travel Mode",
        ["🚗 Car", "✈️ Flight", "🚆 Train", "🚌 Bus"],
        label_visibility="collapsed"
    )

generate = st.button("✨ Generate Plan", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- DESTINATIONS ----------
st.markdown("## 🔥 Popular Destinations")

cols = st.columns(4)

destinations = [
    ("Goa", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"),
    ("Manali", "https://images.unsplash.com/photo-1501785888041-af3ef285b470"),
    ("Jaipur", "https://images.unsplash.com/photo-1548013146-72479768bada"),
    ("Kerala", "https://images.unsplash.com/photo-1593693411515-c20261bcad6e")
]

for i, (name, img) in enumerate(destinations):
    with cols[i]:
        st.markdown(f"""
        <div class="card">
            <img src="{img}">
            <div class="card-title">{name}</div>
        </div>
        """, unsafe_allow_html=True)
# -------- MAIN -------- #

if generate and source and destination:

    with st.spinner("🔍 Planning your smart trip..."):

        route_places = get_route_places(source, destination)
    
        # hotels = get_hotels(destination)
        hotels = get_hotels(destination, days)
        # hotels = get_hotels(destination, days, budget_min or 0, budget_max or 100000)
        # hotels = get_hotels(destination, days, budget_max)
        plan = generate_plan(
            source, destination, days,
            budget_min, budget_max,
            travel_mode, route_places
        )

    st.success("✅ Trip Ready!")
    st.markdown(f"""
    ### ✈️ Trip Overview  
    **From:** {source} → **To:** {destination}  
    📅 {days} Days | 💰 ₹{budget_min}-{budget_max} | 🚆 {travel_mode}
    """)

    # -------- TABS -------- #
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🗺️ Plan", "🛣️ Route Places", "🏨 Hotels", "📊 Summary"]
    )

    # -------- PLAN -------- #
    with tab1:
        st.subheader("📅 AI Itinerary")
        for line in plan.split("\n"):
            if line.strip():
                st.markdown(f"- {line}")

        st.markdown("### 🔗 Booking Platforms")
        st.markdown("""
                    - 🛏️ Hotels: [MakeMyTrip](https://www.makemytrip.com), [Booking.com](https://www.booking.com)
                    - 🚆 Train: [IRCTC](https://www.irctc.co.in)
                    - 🚌 Bus: [RedBus](https://www.redbus.in)
                    - ✈️ Flights: [Goibibo](https://www.goibibo.com)
                            """)
    # -------- ROUTE PLACES -------- #
    with tab2:
        st.subheader("🛣️ Places Between Your Journey")

        if not route_places:
            st.warning("⚠️ No route places found")
        else:
            cols = st.columns(2)

            for i, p in enumerate(route_places):
                with cols[i % 2]:
                    st.image(p["image"], width="stretch")
                    st.markdown(f"""
                    **📍 {p['title']}**  
                    {p['address']}
                    """)

    # -------- HOTELS -------- #
    with tab3:
        st.subheader("🏨 Real Hotels (Live Data)")

        if not hotels:
            st.warning("⚠️ No hotels found in your budget. Try increasing budget.")
        else:
            for h in hotels:

                col1, col2 = st.columns([1, 2])

                with col1:
                    if h.get("image"):
                        st.image(h["image"], width="stretch")

                with col2:
                    price = h.get("price_per_night", "N/A")

                    st.markdown(f"""
                    ### 🏨 {h.get('name', 'Hotel')}

                    ⭐ {h.get('rating', 'N/A')} / 10 ({h.get('review', '')})  
                    📍 {h.get('address', 'No address')}  
                    📏 {h.get('distance', 'N/A')} from center  

                    💰 **₹{price} / night**
                    """)

                    if h.get("url"):
                        st.markdown(f"[🔘 Book Now]({h['url']})")

                st.markdown("---")
    # with tab3:
    #     st.subheader("🏨 Real Hotels (Live Data)")

    #     if not hotels:
    #         st.warning("⚠️ No hotels found in your budget. Try increasing budget.")
    #     else:
    #         for h in hotels:

    #             col1, col2 = st.columns([1, 2])

    #             with col1:
    #                 if h["image"]:
    #                     st.image(h["image"], use_container_width=True)

    #             with col2:
    #                 st.markdown(f"""
    #                 ### 🏨 {h['name']}

    #                 ⭐ {h['rating']} / 10 ({h['review']})  
    #                 📍 {h['address']}  
    #                 📏 {h['distance']} from center  

    #                 💰 **₹{h['price_per_night']} / night**
    #                 """)

    #                 st.markdown(f"[🔘 Book Now]({h['url']})")

    #             st.markdown("---")

    # with tab3:
    #     st.subheader("🏨 Real Hotels (Live Data)")

    #     if not hotels:
    #         st.warning("⚠️ No hotels found in your budget. Try increasing budget.")
    #     else:
    #         for h in hotels:

    #             col1, col2 = st.columns([1, 2])

    #             with col1:
    #                 if h.get("image"):
    #                     st.image(h["image"], use_container_width=True)

    #             with col2:
    #                 # ✅ SAFE VALUES
    #                 name = h.get("name", "Hotel")
    #                 rating = h.get("rating", "N/A")
    #                 review = h.get("review", "")
    #                 address = h.get("address", "Location not available")
    #                 distance = h.get("distance", "N/A")
    #                 total_price = h.get("total_price", "N/A")
    #                 per_night = h.get("price_per_night", "N/A")
    #                 currency = h.get("currency", "₹")

    #                 st.markdown(f"""
    #                 ### 🏨 {name}

    #                 ⭐ {rating} / 10 ({review})  
    #                 📍 {address}  
    #                 📏 {distance} from center  

    #                 💰 **{currency} {total_price} total stay**  
    #                 🌙 **{currency} {per_night} per night**
    #                 """)

    #                 if h.get("url"):
    #                     st.markdown(f"[🔘 Book Now]({h['url']})")

    #             st.markdown("---")
    # with tab3:
    #     st.subheader("🏨 Real Hotels (Live Data)")

    #     if not hotels:
    #         st.warning("⚠️ No hotels found")
    #     else:
    #         for h in hotels:

    #             col1, col2 = st.columns([1, 2])

    #             with col1:
    #                 if h["image"]:
    #                     st.image(h["image"], use_container_width=True)

    #             with col2:
    #                 st.markdown(f"""
    #                 ### 🏨 {h['name']}

    #                 ⭐ {h['rating']} / 10 ({h['review']})  
    #                 📍 {h['address']}  
    #                 📏 {h['distance']} from center  

    #                 💰 **₹{h['price']} total stay**
    #                 """)

    #                 st.markdown(f"[🔘 Book Now]({h['url']})")

    #             st.markdown("---")
                
   

    # -------- SUMMARY -------- #
    with tab4:
        st.subheader("📊 Trip Summary")

        st.markdown(f"""
        - 📍 From: {source}  
        - 🏁 To: {destination}  
        - 📅 Days: {days}  
        - 💰 Budget: ₹{budget_min} - ₹{budget_max}  
        - 🚆 Travel Mode: {travel_mode}  
        """)

