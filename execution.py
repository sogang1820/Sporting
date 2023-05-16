import requests

url = "http://localhost:8000/users"
data = {
    "name": "John Doe",
    "email": "johndoe@example.com"
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
