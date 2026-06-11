import customtkinter as ctk
from PIL import Image

from weather_service import get_weather
from aqi_service import get_aqi
from forecast_service import get_forecast
from chart_service import create_temperature_chart


# ==========================
# APPEARANCE
# ==========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class WeatherApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(
            fill="both",
            expand=True
        )
        
        self.title("AtmosIQ - Advanced Weather Intelligence")
        self.geometry("1400x1000")

        # ==========================
        # HEADER
        # ==========================

        self.title_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="🌦 AtmosIQ",
            font=("Arial", 34, "bold")
        )
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Advanced Weather Intelligence",
            font=("Arial", 16)
        )
        self.subtitle_label.pack(pady=(0, 20))

        # ==========================
        # SEARCH BAR
        # ==========================

        self.search_frame = ctk.CTkFrame(self.scrollable_frame)
        self.search_frame.pack(pady=10)

        self.city_entry = ctk.CTkEntry(
            self.search_frame,
            width=400,
            height=40,
            placeholder_text="Enter City Name"
        )
        self.city_entry.pack(side="left", padx=10, pady=10)

        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="🔍 Get Weather",
            width=180,
            height=40,
            command=self.fetch_weather
        )
        self.search_btn.pack(side="left", padx=10)

        # ==========================
        # CITY HEADER
        # ==========================

        self.city_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Search a city to begin",
            font=("Arial", 26, "bold")
        )
        self.city_label.pack(pady=20)

        self.condition_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="",
            font=("Arial", 18)
        )
        self.condition_label.pack(pady=(0, 10))

        self.aqi_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="",
            font=("Arial", 18, "bold")
        )
        self.aqi_label.pack(pady=(0, 20))

        # ==========================
        # WEATHER CARDS
        # ==========================
        self.cards_frame = ctk.CTkFrame(self.scrollable_frame)
        self.cards_frame.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.cards = {}

        card_data = [
            ("temperature", "🌡 Temperature"),
            ("humidity", "💧 Humidity"),
            ("wind", "🌬 Wind Speed"),
            ("pressure", "🌀 Pressure"),
            ("visibility", "👁 Visibility"),
            ("clouds", "☁ Clouds")
        ]

        for index, (key, title) in enumerate(card_data):

            row = index // 2
            col = index % 2

            frame = ctk.CTkFrame(
                self.cards_frame,
                width=350,
                height=90
            )

            frame.grid(
                row=row,
                column=col,
                padx=10,
                pady=5,
                sticky="nsew"
            )

            value_label = ctk.CTkLabel(
                frame,
                text="--",
                font=("Arial", 22, "bold")
            )
            value_label.pack(pady=(20, 5))

            title_label = ctk.CTkLabel(
                frame,
                text=title,
                font=("Arial", 14)
            )
            title_label.pack()

            self.cards[key] = value_label

        self.cards_frame.grid_columnconfigure(0, weight=1)
        self.cards_frame.grid_columnconfigure(1, weight=1)

        # ==========================
        # FORECAST SECTION
        # ==========================

        self.forecast_frame = ctk.CTkFrame(self.scrollable_frame)
        self.forecast_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )
        self.forecast_frame.configure(
            fg_color="red"
        )

        self.forecast_title = ctk.CTkLabel(
            self.forecast_frame,
            text="📅 5-Day Forecast",
            font=("Arial", 20, "bold")
        )
        self.forecast_title.pack(pady=10)

        self.forecast_label = ctk.CTkLabel(
            self.forecast_frame,
            text="",
            font=("Arial", 16),
            justify="left"
        )
        self.forecast_label.pack(pady=10)
        print("FORECAST SECTION CREATED - app.py:185")
        # ==========================
        # CHART SECTION
        # ==========================

        self.chart_frame = ctk.CTkFrame(self.scrollable_frame)
        self.chart_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.chart_title = ctk.CTkLabel(
            self.chart_frame,
            text="📈 Temperature Trend",
            font=("Arial", 20, "bold")
        )
        self.chart_title.pack(pady=10)

        self.chart_label = ctk.CTkLabel(
            self.chart_frame,
            text=""
        )
        self.chart_label.pack(pady=10)
        print("CHART SECTION CREATED - app.py:209")
        # ==========================
        # ADDITIONAL INFO
        # ==========================

        self.extra_frame = ctk.CTkFrame(self.scrollable_frame)
        self.extra_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.extra_info = ctk.CTkLabel(
            self.extra_frame,
            text="",
            justify="left",
            font=("Arial", 16)
        )
        self.extra_info.pack(pady=15)

        # ==========================
        # FOOTER
        # ==========================

        self.footer = ctk.CTkLabel(
            self.scrollable_frame,
            text="AtmosIQ v3.0 | Weather • AQI • Forecast • Charts",
            font=("Arial", 12)
        )
        self.footer.pack(pady=(0, 10))

    def fetch_weather(self):

        city = self.city_entry.get().strip()

        if not city:
            self.city_label.configure(
                text="⚠ Please enter a city"
            )
            return

        weather = get_weather(city)

        if not weather:
            self.city_label.configure(
                text="⚠ Unable to fetch weather"
            )
            self.condition_label.configure(
                text="Check city name or API key."
            )
            return

        aqi_data = get_aqi(
            weather["lat"],
            weather["lon"]
        )

        forecast = get_forecast(
            weather["lat"],
            weather["lon"]
        )

        # ==========================
        # HEADER
        # ==========================

        self.city_label.configure(
            text=f"📍 {weather['city']}, {weather['country']}"
        )

        self.condition_label.configure(
            text=f"☁ {weather['description']}"
        )

        aqi_colors = {
            1: "#00FF00",
            2: "#7CFC00",
            3: "#FFD700",
            4: "#FF8C00",
            5: "#FF0000"
        }

        if aqi_data:
            self.aqi_label.configure(
                text=f"🌿 AQI: {aqi_data['aqi']} ({aqi_data['label']})",
                text_color=aqi_colors.get(
                    aqi_data["aqi"],
                    "#FFFFFF"
                )
            )

        # ==========================
        # WEATHER CARDS
        # ==========================

        self.cards["temperature"].configure(
            text=f"{weather['temperature']}°C"
        )

        self.cards["humidity"].configure(
            text=f"{weather['humidity']}%"
        )

        self.cards["wind"].configure(
            text=f"{weather['wind_speed']} m/s"
        )

        self.cards["pressure"].configure(
            text=f"{weather['pressure']} hPa"
        )

        self.cards["visibility"].configure(
            text=f"{weather['visibility']} km"
        )

        self.cards["clouds"].configure(
            text=f"{weather['clouds']}%"
        )

        # ==========================
        # FORECAST DISPLAY
        # ==========================

        if forecast:

            forecast_text = ""

            for item in forecast:

                forecast_text += (
                    f"{item['date']}    "
                    f"{item['temp']}°C    "
                    f"{item['description']}\n"
                )

            self.forecast_label.configure(
                text=forecast_text
            )

            create_temperature_chart(
                forecast
            )

            chart_image = ctk.CTkImage(
                light_image=Image.open(
                    "forecast_chart.png"
                ),
                dark_image=Image.open(
                    "forecast_chart.png"
                ),
                size=(700, 350)
            )

            self.chart_label.configure(
                image=chart_image,
                text=""
            )

            self.chart_label.image = chart_image

        # ==========================
        # ADDITIONAL INFO
        # ==========================

        self.extra_info.configure(
            text=f"""
🌅 Sunrise : {weather['sunrise']}

🌇 Sunset : {weather['sunset']}

🌡 Min Temp : {weather['temp_min']}°C

🌡 Max Temp : {weather['temp_max']}°C

🌿 AQI Status : {aqi_data['label'] if aqi_data else 'N/A'}

PM2.5 : {aqi_data['pm25'] if aqi_data else 'N/A'}

PM10 : {aqi_data['pm10'] if aqi_data else 'N/A'}

CO : {aqi_data['co'] if aqi_data else 'N/A'}

NO₂ : {aqi_data['no2'] if aqi_data else 'N/A'}

O₃ : {aqi_data['o3'] if aqi_data else 'N/A'}
"""
        )

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()