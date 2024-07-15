import time
import numpy as np
from setCamera import *

from base import PIDController



def get_dir(img):
    # 对图像进行提亮操作
    alpha = 1.5  # 对比度控制 (1.0-3.0)
    beta = 50  # 亮度控制 (0-100)
    img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)

    # 应用高斯模糊以减少噪声
    img = cv.GaussianBlur(img, (5, 5), 0)

    # 获取图像的高度和宽度
    height, width = img.shape[:2]

    # 计算下1/4部分的起始行
    start_row = 3 * height // 4

    # 创建 img 的副本 img1 并将上3/4部分设置为黑色
    img1 = img.copy()
    img1[:start_row, :] = 0

    # 截取下1/4部分
    img_lower = img[start_row:, :]

    # 转换为灰度图
    gray_lower = cv.cvtColor(img_lower, cv.COLOR_BGR2GRAY)

    # 使用大津法进行二值化
    ret, binary_lower = cv.threshold(gray_lower, 10, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    binary_lower = cv.bitwise_not(binary_lower)

    # 创建核进行膨胀和腐蚀处理
    kernel = np.ones((3,3), np.uint8)

    # 腐蚀处理
    eroded = cv.erode(binary_lower, kernel, iterations=1)

    # 提取轮廓
    contours, hierarchy = cv.findContours(eroded, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # 找到最大的轮廓
    if contours:
        max_contour = max(contours, key=cv.contourArea)

        # 创建一个与 img_lower 相同大小的黑色图像
        mask = np.zeros_like(eroded)

        # 绘制最大的轮廓，将其填充为白色
        cv.drawContours(mask, [max_contour], -1, 255, thickness=cv.FILLED)

        # 将掩码应用于原始图像的下半部分
        white_fill = np.full_like(img_lower, 255)
        img_lower_masked = cv.bitwise_and(white_fill, white_fill, mask=mask)

        # 将处理后的结果放回原图像副本的相应位置
        img1[start_row:, :] = img_lower_masked

        # 腐蚀处理
        img1 = cv.erode(img1, kernel, iterations=2)

        sorted_contour = sorted(max_contour, key=lambda point: point[0][1])

        points_by_y = {}
        for point in sorted_contour:
            x, y = point[0]
            if y not in points_by_y:
                points_by_y[y] = []
            points_by_y[y].append(x)

        direction = []
        for y, x_values in points_by_y.items():
            x_values.sort()
            for i in range(0, len(x_values), 3):
                segment = x_values[i:i+5]
                avg_x = int(np.mean(segment))
                cv.circle(img1, (avg_x, y + start_row), 3, (0, 0, 255), -1)
                direction.append(avg_x)

        direction_out = np.mean(direction)
        return direction_out, img1
    else:
        return None, img1


def cali_control_bot(center_x, width, bot, pid, prev_time):
    # 根据黑线的中心位置调整小车运动方向
    if center_x == None:
        error = 0
    else:
        error = center_x - width // 2
    
    error = error / 60

    if error < 0:
        error -= 0.15
    else:
        error += 0.15

    if abs(error) < 0.2:
        error = 0
    # print(error)
    if error > 0:
        bot.set_car_motion(0, 0, -0.55)# -0.4
        # print("left! adjust!!!")
    elif error < 0:
        bot.set_car_motion(0, 0, 0.55)
        # print("right! adjust!!!")
    if error == 0:
        bot.set_car_motion(0, 0, 0)

    return 0


def cali_line(cap, pid, bot):
    print("start_cali_to_the_line")
    cali_start = time.time()
    count = 0
    while time.time() - cali_start < 5:
        ret, frame = cap.read()
        # print(frame.shape)
        # cv.imwrite("1.png", frame)

        if not ret:
            print('break')
            break
        center_x, binary_frame = get_dir(frame)
        cali_time = cali_control_bot(center_x, frame.shape[1], bot, pid, cali_start)
        # cv.imshow('img',frame)
        # cv.imshow('binary', binary_frame)

        if cv.waitKey(1) & 0xFF == ord(' '):
            break
    bot.set_car_motion(0, 0, 0)

