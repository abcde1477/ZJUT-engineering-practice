<script>
import axios from 'axios';
import jsQR from 'jsqr';

export default {
  data() {
    return {
      weatherData: null,
      qrCodeData: '', // 初始化为空字符串，扫描到二维码后更新内容
      scanning: false,
      video: null,
      canvas: null,
      context: null,
      animationFrameId: null,

    };
  },

  mounted() {
    // 发送GET请求获取天气数据
    axios.get('http://192.168.109.127:3000/weather-data')
      .then(response => {
        this.weatherData = response.data;
        console.log('Received weather data:', this.weatherData);
      })
      .catch(error => {
        console.error('Error fetching weather data:', error);
      });
    // 发送 HTTP GET 请求获取从 Node.js 服务器发送的二维码数据
    this.fetchDataAndUpdateMap();
  },

  methods: {
    async toggleScan() {
      if (!this.scanning) {
        // 启动扫描
        this.video = this.$refs.video;
        this.canvas = this.$refs.canvas;
        this.context = this.canvas.getContext('2d');

        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
            this.video.srcObject = stream;
            this.video.play();
            this.scanning = true;
            this.tick();
          } catch (error) {
            console.error("Error accessing the camera: ", error);
            alert('无法访问摄像头，请检查权限或设备。');
          }
        } else {
          alert('对不起，您的浏览器不支持访问摄像头。');
        }
      } else {
        // 停止扫描
        if (this.video && this.video.srcObject) {
          const stream = this.video.srcObject;
          const tracks = stream.getTracks();

          tracks.forEach(track => {
            track.stop();
          });

          this.video.srcObject = null;
          cancelAnimationFrame(this.animationFrameId);
          this.scanning = false;
        }
      }
    },

    tick() {
      if (this.video.readyState === this.video.HAVE_ENOUGH_DATA) {
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
        this.context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
        const imageData = this.context.getImageData(0, 0, this.canvas.width, this.canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);

        if (code) {
          console.log('二维码数据:', code.data); // 打印二维码数据，检查其格式是否正确

          try {
            let qrData = JSON.parse(code.data); // 尝试解析二维码数据为对象

            this.qrCodeData = `QR码数据: ${qrData}`;

            const data = {
              qrCodeData: qrData
            };

            fetch('http://192.168.109.127:3000/car/get-all-task', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(data)
            })
              .then(response => {
                if (!response.ok) {
                  throw new Error(`HTTP 错误! 状态: ${response.status}`);
                }
                return response.json(); // 如果服务器返回 JSON 数据，可以进一步处理
              })
              .then(responseData => {
                console.log('服务器返回的数据:', responseData);
                // 在这里处理服务器返回的数据
              })
              .catch(error => {
                console.error('发生错误:', error);
              });
          } catch (error) {
            console.error('解析二维码数据时发生错误:', error);
          }
        }
      }
      this.animationFrameId = requestAnimationFrame(this.tick);
    },


    fetchDataAndUpdateMap() {
      axios.get('http://192.168.109.127:3000/QRcode-data')
        .then(response => {
          const qrdata = response.data;
          console.log('接收到的QR码数据:', qrdata);
          this.updateMapWithQRData(qrdata); // 使用 this.updateMapWithQRData() 更新地图
        })
        .catch(error => {
          console.error('获取QR码数据时出错:', error);
        });
    },

    updateMapWithQRData(newRowString) {
      // 清理并解析 newRowString
      const cleanedRowString = newRowString.trim().replace(/[\r\n]+/g, '');

      try {
        // 解析为 JSON 数组
        const newRow = JSON.parse(cleanedRowString);

        // 生成坐标数组
        const coordinates = newRow.reduce((acc, value, index) => {
          if (value === 1) {
            acc.push([0, index]); // 在第一行添加坐标 [0, index]
          }
          return acc;
        }, []);

        // 更新地图的第一行
        if (coordinates.length > 0) {
          // 假设 map 是您的地图数据对象，确保 map.value 是一个数组
          if (map.value.length > 0) {
            map.value[0] = [...coordinates]; // 更新地图的第一行
          } else {
            console.error('地图对象中没有初始化数据。');
          }
        } else {
          console.error('新行数据中未找到值为1的索引。');
        }
      } catch (error) {
        console.error('解析新行数据时出错:', error.message);
      }
    },
  },
};

</script>
