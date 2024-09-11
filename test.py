import requests

url = 'http://172.20.10.14/receive_device_id'
data = {'id': 'goodlock2u'}  # Replace 'your_device_id_here' with a test device ID

response = requests.post(url, data=data)

print(response.status_code)
print(response.text)