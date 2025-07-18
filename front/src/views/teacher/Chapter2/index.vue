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
              <div v-for="chapter in chapters" :key="chapter.id" @click="handleChapterClick(chapter)" class="chapter-item" :class="{ active: activeChapter === chapter.id }"  >
                <span class="chapter-title">{{ chapter.name }}</span>
              </div>
            </el-space>
          </div>
        </div>  
      </div>
    </div>
    <div class="right-panel">
      <div class="content-area" v-if="selectedChapter">
        <div class="header">
          <h3 class="chapterTitle">{{ selectedChapter.name }}</h3>
        </div>
        <!-- 功能按钮组 -->
        <div class="function-buttons">
          <div class="edit-buttons">
            <el-button type="primary" @click="exportToWord" class='function-btn'>导出为 Word</el-button>
            <el-button type="primary" @click="exportToPPT" class='function-btn'>导出为 PPT</el-button>
          </div>
        </div>

        <div class="chapter-content">
          <el-input v-if="isEditing" type="textarea" class='edit-content' v-model="editedContent" rows="20" resize="none" />
          <el-scrollbar v-else class="read-only-content">
            <div v-html="renderedHtml"></div>
          </el-scrollbar>
        </div>
      </div>
      <div class="content-area" v-else>
        <p style="text-align: center; margin-top: 100px; color: #999;">请先选择一个章节</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue';
import { mainStore } from '../../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { marked } from 'marked';
import { ElMessage } from 'element-plus';
import { Document, Edit, Delete } from '@element-plus/icons-vue';
const store = mainStore();
const courseId = ref('');
const chapters = ref([]);
const selectedChapter = ref<any>(null);
const activeChapter = ref<number | null>(null);
const isEditing = ref(false);
const editedContent = ref('');
interface Chapter {
  id: number;
  name: string;
  content: string;
}

const renderedHtml = computed(() => {
  return marked(selectedChapter.value.content || '');
});

const exportToWord = () => {
  if (!selectedChapter.value) {
    ElMessage.warning('请先选择章节');
    return;
  }

  const markdown = selectedChapter.value.content || '';
  const htmlContent = marked(markdown);

  const fullHtml = `
  <!DOCTYPE html>
  <html>
  <head><meta charset="utf-8"><title>${selectedChapter.value.name}</title></head>
  <body>${htmlContent}</body>
  </html>
  `;

  const blob = (window as any).htmlDocx.asBlob(fullHtml);
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${selectedChapter.value.name}.docx`;
  a.click();
};

const exportToPPT = () => {
  if (!selectedChapter.value) {
    ElMessage.warning('请先选择章节');
    return;
  }

  const formData = new FormData();
  formData.append('chapter_id', selectedChapter.value.id.toString());
  
  ElMessage.info('正在生成PPT，请稍候...');
  
  axios({
    method: 'post',
    url: `${store.ip}/api/generatePPT`,
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
    data: formData,
  })
    .then((response) => {
      const res = response.data;
      if (res.ret === 0) {
        ElMessage.success('PPT生成成功，下载即将开始');
      } else {
        ElMessage.error('PPT生成失败：' + (res.msg || '未知错误'));
      }
    })
    .catch((error) => {
      console.error('PPT生成失败:', error);
      ElMessage.error('PPT生成失败：网络错误，请稍后重试！');
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



const handleChapterClick = (chapter: any) => {
  selectedChapter.value = { ...chapter };
  activeChapter.value = chapter.id;
  isEditing.value = false;
  editedContent.value = chapter.content;
};



onMounted(() => {
  courseId.value = localStorage.getItem('selectedCourseId');
  getChapterList();
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
  border-right: 1.5px solid transparent;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
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
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  border-radius: 5px;
  background-color: transparent;
  color: var(--textColor2);
  width: 270px;
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

.chapter-actions {
  display: flex;
  margin-left: 16px;
  opacity: 1;
  transition: all 0.2s ease;
}

.chapter-actions .chapter-btn.function-btn-left {
  font-size: 10px;
  padding: 2px 2px;
  height: auto;
  min-height: 20px;
  border-radius: 4px;
  font-weight: 500;
}

.nav-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--titleColor);
  margin-left: auto;
  margin-right: auto;
  padding: 20px 20px 28px 20px;
}

.add-btn {
  width: 4rem;
  height: 2rem;
  margin-top: 1rem;
  margin-left: 0.7rem;
  font-size: 1.3rem;
  color: var(--textColor2);
  border: transparent;
  background-color: transparent;
  padding: 0;
}
.is-loading {
  width: 2rem;
  height: 2rem;
  margin-right: 1rem;
  padding-left: 5px;
}

.add-btn:hover {
  color: var(--textColor);
}

.chapterTitle {
  color: var(--titleColor);
}

.chapter-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}


.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: transparent;
}

.content-area {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chapter-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  text-align: left;
  min-height: 500px;
}

.header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin-top: 1.5rem;
}

/* 功能按钮组样式 */
.function-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  padding-bottom: 0;
  background: transparent;
}

.button-group {
  display: flex;
  gap: 12px;
  align-items: center;
}

.edit-buttons {
  display: flex;
  gap: 12px;
  align-items: center;
}

.function-btn-left {
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  background-color: transparent;
  color: var(--textColor2);
}

.function-btn-left:hover:not(:disabled) {
  transform: translateY(-2px);
  color: var(--textColor);
  border: 1px solid transparent;
}

.function-btn-left.active {
  background: #417dff;
  border-color: #409eff;
  color: white;
  box-shadow: 0 2px 8px var(--shadowColor);
}

.function-btn-left :deep(.el-icon) {
  font-size: 15px;
}


.function-btn {
  border-radius: 8px;
  font-weight: 500;
  padding: 12px 20px;
  transition: all 0.3s ease;
  border: 1.5px solid var(--textColor2);
  background-color: var(--backgroundColor);
  color: var(--textColor2);
}

.function-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--shadowColor2);
  color: var(--textColor);
  border: 1.5px solid var(--textColor2);
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

.read-only-content {
  padding: 2rem;
  background: var(--backgroundColor3);
  border: 1px solid #ddd;
  border-radius: 6px;
  white-space: pre-wrap;
  max-height: 70vh;
  color: var(--textColor);
}

.edit-content :deep(.el-textarea__inner){
  max-height: 70vh;
  background: var(--backgroundColor3);
  color: var(--textColor);
  padding: 2rem;
  border-radius: 6px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .loading-animation {
    width: 300px;
    padding: 20px;
  }
  
  .loading-spinner {
    width: 80px;
    height: 80px;
  }
  
  .loading-text {
    font-size: 16px;
  }
}
</style>