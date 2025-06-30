<template>
  <div class="main">
    <div class="left-panel">
      <div class="chapter-navigation">
        <div class="chapter-head">
        <h3 class="nav-title">课程章节</h3>
        </div>
        <div class="sidebar">
          <div class="chapter-list">
            <el-space direction="vertical" fill>
              <div class="chapter-item" :class="{ active: activeChapter === chapter.id }" v-for="chapter in chapters" :key="chapter.id" @click="handleChapterClick(chapter)" >
                <span class="chapter-title">{{ chapter.name }}</span>
              </div>
            </el-space>
          </div>
        </div>  
      </div>
    </div>
    <div class="right-panel">
      <div class="right-head">
      <h2 class="course-name">题目列表</h2>
      </div>
      <div class="head-btn">
      <el-button type="primary" @click="dialogVisible = true" class="function-btn">生成习题</el-button>
      </div>
    <div class="content-area">
    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="5" animated />
    </div>
    <div v-else-if="exercises.length === 0" class="empty-state">
      <el-empty description="暂无习题"></el-empty>
    </div>
    <div v-else class="exercise-list">
      <div class="exercise-item" v-for="item in exercises" :key="item.id" @click="handleExerciseClick(item)">
        <div class="exercise-content">{{ formatExerciseContent(item.content, 80) }}</div>
        <div class="exercise-meta">
        <span class="exercise-difficulty">难度: {{ item.difficulty }}</span>
        <span class="exercise-type">{{ getTypeLabel(item.type) }}</span>
        <el-button @click="deleteExercise(item)" class="deleteBtn">删除</el-button>
        </div>
      </div>
    </div>
    <el-dialog v-model="dialogVisible" title="生成习题" width="30%">
      <h2 class="input-title">请选择难度等级</h2>
      <el-select v-model="difficulty" placeholder="难度等级" style="width: 115px" size="large">
        <el-option label="等级1" value="1" />
        <el-option label="等级2" value="2" />
        <el-option label="等级3" value="3" />
        <el-option label="等级4" value="4" />
      </el-select>
      <h2 class="input-title">请选择题目类型</h2>
      <el-select v-model="type" placeholder="题目类型" style="width: 115px" size="large">
        <el-option label="选择题" value="choices" />
        <el-option label="填空题" value="blanks" />
        <el-option label="简答题" value="answers" />
      </el-select>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createExercise">生成</el-button>
      </template>
    </el-dialog>
  </div>
  </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue';
import { mainStore } from '../../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import T_exercise from '../Exercise/index.vue'
import { marked } from 'marked';
const courseId = ref('');
const courseName = ref('');
const store = mainStore();
const router = useRouter();
const chapters = ref([]);
const chapter = ref<Record<string, any>>({});
const exercises = ref([]);
const difficulty = ref('');
const type = ref('');
const selectedExercise = ref<any>(null);
const dialogVisible = ref(false);
const activeChapter = ref<number | null>(null);
interface Chapter {
  id: number;
  name: string;
  content: string;
}
const typeMap: Record<string, string> = {
  choices: '选择题',
  blanks: '填空题',
  answers: '简答题'
};

const getTypeLabel = (type: string): string => {
  return typeMap[type] || '未知题型';
};

const getExercisesList = () => {
  const formData = new FormData();
  formData.append('id', chapter.value.id);

  axios.post(`${store.ip}/api/teacher/getExercisesList`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    const data = res.data;

    if (data.ret === 0 && Array.isArray(data.exercisesList)) {
      exercises.value = data.exercisesList;
    } else {
      exercises.value = []; 
      ElMessage.error('获取习题列表失败：' + data.msg);
    }
  }).catch(() => {
    ElMessage.error('获取习题列表失败：网络错误');
  });
};

const getChapterList = () => {
  const formData = new FormData();
  formData.append('id', courseId.value);
  axios({
    method: 'post',
    url: `${store.ip}/api/getChapterList`,
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
    .then((response) => {
      const responseData = response.data;
      console.log('响应数据:', responseData);

      if (responseData.ret === 0) {
        chapters.value = Array.isArray(responseData.chapterList) ? responseData.chapterList : [responseData.chapterList];
      } else {
        chapters.value = [];
        ElMessage({
          message: '获取章节列表失败：' + responseData.msg,
          type: 'error',
        });
      }
    })
    .catch((error) => {
      console.error('Error posting data:', error);
      ElMessage({
        message: '获取章节列表失败：网络错误，请稍后重试！',
        type: 'error',
        duration: 5000,
        grouping: true,
      });
    });
};

const handleExerciseClick = (item: any) => {
  selectedExercise.value = item;
  localStorage.setItem('selectedExercise', JSON.stringify(selectedExercise.value));
  store.addTab('习题', T_exercise);
}

const createExercise = () => {
  const formData = new FormData();
  formData.append('ChapterNo', chapter.value.id);
  formData.append('difficulty', difficulty.value);
  formData.append('type', type.value);

  axios.post(`${store.ip}/api/teacher/generate_tasks`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    const data = res.data;

    if (data.ret === 0) {
      dialogVisible = false;
      getExercisesList();
    } else {
      ElMessage.error('新建习题失败' + data.msg);
    }
  }).catch(() => {
    ElMessage.error('新建习题失败：网络错误');
  });
}

const deleteExercise = (exercise: any) => {
  const formData = new FormData();
  formData.append('id', exercise.id);
  axios.post(`${store.ip}/api/deleteExercise`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    ElMessage.success('删除成功');
    const data = res.data;
    if (data.ret === 0) {
      getExercisesList();
    } else {
      ElMessage.error('删除习题失败' + data.msg);
    }
  }).catch(() => {
    ElMessage.error('删除习题失败：网络错误');
  });
}


const handleChapterClick = (Chapter: any) => {
  chapter.value = { ...Chapter };
  activeChapter.value = Chapter.id;
  getExercisesList();
};


const formatExerciseContent = (content: string, maxLength: number = 50): string => {
  if (!content) return '';
  
  // 将 Markdown 转换为 HTML
  const html = marked.parse(content);
  
  // 创建临时 DOM 元素来解析 HTML
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = html;
  
  // 获取纯文本内容
  const plainText = tempDiv.textContent || tempDiv.innerText || '';
  
  // 截取指定长度并添加省略号
  return plainText.length > maxLength ? plainText.substring(0, maxLength) + '...' : plainText;
};

onMounted(() => {
  courseId.value = localStorage.getItem('selectedCourseID');
  courseName.value = localStorage.getItem('selectedCourseName');
  getChapterList();
  chapter.value = JSON.parse(localStorage.getItem('selectedChapter') || '{}');
  if (chapter.value?.id) {
    getExercisesList();
  }
});



</script>

<style scoped>

.main {
  display: flex;
  height: 100%;
  background-color: transparent;
  font-family: Arial, Helvetica, sans-serif;
}
.left-panel {
  width: 300px;
  background: var(--backgroundColor2);  
  border-right: 1px solid transparent;
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
  display: flex;
  flex-direction: column;
}
.course-header {
  padding: 24px 20px;
  border-bottom: 2px solid var(--backgroundColor3);
  background: transparent;
  color: var(--titleColor);
}

.course-name {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.sidebar {
  flex: 1;
  overflow-y: auto;
}


.chapter-navigation {
  flex: 1;
  overflow-y: auto;
}

.chapter-list {
  padding-bottom: 20px;
  padding-left: 5px;
  padding-right: 5px;
}

.chapter-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  margin-bottom: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  border-radius: 5px;
  background-color: transparent;
  color: var(--textColor2);
}

.chapter-item:hover {
  background-color: var(--backgroundColor2);
  color: var(--titleColor);
}

.chapter-item.active {
  color: var(--titleColor);
  background-color: var(--backgroundColor2);
  font-weight: 540;
}

.chapter-title {
  font-size: 14px;
  line-height: 1.4;
  flex: 1;
}

.chapter-btn {
  flex-grow: 1;
  margin-right: 4px;
}


.chapterBtn {
  width: 2rem;
  height: 2rem;
  margin-left: 1rem;
  font-size: 11px;
}

.chapterBtn:hover {
}
.nav-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--titleColor);
  padding: 20px 20px 16px 20px;
}

.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: transparent;
}

.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.exercise-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 题目内容 Markdown 样式 - Typora风格 */
.question-content {
  line-height: 1.7;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  font-size: 14px;
  color: #2c3e50;
}

/* 标题样式 */
.question-content h1,
.question-content h2,
.question-content h3,
.question-content h4,
.question-content h5,
.question-content h6 {
  margin: 24px 0 16px 0;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1.4;
}

.question-content h1 {
  font-size: 2em;
  border-bottom: 2px solid #eaecef;
  padding-bottom: 12px;
  margin-bottom: 20px;
}

.question-content h2 {
  font-size: 1.6em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 8px;
}

.question-content h3 {
  font-size: 1.3em;
}

.question-content h4 {
  font-size: 1.1em;
}

.question-content h5 {
  font-size: 1em;
}

.question-content h6 {
  font-size: 0.9em;
  color: #6a737d;
}

/* 段落样式 */
.question-content p {
  margin: 16px 0;
  text-align: justify;
  text-justify: inter-ideograph;
}

/* 列表样式 */
.question-content ul,
.question-content ol {
  margin: 16px 0;
  padding-left: 24px;
}

.question-content li {
  margin: 8px 0;
  line-height: 1.6;
}

.question-content ul li {
  list-style-type: disc;
}

.question-content ol li {
  list-style-type: decimal;
}

/* 嵌套列表 */
.question-content ul ul,
.question-content ol ol,
.question-content ul ol,
.question-content ol ul {
  margin: 4px 0;
}

/* 行内代码样式 */
.question-content code {
  background-color: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 3px;
  padding: 2px 6px;
  font-family: 'SFMono-Regular', 'Consolas', 'Liberation Mono', 'Menlo', 'Courier', monospace;
  font-size: 0.85em;
  color: #d73a49;
}

/* 代码块样式 */
.question-content pre {
  background-color: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
  overflow-x: auto;
  font-size: 0.85em;
  line-height: 1.45;
}

.question-content pre code {
  background: none;
  border: none;
  padding: 0;
  color: #24292e;
  font-size: inherit;
}

/* 引用样式 */
.question-content blockquote {
  border-left: 4px solid #dfe2e5;
  margin: 16px 0;
  padding: 0 16px;
  color: #6a737d;
  background-color: #f8f9fa;
  border-radius: 0 3px 3px 0;
}

.question-content blockquote p {
  margin: 12px 0;
}

/* 表格样式 */
.question-content table {
  border-collapse: collapse;
  margin: 20px 0;
  width: 100%;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  overflow: hidden;
}

.question-content th,
.question-content td {
  border: 1px solid #d0d7de;
  padding: 12px 16px;
  text-align: left;
  vertical-align: top;
}

.question-content th {
  background-color: #f6f8fa;
  font-weight: 600;
  color: #24292e;
}

.question-content tr:nth-child(even) {
  background-color: #f6f8fa;
}

.question-content tr:hover {
  background-color: #f1f8ff;
}

/* 链接样式 */
.question-content a {
  color: #0969da;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.2s ease;
}

.question-content a:hover {
  color: #0550ae;
  border-bottom-color: #0969da;
}

.question-content a:visited {
  color: #8250df;
}

/* 强调样式 */
.question-content strong {
  font-weight: 600;
  color: #24292e;
}

.question-content em {
  font-style: italic;
  color: #656d76;
}

/* 分隔线样式 */
.question-content hr {
  border: none;
  height: 2px;
  background-color: #d0d7de;
  margin: 24px 0;
  border-radius: 1px;
}

/* 删除线样式 */
.question-content del {
  text-decoration: line-through;
  color: #656d76;
}

/* 高亮样式 */
.question-content mark {
  background-color: #fff8c5;
  padding: 2px 4px;
  border-radius: 3px;
}

/* 图片样式 */
.question-content img {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
  margin: 16px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 任务列表样式 */
.question-content input[type="checkbox"] {
  margin-right: 8px;
  transform: scale(1.1);
}

.question-content .task-list-item {
  list-style: none;
  margin-left: -20px;
}

/* 键盘按键样式 */
.question-content kbd {
  background-color: #f6f8fa;
  border: 1px solid #d0d7de;
  border-bottom-color: #afb8c1;
  border-radius: 6px;
  box-shadow: inset 0 -1px 0 #afb8c1;
  color: #24292e;
  display: inline-block;
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 11px;
  line-height: 10px;
  padding: 3px 5px;
  vertical-align: middle;
}

/* 首行缩进优化 */
.question-content p:first-child {
  margin-top: 0;
}

.question-content p:last-child {
  margin-bottom: 0;
}

.question-content code {
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  color: #e6a23c;
}

.question-content pre {
  background: #f5f7fa;
  padding: 16px;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
  overflow-x: auto;
  margin: 16px 0;
}

.question-content pre code {
  background: none;
  padding: 0;
  color: #303133;
}

.question-content strong {
  font-weight: 600;
  color: #303133;
}

.question-content blockquote {
  margin: 16px 0;
  padding: 12px 16px;
  background: #f8f9fa;
  border-left: 4px solid #409eff;
  color: #606266;
}

.exercise-content {
  font-size: 16px;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
  flex: 1;
  width: 100%;
  max-width: 100%;
  color: #303133;
  font-weight: 500;
}

.exercise-meta {
  font-size: 12px;
  color: #606266;
  display: flex;
  justify-content: end;
  align-items: center;
  flex-shrink: 0;
}

.exercise-difficulty {
  color: #909399;
  margin-right: 1rem;
}


.exercise-type {
  background-color: #417dff;
  color: white;
  padding: 2px 8px;
  margin-right: 1rem;
  border-radius: 4px;
  font-weight: 500;
}

.exercise-item {
  background: white;
  padding: 16px;
  margin-bottom: 12px;
  border-radius: 8px;
  border: 1px solid #f8f8f8;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 80px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.exercise-item:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

.right-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin-top: 1rem;
}

.head-btn {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: end;
  margin-right: 24px;
}

.add-btn {
  margin-right: 2rem;
}

.function-btn {
  border-radius: 8px;
  font-weight: 500;
  padding: 12px 20px;
  transition: all 0.3s ease;
  border: 1px solid var(--textColor2);
  background-color: var(--backgroundColor2);
  color: var(--textColor2);
}

.function-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--shadowColor2);
  color: var(--textColor);
  border: 1px solid var(--textColor2);
}

.function-btn.active {
  background: #417dff;
  border-color: #409eff;
  color: white;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.4);
}

.function-btn :deep(.el-icon) {
  margin-right: 6px;
}
</style>