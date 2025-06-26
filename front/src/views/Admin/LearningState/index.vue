<template>
  <div class="main-container">
    <div class="toggle-buttons">
      <el-button 
        type="primary" 
        :plain="activeTab !== 'students'"
        @click="activeTab = 'students'"
      >
        学生视图
      </el-button>
      <el-button 
        type="primary" 
        :plain="activeTab !== 'courses'"
        @click="activeTab = 'courses'"
      >
        课程视图
      </el-button>
    </div>

    <div class="main-content">
      <div class="student-list" v-show="activeTab === 'students'">
        <el-collapse v-model="activeStudentNames" accordion>
          <el-collapse-item 
            v-for="student in students" 
            :key="student.id" 
            :name="student.id"
          >
            <template #title>
              <div class="student-title">姓名：{{ student.name }}</div>
            </template>
          <div class="student-summary">
            <div class="summary-title">课程汇总数据</div>
            <div class="chart-container">
              <div class="chart-box">
                <div class="chart-title">各课程AI使用总次数</div>
                <div 
                  class="chart" 
                  :id="`student-summary-ai-chart-${student.id}`"
                  style="width: 100%; height: 300px;"
                ></div>
              </div>
              <div class="chart-box">
                <div class="chart-title">各课程答题总次数</div>
                <div 
                  class="chart" 
                  :id="`student-summary-exercise-chart-${student.id}`"
                  style="width: 100%; height: 300px;"
                ></div>
              </div>
              <div class="chart-box">
                <div class="chart-title">各课程平均正确率</div>
                <div 
                  class="chart" 
                  :id="`student-summary-correctness-chart-${student.id}`"
                  style="width: 100%; height: 300px;"
                ></div>
              </div>
            </div>
          </div>
            
            <el-collapse v-model="activeStudentCourses[student.id]">
              <el-collapse-item 
                v-for="course in student.courses" 
                :key="course.id" 
                :name="course.id"
              >
                <template #title>
                  <div class="course-title">{{ course.name }}</div>
                </template>
                
                <div class="chart-container">
                  <div class="chart-box">
                    <div class="chart-title">各章节AI使用次数分布</div>
                    <div 
                      class="chart" 
                      :id="`student-ai-chart-${student.id}-${course.id}`"
                      style="width: 100%; height: 300px;"
                    ></div>
                  </div>
                  <div class="chart-box">
                    <div class="chart-title">各章节答题次数分布</div>
                    <div 
                      class="chart" 
                      :id="`student-exercise-chart-${student.id}-${course.id}`"
                      style="width: 100%; height: 300px;"
                    ></div>
                  </div>
                  <div class="chart-box">
                    <div class="chart-title">各章节答题准确率</div>
                    <div 
                      class="chart" 
                      :id="`student-correctness-chart-${student.id}-${course.id}`"
                      style="width: 100%; height: 300px;"
                    ></div>
                  </div>
                </div>
              </el-collapse-item>
            </el-collapse>
          </el-collapse-item>
        </el-collapse>
      </div>

      <div class="course-list" v-show="activeTab === 'courses'">
        <el-collapse v-model="activeCourseNames" accordion >
          <el-collapse-item 
            v-for="course in courses" 
            :key="course.id" 
            :name="course.id"
          >
            <template #title>
              <div class="course-title">{{ course.name }}</div>
            </template>
            
            <div class="chart-container">
              <div class="chart-box">
                <div class="chart-title">各章节AI使用次数分布</div>
                <div 
                  class="chart" 
                  :id="`course-ai-chart-${course.id}`"
                  style="width: 100%; height: 300px;"
                ></div>
              </div>
                  <div class="chart-box">
                    <div class="chart-title">各章节答题次数分布</div>
                    <div 
                      class="chart" 
                      :id="`course-exercise-chart-${course.id}`"
                      style="width: 100%; height: 300px;"
                    ></div>
                  </div>
              <div class="chart-box">
                <div class="chart-title">各章节答题准确率</div>
                <div 
                  class="chart" 
                  :id="`course-correctness-chart-${course.id}`"
                  style="width: 100%; height: 300px;"
                ></div>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>
  </div>
</template>



<script lang="ts" setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import * as echarts from 'echarts'
const store = mainStore();
const students = ref([]);
const courses = ref([]);
const activeTab = ref<'students' | 'courses'>('students');
const activeStudentNames = ref([]);
const activeStudentCourses = ref({});
const activeCourseNames = ref([]);
const chartInstances = new Map();

onMounted(() => {
    getStudentsList();
    getCoursesList();
    window.addEventListener('resize', () => {
      chartInstances.forEach(chart => chart.resize());
    });
});

watch([students, courses], () => {
  nextTick(() => {
    renderAllCharts();
  });
}, { deep: true });

watch([activeStudentNames, activeStudentCourses, activeCourseNames], () => {
  nextTick(() => {
    renderAllCharts();
  });
}, { deep: true });

watch(activeTab, (newVal) => {
  nextTick(() => {
    renderAllCharts();
  });
});

watch(activeTab, () => {
  nextTick(() => {
    renderAllCharts();  // 确保重新渲染或补充图表
    setTimeout(resizeAllCharts, 100); // 延迟触发 resize，等待 DOM 显示完毕
  });
});

const renderAllCharts = () => {
  // Clear all existing charts first
  chartInstances.forEach((chart) => {
    chart.dispose();
  });
  chartInstances.clear();

  // Render student charts
  students.value.forEach(student => {
    student.courses?.forEach(course => {
      renderStudentSummaryCharts(student);
      if (activeStudentCourses.value[student.id]?.includes(course.id)) {
        renderAIChart(
          `student-ai-chart-${student.id}-${course.id}`,
          course.chapters,
          'AI使用次数'
        );
        renderExerciseChart(
          `student-exercise-chart-${student.id}-${course.id}`,
          course.chapters,
          '答题次数'
        );
        renderCorrectnessChart(
          `student-correctness-chart-${student.id}-${course.id}`,
          course.chapters
        );
      }
    });
  });

  // Render course charts
  courses.value.forEach(course => {
    if (activeCourseNames.value === course.id) {
      renderAIChart(
        `course-ai-chart-${course.id}`,
        course.chapters,
        'AI使用次数'
      );
      renderExerciseChart(
        `course-exercise-chart-${course.id}`,
        course.chapters,
        '答题次数'
      );
      renderCorrectnessChart(
        `course-correctness-chart-${course.id}`,
        course.chapters
      );
    }
  });
};
const renderAIChart = (chartId: string, chapters: any[], title: string) => {
  const chartDom = document.getElementById(chartId);
  if (!chartDom) return;

  const chart = echarts.init(chartDom);
  chartInstances.set(chartId, chart);

  const option = {
    title: {
      text: title,
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: chapters.map(c => c.name)
    },
    series: [
      {
        name: title,
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
        data: chapters.map(c => ({
          value: c.AiFrequence,
          name: c.name
        }))
      }
    ]
  };

  chart.setOption(option);
  window.addEventListener('resize', () => chart.resize());
};

const renderExerciseChart = (chartId: string, chapters: any[], title: string) => {
  const chartDom = document.getElementById(chartId);
  if (!chartDom) return;

  const chart = echarts.init(chartDom);
  chartInstances.set(chartId, chart);

  const option = {
    title: {
      text: title,
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: chapters.map(c => c.name)
    },
    series: [
      {
        name: title,
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
        data: chapters.map(c => ({
          value: c.sum_exercises,
          name: c.name
        }))
      }
    ]
  };

  chart.setOption(option);
  window.addEventListener('resize', () => chart.resize());
};

const renderCorrectnessChart = (chartId: string, chapters: any[]) => {
  const chartDom = document.getElementById(chartId);
  if (!chartDom) return;

  const chart = echarts.init(chartDom);
  chartInstances.set(chartId, chart);

  const option = {
    title: {
      text: '答题准确率',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: chapters.map(c => c.name),
      axisLabel: {
        interval: 0,
        rotate: 30
      }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100,
      axisLabel: {
        formatter: '{value}%'
      }
    },
    series: [
      {
        name: '答题准确率',
        type: 'bar',
        data: chapters.map(c => c.correctness),
        itemStyle: {
          color: function(params) {
            // Color based on value - red for low, yellow for medium, green for high
            const value = params.data;
            if (value < 50) {
              return '#ff6384';
            } else if (value < 80) {
              return '#ffcd56';
            } else {
              return '#4bc0c0';
            }
          }
        },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}%'
        }
      }
    ]
  };

  chart.setOption(option);
  window.addEventListener('resize', () => chart.resize());
};

const resizeAllCharts = () => {
  chartInstances.forEach((chart) => {
    chart.resize();
  });
};

const renderStudentSummaryCharts = (student: any) => {
  // 计算各课程汇总数据
  const courseSummary = student.courses?.map(course => {
    const totalExercises = course.chapters?.reduce((sum, chapter) => sum + (chapter.sum_exercises || 0), 0) || 0;
    const totalCorrect = course.chapters?.reduce((sum, chapter) => sum + (chapter.right_exercises || 0), 0) || 0;
    const avgCorrectness = totalExercises > 0 ? (totalCorrect / totalExercises * 100) : 0;
    
    return {
      name: course.name,
      totalAi: course.chapters?.reduce((sum, chapter) => sum + (chapter.AiFrequence || 0), 0) || 0,
      totalExercises,
      avgCorrectness
    };
  });

  // 渲染AI使用总次数饼图
  renderSummaryAIChart(
    `student-summary-ai-chart-${student.id}`,
    courseSummary,
    'AI使用总次数'
  );

  // 渲染答题总次数饼图
  renderSummaryExerciseChart(
    `student-summary-exercise-chart-${student.id}`,
    courseSummary,
    '答题总次数'
  );

  // 渲染平均正确率柱状图
  renderSummaryCorrectnessChart(
    `student-summary-correctness-chart-${student.id}`,
    courseSummary
  );
};
const renderSummaryAIChart = (chartId: string, courseSummary: any[], title: string) => {
  const chartDom = document.getElementById(chartId);
  if (!chartDom || !courseSummary) return;

  const chart = echarts.init(chartDom);
  chartInstances.set(chartId, chart);

  const option = {
    title: {
      text: title,
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: courseSummary.map(c => c.name)
    },
    series: [
      {
        name: title,
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
        data: courseSummary.map(c => ({
          value: c.totalAi,
          name: c.name
        }))
      }
    ]
  };

  chart.setOption(option);
  window.addEventListener('resize', () => chart.resize());
};
const renderSummaryExerciseChart = (chartId: string, courseSummary: any[], title: string) => {
  const chartDom = document.getElementById(chartId);
  if (!chartDom || !courseSummary) return;

  const chart = echarts.init(chartDom);
  chartInstances.set(chartId, chart);

  const option = {
    title: {
      text: title,
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: courseSummary.map(c => c.name)
    },
    series: [
      {
        name: title,
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
        data: courseSummary.map(c => ({
          value: c.totalExercises,
          name: c.name
        }))
      }
    ]
  };

  chart.setOption(option);
  window.addEventListener('resize', () => chart.resize());
};

const renderSummaryCorrectnessChart = (chartId: string, courseSummary: any[]) => {
  const chartDom = document.getElementById(chartId);
  if (!chartDom || !courseSummary) return;

  const chart = echarts.init(chartDom);
  chartInstances.set(chartId, chart);

  const option = {
    title: {
      text: '课程平均正确率',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: courseSummary.map(c => c.name),
      axisLabel: {
        interval: 0,
        rotate: 30
      }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100,
      axisLabel: {
        formatter: '{value}%'
      }
    },
    series: [
      {
        name: '平均正确率',
        type: 'bar',
        data: courseSummary.map(c => c.avgCorrectness),
        itemStyle: {
          color: function(params) {
            const value = params.data;
            if (value < 50) return '#ff6384';
            else if (value < 80) return '#ffcd56';
            else return '#4bc0c0';
          }
        },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}%'
        }
      }
    ]
  };

  chart.setOption(option);
  window.addEventListener('resize', () => chart.resize());
};

const getStudentsList = () => {
  const formData = new FormData();
  axios.post(`${store.ip}/api/getLearningStatsByPerson`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    const data = res.data;

    if (data.ret === 0) {
      if (Array.isArray(data.students)){
        students.value = data.students;
      }
      else {
        students.value = []; 
      }
    } else {    
      ElMessage.error('获取学习情况(按学生)失败：' + data.msg);
    }
  }).catch(() => {
    ElMessage.error('获取学习情况(按学生)失败：网络错误');
  });
};

const getCoursesList = () => {
  const formData = new FormData();
  axios.post(`${store.ip}/api/getLearningStatsByCourse`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    const data = res.data;

    if (data.ret === 0) {
      if (Array.isArray(data.courses)){
        courses.value = data.courses;
      }
      else {
        courses.value = []; 
      }
    } else {   
      ElMessage.error('获取学习情况(按课程)失败：' + data.msg);
    }
  }).catch(() => {
    ElMessage.error('获取学习情况(按课程)失败：网络错误');
  });
};

</script>

<style scoped>
.main-container {
  padding: 20px;
  font-family: Arial, Helvetica, sans-serif;
}

.toggle-buttons {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.main-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.student-title,
.course-title {
  font-weight: bold;
  font-size: 16px;
}

.chart-title {
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
  font-size: 15px;
}

.el-collapse {
  border: none;
}

.el-collapse-item {
  margin-bottom: 10px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #ebeef5;
}

.el-collapse-item__header {
  padding: 0 20px;
  height: 48px;
  font-weight: 500;
  background-color: #f5f7fa;
}

.el-collapse-item__content {
  padding: 20px;
}

.chart-container {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  justify-content: space-between;
}

.chart-box {
  flex: 1;
  min-width: 30%; /* 三个图表并排 */
  max-width: 32%; /* 留一点间隙 */
  background: #fff;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.student-summary {
  padding: 15px;
  margin-bottom: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.summary-title {
  font-weight: bold;
  margin-bottom: 15px;
  font-size: 15px;
  color: #409EFF;
}


@media (max-width: 1200px) {
  .chart-box {
    min-width: 48%; /* 中等屏幕下两列布局 */
    max-width: 49%;
  }
}

@media (max-width: 768px) {
  .chart-container {
    flex-direction: column;
  }
  
  .chart-box {
    min-width: 100%;
    max-width: 100%;
  }
}

</style>