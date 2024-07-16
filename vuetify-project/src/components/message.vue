<template>
  <v-card class="mx-auto" max-width="600">
    <v-toolbar color="secondary">
      <v-btn icon variant="text" v-tooltip="'下列为实时更新的任务列表'">
        <v-icon>mdi-menu</v-icon>
      </v-btn>
      <v-toolbar-title>任务队列</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>

    <v-list>
      <v-list-item style="height: 8vh" v-for="task in tasks" :key="task.fid">
        <v-list-item-avatar style="position: absolute;top:1vh">
          <v-avatar :color="task.color">
            <v-icon dark>{{ task.icon }}</v-icon>
          </v-avatar>
        </v-list-item-avatar>

        <v-list-item-content style="position: absolute;left:5vw;top:1.5vh">
          <v-list-item-title >{{ task.title }}</v-list-item-title>
          <v-list-item-subtitle>{{ task.subtitle }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-list-item-action style="position: absolute;right: 1vw;top:0.5vh">
          <v-btn v-tooltip="'任务序号：' + task.fid" color="grey lighten-1" icon>
            <v-icon>mdi-clipboard-text</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';

const tasks = ref([]);

onMounted(() => {
  // Adjust the API endpoint URL accordingly
  axios.get('http://192.168.109.127:3000/car/get-all-task')
    .then(response => {
      tasks.value = response.data; // Assuming response.data is an array of tasks
      console.log('获取到的任务:', tasks.value);
    })
    .catch(error => {
      console.error('获取任务失败:', error);
    });
});

// Optionally, if you want to refresh tasks periodically
setInterval(() => {
  axios.get('http://192.168.109.127:3000/car/get-all-task')
    .then(response => {
      tasks.value = response.data;
      console.log('获取到的任务:', tasks.value);
    })
    .catch(error => {
      console.error('获取任务失败:', error);
    });
}, 2000);
</script>


<style>
.mx-auto{
  position: absolute;
  left:35vw;
  width: 30vw;
  height: 100vh;
}

</style>
