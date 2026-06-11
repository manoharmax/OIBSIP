from forecast_service import get_forecast
from chart_service import create_temperature_chart

forecast = get_forecast(
    17.3850,
    78.4867
)

create_temperature_chart(forecast)

print("Chart Generated Successfully - test_chart.py:11")