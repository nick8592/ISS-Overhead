import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 23.697809 # Your latitude
MY_LONG = 120.960518 # Your longitude
TIME_ZONE = 8 # Your time-zone
MY_EMAIL = "birthdayman32@outlook.com"
MY_PASSWORD = "!@#QWE123"


def compare_position():
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.
is_nearby = compare_position()
print(is_nearby)


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("http://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + TIME_ZONE
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + TIME_ZONE
if sunrise > 24:
    sunrise -= 24
if sunset > 24:
    sunset -= 24
time_now = datetime.now()


#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
while True:
    time.sleep(60)
    if is_nearby:
        if time_now.hour <= sunrise or time_now.hour >= sunset:
            with smtplib.SMTP("smtp.outlook.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL,
                                    to_addrs="birthdaywisher32@gmail.com",
                                    msg=f"Subject:Look Up!!!"
                                        f"\n\nLook up! International Space Station (ISS) is above you in the sky.")




