import requests

url = "https://covid19india.p.rapidapi.com/getStateData/TN"

headers = {
    'x-rapidapi-host': "covid19india.p.rapidapi.com",
    'x-rapidapi-key': "6209f104damsh4bc552882960a5ap1e0542jsnecb749b0e397"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)