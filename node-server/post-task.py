import requests

# 要发送的任务数据
task_data = {
    "task_type": "fetch",
    "from": [4, 4],
    "fid": "A1",
    "color": "blue",
    "icon": "mdi-clipboard-text",
    "subtitle": "2024-7-8 13:08",
    "title": "小车前往 A[4][4] 取货"
}

# 向服务器发送 POST 请求添加任务
url = 'http://192.168.109.127:3000/car/get-all-task'
response = requests.post(url, json=task_data)

# 打印服务器的响应
print(response.status_code)
print(response.text)
