import requests
import json

# 定义API的URL
train_data_url = "http://localhost:18089/train_data"  # 将localhost替换为你的服务器地址
predict_url = 'http://localhost:18089/predict'
data_source_url = 'http://localhost:18089/datasource'

# 设置请求头
headers = {
    "Content-Type": "application/json"
}


datasource_body = {
  "name": "gyhh",
  "display_name": "gyhh",
  "description": "新能源，燃油车市场销量数据",
  "driver": "mysql",
  "username": "root",
  "password": "hiU0i1XYM3",
  "host": "172.26.1.64",
  "port": "30361",
  "tables": [
    "new_energy_vehicle_sales",
    "new_energy_vehicle_model_sales",
    "new_energy_vehicle_city_sales"
  ]
}
train_data_body = {

    
    "data": [
    {
        "query": "SELECT * FROM users WHERE age > 30",
        "sql": "SELECT * FROM users WHERE age > 30",
        "order": True  # 布尔值
    },
    {
        "query": "SELECT name FROM users WHERE active = 1",
        "sql": "SELECT name FROM users WHERE active = 1",
        "order": False  # 布尔值
    }
]
}
image_info = {
  "name": "nev-car-sales",
  "image": "harbor.4pd.io/lab-platform/pk_platform/model_services/mymysql:v4",
  "port": [
    3306
  ],
  "pwd": "123456"
}

predict_body = {
    "model": "qwen-72b",  #可以忽略
    "messages":  [
        {
            "role": "user",
            "content": "去年一年的总保费",
        }
    ],  # 会话历史
    "stream": True,  # bool, 是否流式响应    
    "stop": "<IAMSTOP>", # str, 流式返回结束符，返回在finish_reason里
    "max_tokens": 4096 #可以忽略
 }



# 发送POST请求
# response = requests.post(train_data_url, headers=headers, json=train_data_body)
response = requests.post(data_source_url, headers=headers, json=datasource_body)
# response = requests.post(predict_url, headers=headers, json=predict_body)

# 检查响应状态码
if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Failed to call API. Status code:", response.status_code)
    print("Response:", response.text)
