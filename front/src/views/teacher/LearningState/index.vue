<template>
    <div class="main">
        <div class="toggle-buttons">
            <el-button type="primary" :plain="activeTab !== 'students'" @click="switchToStudentsView"
                class="toggle-student">
                学生视图
            </el-button>
            <el-button type="primary" :plain="activeTab !== 'courses'" @click="switchToCoursesView"
                class="toggle-course">
                课程视图
            </el-button>
        </div>

        <!-- 学生视图 -->
        <div class="main-content-student" v-show="activeTab === 'students'">
            <div class="student-left-panel">
                <div class="student-left-head">
                    <div class="student-left-head-in" v-if="selectedStudent">
                        <button class="nav-btn" @click="goBack">
                            <h3>&lt;</h3>
                        </button>
                        <h3 class="nav-title">{{ selectedStudent.name }}</h3>
                        <div></div>
                    </div>
                    <h3 v-else class="nav-title">学生列表</h3>
                </div>
                <div class="sidebar">
                    <div class="student-list">
                        <el-space direction="vertical" fill>
                            <div v-if="!selectedStudent" class="student-item"
                                :class="{ active: activeStudent === student.id }" v-for="student in students"
                                :key="student.id" @click="selectStudent(student)">
                                <span class="student-title">{{ student.name }}</span>
                            </div>
                            <div v-else class="course-item" :class="{ active: activeCourse === course.id }"
                                v-for="course in selectedStudentCourses" :key="course.id"
                                @click="selectCourseInStudent(course)">
                                <span class="course-title">{{ course.name }}</span>
                            </div>
                        </el-space>
                    </div>
                </div>
            </div>
            <div class="student-right-panel">
                <div class="student-right-content">
                    <!-- 学生整体数据 -->
                    <div v-if="selectedStudent && !selectedCourseInStudent" class="student-content">
                        <div class="student-title-right">{{ selectedStudent.name }}</div>
                        <div class="student-summary" v-if="selectedStudent.courses?.length">
                            <div class="chart-container">
                                <div class="chart-box">
                                    <div class="chart" :id="`student-summary-ai-chart-${selectedStudent.id}`"
                                        style="width: 100%; height: 300px;"></div>
                                </div>
                                <div class="chart-box">
                                    <div class="chart" :id="`student-summary-exercise-chart-${selectedStudent.id}`"
                                        style="width: 100%; height: 300px;"></div>
                                </div>
                                <div class="chart-box">
                                    <div class="chart" :id="`student-summary-correctness-chart-${selectedStudent.id}`"
                                        style="width: 100%; height: 300px;"></div>
                                </div>
                            </div>
                        </div>
                        <div v-else class="no-course">
                            无课程内容
                        </div>
                    </div>

                    <!-- 学生课程数据 -->
                    <div v-if="selectedCourseInStudent" class="course-content">
                        <div class="course-title-right">{{ selectedCourseInStudent.name }}</div>
                        <div class="chart-container">
                            <div class="chart-box">
                                <div class="chart"
                                    :id="`student-ai-chart-${selectedStudent.id}-${selectedCourseInStudent.id}`"
                                    style="width: 100%; height: 300px;"></div>
                            </div>
                            <div class="chart-box">
                                <div class="chart"
                                    :id="`student-exercise-chart-${selectedStudent.id}-${selectedCourseInStudent.id}`"
                                    style="width: 100%; height: 300px;"></div>
                            </div>
                            <div class="chart-box">
                                <div class="chart"
                                    :id="`student-correctness-chart-${selectedStudent.id}-${selectedCourseInStudent.id}`"
                                    style="width: 100%; height: 300px;"></div>
                            </div>
                        </div>
                        <div class="chapter-list">
                            <div v-for="chapter in selectedCourseInStudent.chapters" :key="chapter.id"
                                class="chapter-item">
                                <div class="chapter-title">{{ chapter.name }}</div>
                                <div class="chapter-details">
                                    <div class="detail-item">
                                        <span class="detail-label">AI使用次数：</span>
                                        <span>{{ chapter.AiFrequence || 0 }}</span>
                                    </div>
                                    <div class="detail-item">
                                        <span class="detail-label">答题次数：</span>
                                        <span>{{ chapter.sum_exercises || 0 }}</span>
                                    </div>
                                    <div class="detail-item">
                                        <span class="detail-label">正确答题次数：</span>
                                        <span>{{ chapter.right_exercises || 0 }}</span>
                                    </div>
                                    <div class="detail-item">
                                        <span class="detail-label">正确率：</span>
                                        <span>{{ calculateCorrectness(chapter) }}%</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-if="!selectedStudent && !selectedCourseInStudent" class="no-course-selected">
                        请从左侧选择学生
                    </div>
                </div>
            </div>
        </div>

        <!-- 课程视图 -->
        <div class="main-content-course" v-show="activeTab === 'courses'">
            <div class="course-left-panel">
                <div class="course-left-head">
                    <h3 class="nav-title">课程列表</h3>
                </div>
                <div class="sidebar">
                    <div class="course-list">
                        <el-space direction="vertical" fill>
                            <div class="course-item" :class="{ active: activeCourse === course.id }"
                                v-for="course in courses" :key="course.id" @click="selectCourseInCourse(course)">
                                <span class="course-title">{{ course.name }}</span>
                            </div>
                        </el-space>
                    </div>
                </div>
            </div>
            <div class="course-right-panel">
                <div class="course-right-head">
                    <h3 v-if="selectedCourseInCourse" class="nav-title">
                        {{ selectedCourseInCourse.name }}
                    </h3>
                </div>
                <div class="course-right-content">
                    <!-- 课程数据 -->
                    <div class="statistic">
                        <div v-if="selectedCourseInCourse">
                            <div class="chart-container">
                                <div class="chart-box">
                                    <div class="chart" :id="`course-ai-chart-${selectedCourseInCourse.id}`"
                                        style="width: 100%; height: 300px;"></div>
                                </div>
                                <div class="chart-box">
                                    <div class="chart" :id="`course-exercise-chart-${selectedCourseInCourse.id}`"
                                        style="width: 100%; height: 300px;"></div>
                                </div>
                                <div class="chart-box">
                                    <div class="chart" :id="`course-correctness-chart-${selectedCourseInCourse.id}`"
                                        style="width: 100%; height: 300px;"></div>
                                </div>
                            </div>
                            <div class="chapter-list">
                                <div v-for="chapter in selectedCourseInCourse.chapters" :key="chapter.id"
                                    class="chapter-item">
                                    <div class="chapter-title">{{ chapter.name }}</div>
                                    <div class="chapter-details">
                                        <div class="detail-item">
                                            <span class="detail-label">AI使用次数：</span>
                                            <span>{{ chapter.AiFrequence || 0 }}</span>
                                        </div>
                                        <div class="detail-item">
                                            <span class="detail-label">答题次数：</span>
                                            <span>{{ chapter.sum_exercises || 0 }}</span>
                                        </div>
                                        <div class="detail-item">
                                            <span class="detail-label">正确答题次数：</span>
                                            <span>{{ chapter.right_exercises || 0 }}</span>
                                        </div>
                                        <div class="detail-item">
                                            <span class="detail-label">正确率：</span>
                                            <span>{{ calculateCorrectness(chapter) }}%</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-else class="no-course-selected">
                            请从左侧选择课程
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, nextTick, watch, onUnmounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage, ElSelect, ElOption } from 'element-plus';
import * as echarts from 'echarts';
import { marked } from 'marked';

const store = mainStore();
const students = ref([]);
const courses = ref([]);
const activeTab = ref<'students' | 'courses'>('students');
const activeTab2 = ref<'statistic' | 'analysis'>('statistic');
const selectedStudent = ref<any>(null);
const selectedCourseInStudent = ref<any>(null);
const selectedCourseInCourse = ref<any>(null);
const activeStudent = ref<number | null>(null);
const activeCourse = ref<number | null>(null);
const chartInstances = new Map();
const selectedStudentCourses = computed(() => {
    return selectedStudent.value?.courses || [];
});


// 初始化
onMounted(() => {
    getStudentsList();
    getCoursesList();
    window.addEventListener('resize', resizeAllCharts);
    window.addEventListener('theme-changed', handleThemeChange);
});

onUnmounted(() => {
    window.removeEventListener('resize', resizeAllCharts);
    // 添加：移除主题变化监听
    window.removeEventListener('theme-changed', handleThemeChange);

    // 销毁所有图表实例
    chartInstances.forEach(chart => {
        chart.dispose();
    });
    chartInstances.clear();
});

const handleThemeChange = () => {
    renderAllCharts();
};

// 切换视图时重置状态
watch(activeTab, (newTab) => {
    if (newTab === 'students') {
        selectedCourseInCourse.value = null;
        activeTab2.value = 'statistic';
        // 新增：重置课程视图的active状态
        activeCourse.value = null;
    } else {
        selectedStudent.value = null;
        selectedCourseInStudent.value = null;
        // 新增：重置学生视图的active状态
        activeStudent.value = null;
        activeCourse.value = null;
    }

    nextTick(() => {
        renderAllCharts();
        setTimeout(resizeAllCharts, 100);
    });
});

// 监听数据变化渲染图表
watch([students, courses, selectedStudent, selectedCourseInStudent, selectedCourseInCourse], () => {
    nextTick(() => {
        renderAllCharts();
        setTimeout(resizeAllCharts, 100);
    });
}, { deep: true });


// 视图切换方法
const switchToStudentsView = () => {
    activeTab.value = 'students';
    activeCourse.value = null;
};

const switchToCoursesView = () => {
    activeTab.value = 'courses';
    activeStudent.value = null;
    activeCourse.value = null;
};

// 学生视图方法
const selectStudent = (student: any) => {
    selectedStudent.value = student;
    selectedCourseInStudent.value = null;
    activeStudent.value = student.id;
};

const selectCourseInStudent = (course: any) => {
    selectedCourseInStudent.value = course;
    activeCourse.value = course.id;
};

const goBack = () => {
    selectedStudent.value = null;
    selectedCourseInStudent.value = null;
    activeStudent.value = null;
    activeCourse.value = null;
};

// 课程视图方法
const selectCourseInCourse = (course: any) => {
    selectedCourseInCourse.value = course;
    activeCourse.value = course.id;
};

// 辅助方法
const calculateCorrectness = (chapter: any) => {
    if (!chapter.sum_exercises || chapter.sum_exercises === 0) return 0;
    return Math.round((chapter.right_exercises / chapter.sum_exercises) * 100);
};

const getCssVar = (name: string) =>
    getComputedStyle(document.documentElement).getPropertyValue(name).trim();

// 图表相关方法
const renderAllCharts = () => {
    // 清理所有图表实例
    chartInstances.forEach((chart) => {
        chart.dispose();
    });
    chartInstances.clear();
    // 学生整体数据图表
    if (selectedStudent.value && !selectedCourseInStudent.value) {
        renderStudentSummaryCharts(selectedStudent.value);
    }

    // 学生课程数据图表
    if (selectedCourseInStudent.value) {
        renderCourseCharts(
            `student-ai-chart-${selectedStudent.value.id}-${selectedCourseInStudent.value.id}`,
            `student-exercise-chart-${selectedStudent.value.id}-${selectedCourseInStudent.value.id}`,
            `student-correctness-chart-${selectedStudent.value.id}-${selectedCourseInStudent.value.id}`,
            selectedCourseInStudent.value.chapters
        );
    }

    // 课程视图数据图表
    if (selectedCourseInCourse.value && activeTab2.value === 'statistic') {
        renderCourseCharts(
            `course-ai-chart-${selectedCourseInCourse.value.id}`,
            `course-exercise-chart-${selectedCourseInCourse.value.id}`,
            `course-correctness-chart-${selectedCourseInCourse.value.id}`,
            selectedCourseInCourse.value.chapters
        );
    }
};

const renderStudentSummaryCharts = (student: any) => {
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

    if (courseSummary && courseSummary.length > 0) {
        renderSummaryAIChart(
            `student-summary-ai-chart-${student.id}`,
            courseSummary,
            'AI使用总次数'
        );
        renderSummaryExerciseChart(
            `student-summary-exercise-chart-${student.id}`,
            courseSummary,
            '答题总次数'
        );
        renderSummaryCorrectnessChart(
            `student-summary-correctness-chart-${student.id}`,
            courseSummary
        );
    }
};

const renderCourseCharts = (aiChartId: string, exerciseChartId: string, correctnessChartId: string, chapters: any[]) => {
    renderAIChart(aiChartId, chapters, 'AI使用次数');
    renderExerciseChart(exerciseChartId, chapters, '答题次数');
    renderCorrectnessChart(correctnessChartId, chapters);
};

// 图表渲染函数（从第一个文件复制，保持相同）
const renderAIChart = (chartId: string, chapters: any[], title: string) => {
    const chartDom = document.getElementById(chartId);
    if (!chartDom) return;

    const chart = echarts.init(chartDom);
    const titleColor = getCssVar('--titleColor');
    const textColor = getCssVar('--textColor');
    chartInstances.set(chartId, chart);

    const option = {
        title: {
            text: title,
            left: 'center',
            textStyle: {
                color: textColor,  // 标题颜色
                fontWeight: 'bold',
                fontSize: 16
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            formatter: function (name) {
                return name.length > 6 ? name.slice(0, 6) + '...' : name;
            },
            textStyle: {
                color: textColor  // 图例文字颜色
            },
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
                    position: 'center',
                    color: textColor
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '18',
                        fontWeight: 'bold',
                        color: textColor
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
};

const renderExerciseChart = (chartId: string, chapters: any[], title: string) => {
    const chartDom = document.getElementById(chartId);
    if (!chartDom) return;

    const chart = echarts.init(chartDom);
    const titleColor = getCssVar('--titleColor');
    const textColor = getCssVar('--textColor');
    chartInstances.set(chartId, chart);

    const option = {
        title: {
            text: title,
            left: 'center',
            textStyle: {
                color: textColor,  // 标题颜色
                fontWeight: 'bold',
                fontSize: 16
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            formatter: function (name) {
                return name.length > 6 ? name.slice(0, 6) + '...' : name;
            },
            textStyle: {
                color: textColor  // 图例文字颜色
            },
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
                    position: 'center',
                    color: textColor
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '18',
                        fontWeight: 'bold',
                        color: textColor
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
    const titleColor = getCssVar('--titleColor');
    const textColor = getCssVar('--textColor');
    chartInstances.set(chartId, chart);

    const option = {
        title: {
            text: '答题准确率',
            left: 'center',
            textStyle: {
                color: textColor,  // 标题颜色
                fontWeight: 'bold',
                fontSize: 16
            }
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
                rotate: 0,  // 竖排
                formatter: (value: string) => value.length > 6 ? value.slice(0, 6) + '…' : value
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
                data: chapters.map(c => {
                    const correctness = c.correctness * 100; // 乘以100转换为百分比
                    return Math.round(correctness * 100) / 100; // 保留两位小数
                }),
                itemStyle: {
                    color: function (params) {
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

const renderSummaryAIChart = (chartId: string, courseSummary: any[], title: string) => {
    const chartDom = document.getElementById(chartId);
    if (!chartDom || !courseSummary) return;

    const chart = echarts.init(chartDom);
    const titleColor = getCssVar('--titleColor');
    const textColor = getCssVar('--textColor');
    chartInstances.set(chartId, chart);

    const option = {
        title: {
            text: title,
            left: 'center',
            textStyle: {
                color: textColor,  // 标题颜色
                fontWeight: 'bold',
                fontSize: 16
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            formatter: function (name) {
                return name.length > 6 ? name.slice(0, 6) + '...' : name;
            },
            textStyle: {
                color: textColor  // 图例文字颜色
            },
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
                    position: 'center',
                    color: textColor
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '18',
                        fontWeight: 'bold',
                        color: textColor
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
    const titleColor = getCssVar('--titleColor');
    const textColor = getCssVar('--textColor');
    chartInstances.set(chartId, chart);

    const option = {
        title: {
            text: title,
            left: 'center',
            textStyle: {
                color: textColor,  // 标题颜色
                fontWeight: 'bold',
                fontSize: 16
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            formatter: function (name) {
                return name.length > 6 ? name.slice(0, 6) + '...' : name;
            },
            textStyle: {
                color: textColor  // 图例文字颜色
            },
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
                    position: 'center',
                    color: textColor
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '18',
                        fontWeight: 'bold',
                        color: textColor
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
    const titleColor = getCssVar('--titleColor');
    const textColor = getCssVar('--textColor');
    chartInstances.set(chartId, chart);

    const option = {
        title: {
            text: '课程平均正确率',
            left: 'center',
            textStyle: {
                color: textColor,  // 标题颜色
                fontWeight: 'bold',
                fontSize: 16
            }
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
                rotate: 0,  // 竖排
                formatter: (value: string) => value.length > 6 ? value.slice(0, 6) + '…' : value
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
                    color: function (params) {
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
    axios.post(`${store.ip}/api/teacher/getLearningStatsByPerson`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
        }
    }).then(res => {
        const data = res.data;

        if (data.ret === 0) {
            if (Array.isArray(data.students)) {
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
    axios.post(`${store.ip}/api/teacher/getLearningStatsByCourse`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
        }
    }).then(res => {
        const data = res.data;

        if (data.ret === 0) {
            if (Array.isArray(data.courses)) {
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
.main {
    padding: 20px;
    font-family: Arial, Helvetica, sans-serif;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.toggle-buttons {
    margin-bottom: 10px;
    display: flex;
    gap: 10px;
}

.el-button--primary.is-plain {
    border-radius: 8px;
    font-weight: 500;
    padding: 12px 20px;
    transition: all 0.3s ease;
    border: 1.5px solid transparent;
    background-color: var(--backgroundColor2);
    color: var(--textColor2);
}

.el-button--primary {
    border-radius: 8px;
    font-weight: 500;
    padding: 12px 20px;
    transition: all 0.3s ease;
    background: #417dff;
    border-color: #409eff;
    color: white;
    box-shadow: 0 2px 8px rgba(64, 158, 255, 0.4);
}

.el-button--primary.is-plain:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px var(--shadowColor2);
    color: var(--textColor);
    border: 1.5px solid var(--textColor);
}

/* 学生视图布局 */
.main-content-student {
    display: flex;
    flex: 1;
    background: transparent;
    border-radius: 8px;
    overflow: hidden;
}

.student-left-panel {
    width: 300px;
    background: var(--backgroundColor2);
    border-right: 1.5px solid transparent;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    margin-top: 5px;
}

.student-left-head {
    padding: 15px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
}

.student-left-head-in {
    display: flex;
    flex: 1;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}

.nav-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 18px;
    margin-right: 10px;
    color: var(--titleColor);
}

.nav-btn:hover {
    color: #00a2ff;
}

.nav-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--titleColor);
    margin-left: auto;
    margin-right: auto;
}

.sidebar {
    flex: 1;
    overflow-y: auto;
}

.student-list,
.course-list {
    width: 100%;
    flex: 1;
    overflow-y: auto;
    padding-bottom: 20px;
    padding-left: 5px;
    padding-right: 5px;
}

.student-item,
.course-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid transparent;
    border-radius: 5px;
    background-color: transparent;
    color: var(--textColor2);
    width: 270px;
}

.student-item:hover,
.course-item:hover {
    background-color: var(--backgroundColor2);
    color: var(--titleColor);
}

.student-item.active,
.course-item.active {
    color: var(--titleColor);
    background-color: var(--backgroundColor2);
    font-weight: 540;
}

.student-title,
.course-title {
    font-size: 14px;
    line-height: 1.4;
    flex: 1;
    font-weight: bold;
}

.student-title-right,
.course-title-right {
    font-size: 18px;
    line-height: 1.4;
    flex: 1;
    font-weight: bold;
    padding: 1rem;


}

.student-right-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: transparent;
}

.student-right-head {
    padding: 15px 20px;
    background: transparent;
}

.student-right-content {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    padding-top: 0;
}

.chapter-select {
    width: 300px;
    margin-right: 1rem;
}

/* 课程视图布局 */
.main-content-course {
    display: flex;
    flex: 1;
    background: transparent;
    border-radius: 8px;
    overflow: hidden;
}

.course-left-panel {
    width: 300px;
    background: var(--backgroundColor2);
    border-right: 1.5px solid transparent;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    margin-top: 5px;
}

.course-left-head {
    padding: 15px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
}

.course-right-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: transparent;
}

.course-right-head {
    padding: 15px 20px;
    background: transparent;
    display: flex;
    justify-content: center;
    align-items: center;
}

.function-button {
    display: flex;
    gap: 10px;
}

.course-right-content {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
}

/* 通用样式 */
.chart-container {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    justify-content: space-between;
    margin-bottom: 30px;
}

.chart-box {
    flex: 1;
    min-width: 30%;
    max-width: 32%;
    background: var(--backgroundColor2);
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 1px 3px var(--shadowColor2);
}

.chapter-list {
    margin-top: 20px;
}

.chapter-item {
    margin-bottom: 15px;
    border: 1px solid var(--titleColor);
    border-radius: 8px;
    overflow: hidden;
}

.chapter-title {
    padding: 12px 15px;
    background: var(--backgroundColor2);
    font-weight: 500;
    font-size: 15px;
}

.chapter-details {
    padding: 15px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
}

.detail-item {
    display: flex;
}

.detail-label {
    font-weight: 500;
    min-width: 120px;
    color: var(--textColor2);
}

.no-course,
.no-analysis,
.no-course-selected {
    padding: 20px;
    text-align: center;
    color: var(--textColor2);
    font-style: italic;
    background-color: transparent;
    border-radius: 8px;
    margin-top: 3rem;
}

/* AI分析区域 */
.analysis-content {
    margin-top: 20px;
    border-radius: 8px;
    overflow: hidden;
    background-color: var(--backgroundColor3);
}

.read-only-content {
    padding: 20px;
    background-color: var(--backgroundColor3);
    min-height: 300px;
    max-height: 500px;
    text-align: left;
}

.generate-button {
    display: flex;
    justify-content: center;
}


.analysis-head {
    display: flex;
    flex-direction: row;
    flex: 1;
}

/* 响应式设计 */
@media (max-width: 1200px) {
    .chart-box {
        min-width: 48%;
        max-width: 49%;
    }
}

@media (max-width: 992px) {

    .main-content-student,
    .main-content-course {
        flex-direction: column;
    }

    .student-left-panel,
    .course-left-panel {
        width: 100%;
        border-right: none;
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

    .chapter-details {
        grid-template-columns: 1fr;
    }
}
</style>