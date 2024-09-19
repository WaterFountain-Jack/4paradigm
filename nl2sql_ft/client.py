import requests

# 服务器地址和端点
url = "http://127.0.0.1:81/train_data/"

# 要发送的数据
data = {
    "name": "Apple",
    "description": "A sweet red fruit",
    "price": 1.99,
    "tax": 0.2
}

# 发送POST请求
response = requests.post(url, json=data)

# 打印服务器的响应
print(f"Status Code: {response.status_code}")
print(f"Response JSON: {response.json()}")
