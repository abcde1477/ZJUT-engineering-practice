import requests
from bs4 import BeautifulSoup

def get_web_content(url):
    # 发送 HTTP 请求
    response = requests.get(url)

    # 手动设置编码
    response.encoding = 'utf-8'

    # 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取需要的信息
    time_row = soup.find_all('tr')[0]
    temperature_row = soup.find_all('tr')[2]
    precipitation_row = soup.find_all('tr')[3]
    wind_direction_row = soup.find_all('tr')[4]
    humidity_row = soup.find_all('tr')[5]

    # 提取数据
    time_data = time_row.find_all('td')[1].text.strip()
    temperature_data = temperature_row.find_all('td')[1].text.strip()
    precipitation_data = precipitation_row.find_all('td')[1].text.strip()
    wind_direction_data = wind_direction_row.find_all('td')[1].text.strip()
    humidity_data = humidity_row.find_all('td')[1].text.strip()

    # 将数据存储为字典或JSON格式
    weather_data = {
        "time": time_data,
        "temperature": temperature_data,
        "precipitation": precipitation_data,
        "wind_direction": wind_direction_data,
        "humidity": humidity_data
    }
    
    #print("Weather Data:")
    #print(weather_data)
    
    return weather_data

# 定义服务器端接收数据的URL
server_url = 'http://192.168.109.127:3000/receive-data'

# 获取天气数据
weather_data = get_web_content('https://weather.cma.cn/web/weather/54511.html')

# 发送POST请求将数据发送到服务器
try:
    response = requests.post(server_url, json=weather_data)
    if response.status_code == 200:
        print('Weather data sent successfully!')
    else:
        print(f'Failed to send weather data. Status code: {response.status_code}')
except requests.exceptions.RequestException as e:
    print(f'Error sending weather data: {e}')
