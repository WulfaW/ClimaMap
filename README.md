# 🌤️ ClimaMap - Interactive Weather Dashboard

A modern, interactive weather application built with Python and Streamlit that provides real-time weather information and forecasts with an intuitive map-based interface.

## 🚀 Live Demo

**[View Live Application](https://climamap-5iq7h3eyjrkipunbdbffoc.streamlit.app/)**

## ✨ Features

- 🗺️ **Interactive Map Interface** - Explore weather conditions globally with an intuitive map
- 🌡️ **Real-time Weather Data** - Get current weather conditions for any location
- 📈 **Weather Forecasts** - View detailed weather predictions
- 🎯 **Location Search** - Search for weather by city name or coordinates
- 📱 **Responsive Design** - Optimized for both desktop and mobile devices
- 🎨 **Modern UI** - Clean, user-friendly interface with visual weather representations

## 🛠️ Technologies Used

- **Python** - Core programming language
- **Streamlit** - Web application framework
- **Weather API** - Real-time weather data integration
- **Folium/Plotly** - Interactive map visualizations
- **Pandas** - Data manipulation and analysis
- **Requests** - API data fetching

## 🏗️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/climamap.git
   cd climamap
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API keys**
   ```bash
   # Create a .env file and add your weather API key
   echo "WEATHER_API_KEY=your_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📋 Requirements

```txt
streamlit>=1.25.0
requests>=2.31.0
pandas>=2.0.0
folium>=0.14.0
plotly>=5.15.0
python-dotenv>=1.0.0
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
WEATHER_API_KEY=your_openweathermap_api_key
DEFAULT_CITY=Istanbul
DEFAULT_COUNTRY=TR
```

### API Setup

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Add the API key to your `.env` file
3. Restart the application

## 📱 Usage

1. **Search Location**: Enter a city name or coordinates in the search box
2. **Explore Map**: Click on different locations on the interactive map
3. **View Details**: Check current conditions, forecasts, and weather trends
4. **Compare Locations**: Select multiple cities to compare weather data

## 🏗️ Project Structure

```
climamap/
│
├── app.py                 # Main Streamlit application
├── util.py
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # Project documentation
```

## 🌟 Key Features Explained

### Interactive Weather Map
- Real-time weather overlay on world map
- Click-to-explore functionality
- Visual weather indicators

### Advanced Weather Metrics
- Temperature, humidity, pressure
- Wind speed and direction
- UV index and visibility
- Air quality information

### Smart Location Detection
- Automatic geolocation
- City name autocomplete
- Coordinates support

## 🚀 Deployment

### Streamlit Cloud Deployment

1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add environment variables in the Streamlit dashboard
4. Deploy with one click

### Alternative Deployment Options

- **Heroku**: Use the included `Procfile`
- **Docker**: Containerized deployment ready
- **AWS/GCP**: Cloud platform deployment

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for weather data API
- [Streamlit](https://streamlit.io/) for the amazing web app framework
- Weather icons from [Weather Icons](https://erikflowers.github.io/weather-icons/)

## 📞 Contact


Project Link: [https://github.com/WulfaW/ClimaMap](https://github.com/WulfaW/ClimaMap)

---

⭐ **If you found this project helpful, please give it a star!** ⭐
