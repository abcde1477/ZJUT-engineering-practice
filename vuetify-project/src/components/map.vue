<template>
  <div id="app">
    <div class="top"style="background-color: #12bce1;height: 8.2vh">
      <div class="h2" style="">物流小车取件系统</div><br>
    </div>
    <v-divider :thickness="10"></v-divider>
    <br>
    <div class="grid-container">
      <div v-for="(row, rowIndex) in map" :key="rowIndex" class="row">
        <div v-for="(cell, colIndex) in row" :key="colIndex"
             :class="['cell', getCellClass(cell)]">
          {{ '[' + rowIndex + '][' + colIndex + ']' }}
        </div>
      </div>
    </div>
  </div>
  <div>
    <button  class="no-cursor-change" @click="showAlert" style="background-color: #ffffff;position: absolute; top:10.3vh;left:60vw; width: 1vw">-</button>

  </div>
  <div class="sign">
    <div>
      <div style="float:left;position:absolute;top:2vh;width:3.5vh;height:3.5vh;border:black 1px solid;background-color: #555555"></div>
      <div style="float: left;margin-left: 2vw;margin-top: 2vh">:&nbsp;墙</div>
      <div style="float:left;position:absolute;top:6vh;width:3.5vh;height:3.5vh;border:black 1px solid;background-color: #3ef828"></div>
      <div style="float: left;margin-left: 2vw;margin-top: 1vh">:&nbsp;货物</div>
      <div style="float:left;position:absolute;top:10vh;width:3.5vh;height:3.5vh;border:black 1px solid;background-color: #ff0000"></div>
      <div style="float: left;margin-left: 2vw;margin-top: 1vh">:&nbsp;障碍物</div>
      <div style="float:left;position:absolute;top:14vh;width:3.5vh;height:3.5vh;border:black 1px solid;background-color: #ffffff"></div>
      <div style="float: left;margin-left: 2vw;margin-top: 1vh">:&nbsp;空气</div>

      <div style="float:left;position:absolute;top:18vh;width:3.5vh;height:3.5vh;border:black 1px solid;background-color: #f39c12"></div>
      <div style="float: left;margin-left: 2vw;margin-top: 1vh">:&nbsp;路径</div>
    </div>
  </div>
  <div class="info" >
    <h2 style=" color: #336551;font-size: 26px;font-weight: bold;font-family: YouYuan,serif;">输入取件码取件</h2>
    <!-- 选择方式的表单 -->

    <form @submit.prevent="submitForm" style="left: 4.5vw;margin-top: 2vh;background-color: white;">

      <label for="pickupCodeInput" style="font-size: 20px">取件码：</label>

      <input  v-model="pickupCode" style="width: 20vw;height:4.5vh;color: black;border:black 1.5px solid" type="text" id="pickupCodeInput;" required>

      <button type="submit"style="width: 5vw;text-align: center">读取</button>
    </form>
    <!-- 展示结果 -->
    <div v-if="result">
      <p>读取到的信息：{{ result }}</p>
    </div>
  </div>

</template>

<script>
import axios from 'axios';
import { onMounted, ref } from 'vue';

const map = ref([]);

onMounted(() => {
  // 调整 API 请求地址
  axios.get('http://192.168.109.127:3000/car/get-map')
    .then(response => {
      // 假设服务器返回的是一个数组
      map.value = response.data;
      console.log('获取到的地图:', map.value);
    })
    .catch(error => {
      console.error('获取地图失败:', error.message);
     this.errorMessage = '获取地图失败，请检查网络连接或服务器配置。';
    });
});

// 可选：定时刷新地图数据

  axios.get('http://192.168.109.127:3000/car/get-map')
    .then(response => {
      map.value = response.data;
      console.log('获取到的地图:', map.value);
    })
    .catch(error => {
      console.error('获取地图失败:', error);
    });


async function fetchAndUpdateMap() {
  try {
    // 发起请求获取当前坐标
    const response = await fetch('http://192.168.109.127:3000/car/get-current-location', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // 检查响应状态
    if (!response.ok) {
      throw new Error(`HTTP 错误! 状态: ${response.status}`);
    }

    // 解析响应数据
    const data = await response.json();
    console.log('获取的坐标数据:', data);

    // 将字符串类型的坐标转换为数字
    const xCoordinate = parseFloat(data.x);
    const yCoordinate = parseFloat(data.y);

    // 更新地图上指定坐标的值为 5
    map.value[xCoordinate][yCoordinate] = 5;
    console.log('更新后的地图:', map.value);

    console.log(`当前坐标: (${xCoordinate}, ${yCoordinate})`);

  } catch (error) {
    // 处理错误
    console.error('发生错误:', error);
  }
}
setInterval(fetchAndUpdateMap, 2000);
export default {
  methods: {
    showAlert() {
      alert('目标不可到达。请检查小车环境，并清除障碍物');
    }
  }
};
async function fetchobAndUpdateMap() {
  try {
    // 发起请求获取当前坐标
    const response = await fetch('http://192.168.109.127:3000/car/get-current-obstacle-location', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // 检查响应状态
    if (!response.ok) {
      throw new Error(`HTTP 错误! 状态: ${response.status}`);
    }

    // 解析响应数据
    const data = await response.json();
    console.log('获取的坐标数据:', data);

    // 将字符串类型的坐标转换为数字
    const xCoordinate2 = parseFloat(data.x);
    const yCoordinate2 = parseFloat(data.y);

    // 更新地图上指定坐标的值为 3
    map.value[xCoordinate2][yCoordinate2] = 3;
    console.log('更新后的地图:', map.value);

    console.log(`当前坐标: (${xCoordinate2}, ${yCoordinate2})`);

  } catch (error) {
    // 处理错误
    console.error('发生错误:', error);
  }
}


setInterval(fetchobAndUpdateMap, 2000);
const result = ref(''); // 用来展示读取到的信息
const pickupCode = ref('');

function getFormattedDateWithOffset(hoursOffset) {
  const now = new Date();
 now.setHours(now.getHours() + hoursOffset); // 增加小时数
const year = now.getFullYear();
const month = String(now.getMonth() + 1).padStart(2, '0'); // 月份从0开始
const day = String(now.getDate()).padStart(2, '0');
const hours = String(now.getHours()).padStart(2, '0');
const minutes = String(now.getMinutes()).padStart(2, '0');
const seconds = String(now.getSeconds()).padStart(2, '0');

return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;

}
// Vue组件或setup函数
const submitForm = async () => {
  // 获取输入的取件码值（使用pickupCode.value）
  const code = pickupCode.value.trim();

  // 打印检查输入的取件码值
  console.log('输入的取件码值:', code);

  // 将输入转换为字符串并拆分为 x 和 y 坐标
  const [xStr, yStr] = code.split('-');
  const x = parseInt(xStr, 10);
  const y = parseInt(yStr, 10);

  // 检查 x 和 y 是否为有效坐标
  if (!isNaN(x) && !isNaN(y) && x >= 0 && x < map.value.length && y >= 0 && y < map.value[0].length) {
    // 更新 map 数组中对应位置为 1
    map.value[x][y] = 2;

    // 可以打印更新后的 map 数组进行调试或确认
    console.log('更新后的 map:', map.value);

    // 构建要发送的数据对象
    const data = {
      task_type: "fetch",
      from: [x, y],
      fid: "A1",  // 假设 fid 固定为 "A1"，根据需要进行修改
      color: "blue",  // 颜色属性，如果需要动态设置可以调整
      icon: "mdi-clipboard-text",  // 图标属性，如果需要动态设置可以调整
      subtitle: getFormattedDateWithOffset(0.5), // 使用函数获取加8小时后的时间
      title: `小车前往 A[${x}][${y}] 取货`
    };

    try {
      const response = await fetch('http://192.168.109.127:3000/car/get-all-task', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP 错误! 状态: ${response.status}`);
      }

      const responseData = await response.json();
      console.log('服务器返回的数据:', responseData);
    } catch (error) {
      console.error('发生错误:', error);
    }
  } else {
    console.error('无效的坐标:', x, y);
  }
};

// 示例调用 submitForm 函数以触发表单提交和数据发送
submitForm();

// 定义一个数组来映射每个单元格的类名
const cellClasses = ['empty', 'wall','container', 'obstacle',  'path', 'car'];

// 根据单元格的值获取对应的类名
function getCellClass(cellValue) {
  return cellClasses[cellValue] || 'unknown'; // 处理无效值
}


</script>

<script setup>
import { ref } from 'vue';

</script>

<style scoped>
.no-cursor-change {
  cursor: default; /* 设置鼠标样式为默认样式，不会变形 */
}
.grid-container{
  padding: 20px;
  position: absolute;
  left:7vw;
  line-height: 30px;
  font-weight: bold;
  color: #000000;
  box-shadow: 0 0 0 5px white;
  outline: dashed 10px #457b8f;
  background-color: rgba(180,177,177,0.7);
}
#app {
  color: black;
}
.h2{
  margin-left: 16vw;
  position:absolute;
  top:10px;
  color:white;
  font-size: 28px;
  font-family: YouYuan,serif;
}
.row {
  display: flex;
  justify-content: center;
}

.cell {
  text-align: center;
  width: 50px;
  height: 50px;
  border: 1px solid #ccc;
  margin: 1px;
}

.wall {
  background-color: #555; /* 墙的颜色 */
}

.container {
  background-color: #3ef828; /* 货柜的颜色 */
}

.obstacle {
  background-color: #ff0000; /* 障碍物的颜色 */
}

.empty {
  background-color: #fff; /* 空格的颜色 */
}

.path {
  background-color: #9d10ff; /* 路径的颜色 */
}

.car {
  background-color: #f39c12; /* 小车的颜色 */
}

.sign {
  position:absolute;
  left:60vw;
  top: 11vh;
  width: 8vw;
  height: 30vh;
  font-weight: bold;
  color: black;
  background-color: rgba(180,177,177,0.7);
  padding-left: 15px;
  border-radius: 10px;
  border:rgba(133,150,150,0.5) 2px solid
}

.info{
  font-size: 13px;
  text-align: center;
  color: black;
  background-color: rgba(253, 230, 224, 0.8);
  border-radius:5px;
  position: absolute;
  top:80vh;
  width: 43vw;
  left:6.2vw;
  height:18vh;
  border: black 1px solid;
}


/* 设置网格栏X和Y轴 */
.cell:first-child::before {
  content: attr(data-x);
  position: absolute;
  top: -30px; /* X轴的位置 */
  left: 0;
  width: 100%;
  text-align: center;
}

.row:first-child .cell::before {
  content: attr(data-y);
  position: absolute;
  top: 0;
  left: -40px; /* Y轴的位置 */
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  transform: rotate(-90deg); /* Y轴文字旋转 */
}
form {
  border:black 2px solid;
  margin-bottom: 20px;
  position: absolute;
  color: black;
}

input {
  margin-left: 10px;
}

</style>
