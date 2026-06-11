import matplotlib.pyplot as plt


def create_temperature_chart(forecast):

    dates = [
        item["date"][5:]
        for item in forecast
    ]

    temperatures = [
        item["temp"]
        for item in forecast
    ]

    plt.figure(figsize=(8, 4))

    plt.plot(
        dates,
        temperatures,
        marker="o",
        linewidth=2
    )

    plt.title("5-Day Temperature Forecast")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "forecast_chart.png"
    )

    plt.close()