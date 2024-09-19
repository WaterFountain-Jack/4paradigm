import requests
import pandas as pd
import json
import os

PORT=int(os.environ.get('PORT', '80'))

# 从CSV文件中读取数据
csv_file_path = '/root/test/m10/data/w_0812_0827.train.csv'
df = pd.read_csv(csv_file_path)

# 随机抽样20行数据
sampled_data = df.sample(n=20).to_dict(orient='records')

# 设置请求URL
ready_url = f'http://0.0.0.0:{PORT}/ready'
predict_url = f'http://0.0.0.0:{PORT}/predict'

# 发送 /ready 请求
try:
    ready_response = requests.get(ready_url)
    if ready_response.status_code == 200 and ready_response.json().get('ready'):
        print("Model is ready")
    else:
        print("Failed to load model")
        exit(1)
except requests.exceptions.Timeout:
    print("The /ready request timed out")
    exit(1)
except requests.exceptions.RequestException as e:
    print(f"An error occurred with /ready request: {e}")
    exit(1)

# 设置请求头
headers = {'Content-Type': 'application/json'}

# 发送 /predict 请求
try:
    response = requests.post(predict_url, headers=headers, data=json.dumps({'data': sampled_data}), timeout=0.1)
    print(response.json())
except requests.exceptions.Timeout:
    print("The /predict request timed out")
except requests.exceptions.RequestException as e:
    print(f"An error occurred with /predict request: {e}")