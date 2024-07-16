# ZJUT-engineering-practice

## 项目简介
这是浙江工业大学工程实践的小组作业。使用智能小车验证各模块并做出创意化设计。此仓库存放我们小组的项目代码。  
我们小组选用的智能小车是亚博智能公司推出的ROSMASTER X1，无转机构的四驱小车。  
组件包括:深度摄像头, 激光雷达, 蜂鸣器, RGB炫彩灯条。板子是jetson nano 4GB。  
此套件把ROS放在了产品名称上，所以在使用这个小车的时候，不可避免的需要学习很多ROS相关的知识。很多原厂自带的代码和功能是使用ROS功能包进行封装的。  

## 小组设计
我们的小组设计是一个智能货运机器人。在矩阵地图中执行取货指令，在地图中自行寻路，到达指定地点后返回。

## 代码存放
node-server为服务器部分代码，使用node.js  
vuetify-project为前端代码，使用vue框架  
ws为小车执行逻辑代码，雷达功能封装ROS功能包中，carry_robot.py是小车执行代码的运行脚本

## 启动方式
`roscore`启动ROS核心  
`rolaunch yahboomcar_carry_robot obstacle_laser.lanuch`启动雷达避障功能
`python ws/src/yahboomcar_carry_robot/scripts/carry_robot.py`启动小车  
`node node-server/server.js`启动后端服务器

小车代码会阻塞的对后端服务器请求，如果后端服务器没有运行，小车将无法正常运行。