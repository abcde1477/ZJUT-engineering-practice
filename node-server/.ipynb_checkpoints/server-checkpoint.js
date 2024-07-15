const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors'); // 引入cors模块
const app = express();
const port = 3000;

// 使用cors中间件处理跨域请求
app.use(cors());
// 解析 application/json 请求体
app.use(bodyParser.json());

let taskQueue = [];  // 用于存储任务的数组
let weatherData = {}; // 存储天气数据的全局变量
let qrData = {};
let mapData = null; 

// POST请求处理程序，用于接收任务并添加到任务列表
app.post('/car/get-all-task', (req, res) => {
    const newTask = req.body;  // 从请求体中获取任务数据
    taskQueue.push(newTask);   // 将任务添加到任务队列中
    console.log('添加任务:', newTask);
    res.send('任务添加成功！');
});

// POST请求处理程序，用于接收地图数据
app.post('/car/add-map', (req, res) => {
    mapData = req.body;  // 接收发送过来的地图数据
    console.log('Received map data:', mapData);
    res.send('Map data received successfully!');
});

app.get('/car/get-map', (req, res) => {
    if (mapData) {
        res.status(200).json(mapData); // 将保存的地图数据发送回客户端
    } else {
        res.status(204).send('No map data available'); // 如果没有地图数据，则返回 204 状态码
    }
});

let current_ob_Location = { x: null , y: null }; // 初始位置示例
// POST请求处理程序，用于接收障碍物位置信息
app.post('/car/add-obstacle-location/:x/:y', (req, res) => {
    const { x, y } = req.params;
    console.log(`报告障碍物位置: (${x}, ${y})`);
    current_ob_Location = { x, y };
    // 构建要返回的 JSON 响应体
    const response_ob = {
        x: x,
        y: y
    };
    res.status(200).json(response_ob);
});

// GET请求处理程序，获取障碍物最新位置
app.get('/car/get-current-obstacle-location', (req, res) => {
     res.status(200).json(current_ob_Location);
});



// POST请求处理程序，报告小车无法到达目标
app.post('/car/unreachable', (req, res) => {
    // 根据具体逻辑处理报告不可达
    console.log('报告小车不可达');
    res.status(200).json({});
});
let counter =0

// GET请求处理程序，查询障碍物是否已清除
app.get('/car/is-obstacle-cleared', (req, res) => {
    // 根据具体逻辑处理查询障碍物是否已清除
    // 假设障碍物已清除
    counter++
    let obstacle_clear
    let jsondata
    if( counter > 5){
       jsondata = {"obstacle":"yes"}
    }else{
        jsondata = {"obstacle":"no"}
    }
    res.status(200).json(jsondata);
});

// 修改原有的GET请求处理程序，用于小车获取任务
app.get('/car/get-task', (req, res) => {
    console.log(taskQueue);
    if (taskQueue.length > 0) {
        const task = taskQueue.pop(); // 弹出队列中的最后一个任务
        console.log('分配任务:', task);
        res.status(200).json(task);
    } else {
        // 如果任务队列为空，返回状态码 204 和空的响应体
        res.status(204).json({});
    }
});

// 修改原有的GET请求处理程序，用于小车获取任务
app.get('/car/get-all-task', (req, res) => {
    console.log(taskQueue);
    res.status(200).json(taskQueue);
});

// PUT请求处理程序，报告小车位置
let currentLocation = { x: 0, y: 0 }; // 初始位置示例
app.put('/car/report-location/:x/:y', (req, res) => {
    const { x, y } = req.params;
    console.log(`报告小车位置: (${x}, ${y})`);
    currentLocation = { x, y };
    // 构建要返回的 JSON 响应体
    const response = {
        x: x,
        y: y
    };
    res.status(200).json(response);
});

// GET请求处理程序，获取小车最新位置
app.get('/car/get-current-location', (req, res) => {
    res.status(200).json(currentLocation);
});



// POST请求处理程序，接收天气数据
app.post('/receive-data', (req, res) => {
   weatherData = req.body;
   console.log('Received weather data:', weatherData);
   res.send('Weather data received successfully!');
});

// POST 请求处理程序，接收二维码数据
app.post('/receive-qrcode', (req, res) => {
   qrData = req.body.qr_data;
   console.log('Received QR code data:', qrData);
   // 响应客户端
   res.send('QR code data received successfully!');
});


// GET请求处理程序，返回存储的天气数据
app.get('/weather-data', (req, res) => {
   res.setHeader('Access-Control-Allow-Origin', '*');
   res.json(weatherData);
});

// GET请求处理程序，返回存储的QR数据
app.get('/QRcode-data', (req, res) => {
   res.setHeader('Access-Control-Allow-Origin', '*');
   res.json(qrData);
});

// 启动服务器
app.listen(port, () => {
   console.log(`Server is running at http://localhost:${port}`);
});
