<template>
  <v-app>
    <v-main>
      <message/>
    </v-main>
    <div class="map1">
      <Map />
    </div>
    <getweather/>

  </v-app>

</template>

<script setup>
import Message from "@/components/message.vue";
import Map from "@/components/map.vue";
import getweather from "@/components/getweather.vue";
</script>
<style>

.map1{
  left: 0;
  background-color: #EAEAEF;
  height: 100vh;
  position: absolute;
  width: 69.5vw;
}
</style>
