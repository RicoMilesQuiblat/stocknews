import requests
import datetime as dt
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

ALPHA_KEY = "H9IZOH5O4GPSGIC3"
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_KEY
}

NEWS_API_KEY = "4dc6867cbe714b91a1bc691ed448c680"
news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}

TWILIO_ACCOUNT = "AC62fb8713b31121873d414bfb3257e2db"
TWILIO_KEY = "828d782b098af5e78cc9c73558247c2c"
client = Client(TWILIO_ACCOUNT, TWILIO_KEY)


def difference_percentage(a, b):
    return round(100 * abs(a - b) / ((a + b) / 2))


def get_news(increase_or_decrease, percentage):
    news_response = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
    news_data = news_response.json()
    news_list = [news_data["articles"][i] for i in range(3)]
    final_news = []
    prefix = ""
    if increase_or_decrease:
        prefix += "🔺"
    else:
        prefix += "🔻"
    for i in range(3):
        send_msg(f"TSLA: {prefix + str(percentage) + '%'}\nHeadline: {news_list[i]['title']}\nBrief: {news_list[i]['description']}")


def send_msg(msg):
    message = client.messages.create(
        from_="+18147475639",
        body=msg,
        to="+639184822197"
    )


two_days_ago = str(dt.date.today() - dt.timedelta(days=2))
three_days_ago = str(dt.date.today() - dt.timedelta(days=3))

response = requests.get("https://www.alphavantage.co/query", params=stock_parameters)
data = response.json()
daily_data1 = data["Time Series (Daily)"][three_days_ago]["4. close"]
daily_data2 = data["Time Series (Daily)"][two_days_ago]["4. close"]
percentage_difference = difference_percentage(float(daily_data1), float(daily_data2))

has_increase = False
if daily_data1 < daily_data2:
    has_increase = True

# if percentage_difference >= 5:
get_news(has_increase, percentage_difference)

