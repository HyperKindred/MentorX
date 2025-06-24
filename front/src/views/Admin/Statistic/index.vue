<template>
    <div class="main">
        <div ref="S_chartRef" style="width: 400px; height: 400px;"></div>
        <div ref="T_chartRef" style="width: 400px; height: 400px;"></div>
    </div>

</template>

<script lang="ts" setup>
import { ref, onMounted, watch, computed, onBeforeUnmount } from 'vue';
import * as echarts from 'echarts'
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
const store = mainStore();
const S_stats = ref({
  AiChat: 0,
  exercises: 0,
  check: 0
});
const T_stats = ref({
  courseware: 0,
  exercises: 0,
  check: 0
});

const S_chartRef = ref<HTMLElement | null>(null)
const T_chartRef = ref<HTMLElement | null>(null)
let S_chartInstance: echarts.ECharts | null = null
let T_chartInstance: echarts.ECharts | null = null
onMounted(() => {
    getSystemState();
    S_renderChart();
    T_renderChart();
});
onBeforeUnmount(() => {
  S_chartInstance?.dispose();
  T_chartInstance?.dispose();
});

const S_pieData = computed(() => [
  { value: S_stats.value.AiChat, name: 'AI聊天板块' },
  { value: S_stats.value.exercises, name: '生成习题版块' },
  { value: S_stats.value.check, name: '批改习题版块' },
]);

const T_pieData = computed(() => [
  { value: T_stats.value.courseware, name: '生成课件版块' },
  { value: T_stats.value.exercises, name: '生成习题版块' },
  { value: T_stats.value.check, name: '批改习题版块' },
]);

const S_renderChart = () => {
  if (!S_chartRef.value) return

  S_chartInstance = echarts.init(S_chartRef.value)
  S_chartInstance.setOption({
    title: {
      text: '学生模块使用情况',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '使用频率',
        type: 'pie',
        radius: '60%',
        data: S_pieData.value,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  })
}

watch(S_pieData, () => {
  if (S_chartInstance) {
    S_chartInstance.setOption({
      series: [{ data: S_pieData.value }]
    });
  } else {
    S_renderChart(); 
  }
}, { immediate: true, deep: true });


const T_renderChart = () => {
  if (!T_chartRef.value) return

  T_chartInstance = echarts.init(T_chartRef.value)
  T_chartInstance.setOption({
    title: {
      text: '教师模块使用情况',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '使用频率',
        type: 'pie',
        radius: '60%',
        data: T_pieData.value,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  })
}

watch(T_pieData, () => {
  if (T_chartInstance) {
    T_chartInstance.setOption({
      series: [{ data: T_pieData.value }]
    });
  } else {
    T_renderChart(); 
  }
}, { immediate: true, deep: true });

const getSystemState = () => {
    axios({
        method: 'get',
        url: `${store.ip}/api/admin/getSystemStats`,
        headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
    })
        .then((response) => {
            const responseData = response.data;
            console.log('响应数据:', responseData);

            if (responseData.ret === 0) {
                if (responseData.systemStats) {
                    S_stats.value.AiChat = responseData.systemStats.S_AiChat;
                    S_stats.value.exercises = responseData.systemStats.S_exercises;
                    S_stats.value.check = responseData.systemStats.S_check;

                    T_stats.value.courseware = responseData.systemStats.T_courseware;
                    T_stats.value.exercises = responseData.systemStats.T_exercises;
                    T_stats.value.check = responseData.systemStats.T_check;

                } else {
                    S_stats.value = [];
                    T_stats.value = [];
                }
            } else {
                ElMessage({
                    message: '获取系统信息失败：' + responseData.msg,
                    type: 'error',
                });
            }
        })
        .catch((error) => {
            console.error('Error posting data:', error);
            ElMessage({
                message: '获取系统信息失败：网络错误，请稍后重试！',
                type: 'error',
                duration: 5000,
                grouping: true,
            });
        });
};


</script>

<style scoped>


</style>