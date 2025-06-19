<template>

</template>


<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import courseImg from '../../assets/images/course.png'
const store = mainStore();
const router = useRouter();

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
  overflow: auto;
  background-color: rgba(135, 206, 250, 0.254);
  padding: 20px;
}


</style>
