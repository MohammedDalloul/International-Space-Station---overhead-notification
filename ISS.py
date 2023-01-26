import requests
from datetime import datetime
import smtplib
import time

MY_LAT = float(input("Enter Your Location's Latitude : ")) # Your latitude
MY_LONG = float(input("Enter Your Location's Longitude : ")) # Your longitude

MY_EMAIL = input("Enter Your email address : ")
MY_PASSWD = input("Enter your email's Applications' Password : ")


def is_iss_over_me():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    else:
        return False

#Your position is within +5 or -5 degrees of the ISS position.


def is_it_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    hour_now = datetime.now().hour
    if hour_now >= sunset or hour_now <= sunrise:
        return True
    else:
        return False

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

condition = True
while condition:
    if is_iss_over_me() and is_it_dark():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=f"dalloulmohammed@yahoo.com, {MY_EMAIL}",
                            msg="subject:ISS Passing\n\nLook up! Iss is ABOVE YOU!.")
        time.sleep(60)
