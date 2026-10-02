# ✈️ Voyanta AI — Generative AI Travel Intelligence

An autonomous, **real-time Generative AI Travel Intelligence system** engineered for MCA (AI & DS) capstone project presentations and organizational showcases.

## 🚀 Features

| Feature | Description |
|---|---|
| 🤖 **Gemini AI Itinerary** | Day-by-day personalized plan with costs, tips & food guide |
| 🌤️ **Live Weather** | Real-time weather + 5-day forecast via OpenWeatherMap |
| 🗺️ **Google Maps & Streets** | Embedded live Google Road map with street names, traffic & points of interest |
| 🛰️ **Satellite Imagery** | High-resolution aerial satellite view of your destination |
| 🚶 **360° Street View** | Interactive Google Street View + Google Earth 3D exploration buttons |
| 🌐 **Overview Globe** | Fast offline Plotly geographical map with destination pin |
| 💰 **Budget Breakdown** | Visual chart with category-wise estimated costs |
| 💱 **Live Exchange Rate** | Real-time USD → INR conversion |
| 📥 **Download Itinerary** | Export your plan as a .txt file |
| 🎨 **Beautiful UI** | Custom CSS with gradient cards and smooth animations |

## 🛠️ Tech Stack

- **Frontend:** Streamlit + Custom CSS
- **AI:** Google Gemini API (`gemini-3.8-flash`) with streaming
- **Weather:** OpenWeatherMap API (free tier)
- **Maps:** Folium + OpenStreetMap (no key required)
- **Charts:** Plotly
- **Exchange Rate:** open.er-api.com (free, no key)

## 📦 Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get API Keys
- **Gemini API Key:** https://aistudio.google.com (free)
- **OpenWeather API Key:** https://openweathermap.org/api (free)

### 3. Create `.env` file
```bash
cp .env.example .env
# Edit .env and add your keys
```

### 4. Run the App
```bash
streamlit run app.py
```

## 🎯 How to Demo

1. Enter destination (e.g., "Goa", "Paris", "Bali")
2. Set number of days, budget, and interests
3. Click **Generate My Itinerary**
4. Watch Gemini AI stream the itinerary in real time!
5. Explore the live weather, map, and budget chart

## 📁 Project Structure

```
ai-travel-planner/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # API key template
└── README.md           # Project documentation
```

## 🏆 Why This Project Impresses Organizations

- ✅ **Real-time data** – live weather, exchange rate, map
- ✅ **Generative AI** – streaming Gemini responses
- ✅ **Professional UI** – custom CSS, animations, charts
- ✅ **Practical use case** – every traveler needs this
- ✅ **Full-stack** – API integration, AI, frontend, data viz
- ✅ **Downloadable output** – tangible deliverable
