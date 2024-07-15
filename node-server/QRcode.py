import cv2
import requests

# 创建摄像头捕获模块
cap = cv2.VideoCapture(0)

# 创建窗口并命名
cv2.namedWindow("QR Camera", cv2.WINDOW_AUTOSIZE)

# 创建二维码检测器
qrDecoder = cv2.QRCodeDetector()

# 定义服务器端接收数据的URL
server_url = 'http://192.168.109.127:3000/receive-qrcode'

# 标志变量，用于控制程序是否退出
exit_flag = False

# 逐帧显示
while True:
    ret_val, img = cap.read()
    
    # 调整图像大小
    height, width = img.shape[0:2]
    if width > 800:
        new_width = 800
        new_height = int(new_width / width * height)
        img = cv2.resize(img, (new_width, new_height))
    
    # 二维码检测和识别
    data, bbox, _ = qrDecoder.detectAndDecode(img)
    if data is not None:
        if len(data) > 0:
            print("解码数据 : {}".format(data))
            
            # 发送POST请求将二维码数据发送到服务器
            try:
                json_data = {"qr_data": data}
                response = requests.post(server_url, json=json_data)
                print('Response status code:', response.status_code) 
                if response.status_code == 200:
                    print('QR code data sent successfully to server!')
                    # 设置退出标志为True，表示可以退出程序
                    exit_flag = True
                else:
                    print(f'Failed to send QR code data to server. Status code: {response.status_code}')
                    print(response.text)  # 输出服务器返回的详细信息
            except requests.exceptions.RequestException as e:
                print(f'Error sending QR code data to server: {e}')
        
        else:
            print("二维码解码失败")
    
    else:
        print("未检测到二维码")
    
    # 显示图像
    cv2.imshow("QR Camera", img)
    
    # 监听键盘输入并在按下ESC键时退出循环
    keyCode = cv2.waitKey(30) & 0xFF
    if keyCode == 27 or exit_flag:
        cap.release()
        cv2.destroyAllWindows()
        break

# 释放资源
