<script setup lang="ts">

</script>

<template>
  <router-view></router-view>
  <el-button type="primary" @click="() => $router.push('/')">返回首页</el-button>
</template>

<style>
#app {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>