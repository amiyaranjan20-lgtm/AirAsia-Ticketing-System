from datetime import datetime

def calculate_dynamic_price(duration, aircraft, departure_time, departure_date):

    base_price = 50

    duration = int(duration)

    if "ATR" in aircraft:
        multiplier = 0.5
    elif "A320" in aircraft or "A321" in aircraft:
        multiplier = 0.8
    elif "Boeing" in aircraft or "787" in aircraft or "777" in aircraft or "A350" in aircraft:
        multiplier = 1.5
    else:
        multiplier = 1

    price = base_price + (duration * multiplier)

    hour = int(departure_time.split(":")[0])

    if 6 <= hour <= 9:
        price *= 1.20
    elif 18 <= hour <= 22:
        price *= 1.15

    date_obj = datetime.strptime(departure_date, "%m/%d/%y")

    if date_obj.weekday() >= 4:
        price *= 1.25

    return round(price, 2)