import requests

#POST
'''
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
'''

#GET
'''
url = "http://localhost:8000/users/64636f0c6b92989aee570127"

response = requests.get(url)

print(response.json())
'''

#get_all_users
'''
url = "http://localhost:8000/users"

response = requests.get(url)

print(response.json())
'''

#PUT
'''
import requests

url = "http://localhost:8000/users/64637669862476104bc44fae"  # 업데이트할 사용자 ID에 맞게 변경해주세요
data = {
    "name": "Updated Name",
    "email": "updatedemail@example.com"
}

response = requests.put(url, json=data)

print(response.json())
'''

#DELETE
'''
url = "http://localhost:8000/users/64636f0c6b92989aee570127"

response = requests.delete(url)

print(response.json())
'''
