import cv2
import requests

def capture_and_send_qr_code(cap, server_url):
    # 创建摄像头捕获模块
    return True
    # 创建窗口并命名
    # 创建二维码检测器
    qrDecoder = cv2.QRCodeDetector()
    # 标志变量，用于控制程序是否退出
    exit_flag = False

    # 读取一帧
    ret_val, img = cap.read()
    # 调整图像大小
    height, width = img.shape[0:2]
    if width > 800:
        new_width = 800
        new_height = int(new_width / width * height)
        img = cv2.resize(img, (new_width, new_height))
    # 显示图像
    # cv2.imshow("QR Camera", img)

    data, bbox, _ = qrDecoder.detectAndDecode(img)
    if data:
        if True:
            print("解码数据 : {}".format(data))
            # 发送POST请求将二维码数据发送到服务器
            try:
                json_data = {"qr_data": data}
                response = requests.post(server_url, json=json_data)
                print('Response status code:', response.status_code)
                if response.status_code == 200:
                    print('QR code data sent successfully to server!')
                else:
                    print(f'Failed to send QR code data to server. Status code: {response.status_code}')
                    print(response.text)  # 输出服务器返回的详细信息
            except requests.exceptions.RequestException as e:
                print(f'Error sending QR code data to server: {e}')
    else:
        print("二维码解码失败")


if __name__ == '__main__':
    # 测试
    cap = cv2.VideoCapture(0)
    capture_and_send_qr_code(cap,'http://localhost:3000/receive-qrcode')  # 阻塞调用

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
