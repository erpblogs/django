import requests

url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

querystring = {"term":"wat"}

headers = {
	"X-RapidAPI-Key": "ed7276993bmsh6ebcf60e623573bp197815jsn2d56512b9625",
	"X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)