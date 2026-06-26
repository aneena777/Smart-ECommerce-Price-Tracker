import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText

# Product URL
URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# User Inputs
user_email = input("Enter your email: ")
user_phone = input("Enter your phone number: ")
TARGET_PRICE = float(input("Enter your target price: "))

headers = {
    "User-Agent": "Mozilla/5.0"
}


def get_price():
    try:
        response = requests.get(URL, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        price_tag = soup.find("p", class_="price_color")

        if price_tag is None:
            print("Price element not found!")
            return None

        price_text = price_tag.text.strip()

        price = float(
            ''.join(ch for ch in price_text if ch.isdigit() or ch == '.')
        )

        return price

    except Exception as e:
        print("Error:", e)
        return None


def save_price(price):
    filename = "price_history.csv"

    data = {
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Price": [price]
    }

    df = pd.DataFrame(data)

    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)
def send_email(receiver_email, price):
    print("\n----- EMAIL NOTIFICATION -----")
    print("To:", receiver_email)
    print("Subject: Price Drop Alert!")
    print(f"The product price has dropped to ₹{price}.")
    print("Email notification sent successfully (Simulation).")
    print("------------------------------")



def check_price():
    price = get_price()

    if price is None:
        return

    print("Current Price:", price)

    save_price(price)

    if price <= TARGET_PRICE:
        print("PRICE DROPPED! BUY NOW!")

        # Email Notification
        send_email(user_email, price)

        # SMS Placeholder
        print("SMS notification would be sent to:", user_phone)

    else:
        print("Price is above target price.")


if __name__ == "__main__":
    check_price()