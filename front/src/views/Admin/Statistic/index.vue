<template>
    <div class="dashboard-container">
        <div class="charts-row">
            <div class="chart-card">
                <div ref="S_chartRef" class="chart"></div>
            </div>
            <div class="chart-card">
                <div ref="T_chartRef" class="chart"></div>
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="el-icon-user-solid"></i>
                </div>
                <div class="stat-content">
                    <h3>用户总数</h3>
                    <p>{{ user_num }}</p>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon" style="background-color: #f56c6c;">
                    <i class="el-icon-male"></i>
                </div>
                <div class="stat-content">
                    <h3>男性用户</h3>
                    <p>{{ male_num }}</p>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon" style="background-color: #e6a23c;">
                    <i class="el-icon-female"></i>
                </div>
                <div class="stat-content">
                    <h3>女性用户</h3>
                    <p>{{ female_num }}</p>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon" style="background-color: #67c23a;">
                    <i class="el-icon-notebook-2"></i>
                </div>
                <div class="stat-content">
                    <h3>课程数量</h3>
                    <p>{{ course_num }}</p>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon" style="background-color: #409eff;">
                    <i class="el-icon-collection"></i>
                </div>
                <div class="stat-content">
                    <h3>章节数量</h3>
                    <p>{{ chapter_num }}</p>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon" style="background-color: #909399;">
                    <i class="el-icon-document"></i>
                </div>
                <div class="stat-content">
                    <h3>习题总数</h3>
                    <p>{{ exercise_num }}</p>
                </div>
            </div>
        </div>
        
        <div class="gender-chart-container">
            <div ref="genderChartRef" class="chart"></div>
        </div>
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
const exercise_num = ref(0);
const user_num = ref(0);
const course_num = ref(0);
const female_num = ref(0);
const male_num = ref(0);
const chapter_num = ref(0);

const S_chartRef = ref<HTMLElement | null>(null)
const T_chartRef = ref<HTMLElement | null>(null)
const genderChartRef = ref<HTMLElement | null>(null)
let S_chartInstance: echarts.ECharts | null = null
let T_chartInstance: echarts.ECharts | null = null
let genderChartInstance: echarts.ECharts | null = null

onMounted(() => {
    getSystemState();
    initCharts();
});

onBeforeUnmount(() => {
  S_chartInstance?.dispose();
  T_chartInstance?.dispose();
  genderChartInstance?.dispose();
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

const genderData = computed(() => [
  { value: male_num.value, name: '男性' },
  { value: female_num.value, name: '女性' },
]);

const initCharts = () => {
  initSChart();
  initTChart();
  initGenderChart();
}

const initSChart = () => {
  if (!S_chartRef.value) return

  S_chartInstance = echarts.init(S_chartRef.value)
  S_chartInstance.setOption({
    title: {
      text: '学生模块使用情况',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: ['AI聊天板块', '生成习题版块', '批改习题版块']
    },
    series: [
      {
        name: '使用频率',
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: S_pieData.value
      }
    ],
    color: ['#409EFF', '#67C23A', '#E6A23C']
  })
}

const initTChart = () => {
  if (!T_chartRef.value) return

  T_chartInstance = echarts.init(T_chartRef.value)
  T_chartInstance.setOption({
    title: {
      text: '教师模块使用情况',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: ['生成课件版块', '生成习题版块', '批改习题版块']
    },
    series: [
      {
        name: '使用频率',
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: T_pieData.value
      }
    ],
    color: ['#F56C6C', '#67C23A', '#E6A23C']
  })
}

const initGenderChart = () => {
  if (!genderChartRef.value) return

  genderChartInstance = echarts.init(genderChartRef.value)
  genderChartInstance.setOption({
    title: {
      text: '用户性别比例',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'horizontal',
      bottom: 10,
      data: ['男性', '女性']
    },
    series: [
      {
        name: '性别比例',
        type: 'pie',
        radius: '60%',
        center: ['50%', '50%'],
        data: genderData.value,
        itemStyle: {
          emphasis: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        label: {
          show: true,
          formatter: '{b}: {c} ({d}%)'
        },
        labelLine: {
          show: true
        }
      }
    ],
    color: ['#409EFF', '#F56C6C']
  })
}

watch(S_pieData, () => {
  if (S_chartInstance) {
    S_chartInstance.setOption({
      series: [{ data: S_pieData.value }]
    });
  }
}, { deep: true });

watch(T_pieData, () => {
  if (T_chartInstance) {
    T_chartInstance.setOption({
      series: [{ data: T_pieData.value }]
    });
  }
}, { deep: true });

watch(genderData, () => {
  if (genderChartInstance) {
    genderChartInstance.setOption({
      series: [{ data: genderData.value }]
    });
  }
}, { deep: true });

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
                    exercise_num.value = responseData.systemStats.exercise_num;
                    user_num.value = responseData.systemStats.user_num;
                    male_num.value = responseData.systemStats.male_num;
                    female_num.value = responseData.systemStats.female_num;
                    course_num.value = responseData.systemStats.course_num;
                    chapter_num.value = responseData.systemStats.chapter_num;

                } else {
                    S_stats.value = [];
                    T_stats.value = [];
                    exercise_num.value = 0;
                    user_num.value = 0;
                    male_num.value = 0;
                    female_num.value = 0;
                    course_num.value = 0;
                    chapter_num.value = 0;
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
.dashboard-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

.charts-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    gap: 20px;
}

.chart-card {
    flex: 1;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 15px;
}

.chart {
    width: 100%;
    height: 350px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 20px;
}

.stat-card {
    display: flex;
    align-items: center;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 20px;
}

.stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: #409EFF;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 20px;
    color: white;
    font-size: 24px;
}

.stat-content h3 {
    margin: 0;
    font-size: 16px;
    color: #909399;
    font-weight: normal;
}

.stat-content p {
    margin: 10px 0 0;
    font-size: 24px;
    font-weight: bold;
    color: #303133;
}

.gender-chart-container {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 15px;
}

@media (max-width: 992px) {
    .charts-row {
        flex-direction: column;
    }
    
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }
}
</style>