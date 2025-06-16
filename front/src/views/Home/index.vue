<template>

</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const store = mainStore();
const router = useRouter();
const message = ref('');
function navigateTo(componentName) {
  router.push({ name: componentName });
}


onMounted(() => {

});


</script>

<style scoped>
.Main {
  left: 0%;
  top: 0%;
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: rgba(135, 206, 250, 0.254);
}

</style>