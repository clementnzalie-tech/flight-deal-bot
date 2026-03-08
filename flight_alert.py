import os
import requests

origin = "LHR"
destination = "JFK"
departure = "2026-04-10"
return_date = "2026-04-20"
budget = 300

token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"

data = {
    "grant_type": "client_credentials",
    "client_id": os.environ["AMADEUS_API_KEY"],
    "client_secret": os.environ["AMADEUS_API_SECRET"]
}

r = requests.post(token_url, data=data)
token = r.json()["access_token"]

search_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"

params = {
    "originLocationCode": origin,
    "destinationLocationCode": destination,
    "departureDate": departure,
    "returnDate": return_date,
    "adults": 1,
    "max": 5,
    "currencyCode": "GBP"
}

headers = {"Authorization": f"Bearer {token}"}

response = requests.get(search_url, headers=headers, params=params)

flights = response.json()["data"]

for flight in flights:
    price = float(flight["price"]["total"])

    if price <= budget:

        message = f"Cheap flight found: £{price} {origin}->{destination}"

        requests.post(
            f"https://ntfy.sh/{os.environ['NTFY_TOPIC']}",
            data=message.encode("utf-8")
        )
