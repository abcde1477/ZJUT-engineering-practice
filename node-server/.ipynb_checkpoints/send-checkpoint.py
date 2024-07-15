import requests

url = 'http://192.168.109.127:/receive-data'  # 替换为Node.js服务器的地址和接收数据的端点
data = {'message': 'Hello from Jetson Nano!'}

response = requests.post(url, json=data)

if response.status_code == 200:
    print('Data sent successfully!')
else:
    print(f'Failed to send data. Status code: {response.status_code}')

    
    #  // 设置CORS头部
# res.setHeader('Access-Control-Allow-Origin', '*');
  #res.setHeader('Access-Control-Allow-Methods', 'GET');
 # res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');