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
              <div class="chapter-item" :class="{ active: activeChapter === chapter.id }" v-for="chapter in chapters" :key="chapter.id" @click="handleChapterClick(chapter)">
                <span class="chapter-title">{{ chapter.name }}</span>
                <el-button type="text" class='chapterBtn' :icon="Edit" @click.stop="renameChapter(chapter)"></el-button>
                <el-button type="text" class='chapterBtn' :icon="Delete" @click.stop="deleteChapter(chapter.id)"></el-button>
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
      <div class="header-btn">
        <el-button type="primary" class='function-btn' @click="showExercises">习题</el-button>
        <el-button type="primary" class='function-btn' @click="toggleEditContent">
          {{ isEditing ? '保存' : '修改' }}
        </el-button>
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

    <el-dialog v-model="renameDialogVisible" title="重命名章节" width="30%">
      <el-input v-model="renameValue" placeholder="请输入新名称" clearable />
      <template #footer>
        <el-button @click="renameDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmRename">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue';
import { mainStore } from '../../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { marked } from 'marked';
import { ElMessage } from 'element-plus';
import A_Exercises from '../Exercises/index.vue'
import { Document, Edit, Delete } from '@element-plus/icons-vue';
const store = mainStore();
const courseId = ref('');
const courseName = ref('');
const chapters = ref([]);
const selectedChapter = ref<any>(null);
const isEditing = ref(false);
const editedContent = ref('');
const renameDialogVisible = ref(false);
const renameValue = ref('');
const renameTargetId = ref(0);
const activeChapter = ref<number | null>(null);

const renderedHtml = computed(() => {
  return marked(selectedChapter.value.content || '');
});



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



const deleteChapter = (id: number) => {
  const formData = new FormData();
  formData.append('id', id.toString());
  axios.post(`${store.ip}/api/deleteChapter`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    if (res.data.ret === 0) {
      ElMessage.success('删除成功');
      getChapterList();
      if (selectedChapter.value?.id === id) {
        selectedChapter.value = null;
        activeChapter.value = null;
      }
    } else {
      ElMessage.error('删除失败：' + res.data.msg);
    }
  }).catch(() => {
    ElMessage.error('删除失败：网络错误');
  });
};

const handleChapterClick = (chapter: any) => {
  selectedChapter.value = { ...chapter };
  activeChapter.value = chapter.id;
  isEditing.value = false;
  editedContent.value = chapter.content;
};

const toggleEditContent = () => {
  if (!selectedChapter.value) return;
  if (isEditing.value) {
    const formData = new FormData();
    formData.append('id', selectedChapter.value.id);
    formData.append('content', editedContent.value);
    axios.post(`${store.ip}/api/teacher/updateChapter`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      }
    }).then(res => {
      if (res.data.ret === 0) {
        ElMessage.success('保存成功');
        selectedChapter.value.content = editedContent.value;
        isEditing.value = false;
      } else {
        ElMessage.error('保存失败：' + res.data.msg);
      }
    }).catch(() => {
      ElMessage.error('保存失败：网络错误');
    });
  } else {
    isEditing.value = true;
  }
};

const renameChapter = (chapter: any) => {
  renameTargetId.value = chapter.id;
  renameValue.value = chapter.name;
  renameDialogVisible.value = true;
};

const confirmRename = () => {
  const formData = new FormData();
  formData.append('id', renameTargetId.value.toString());
  formData.append('name', renameValue.value);

  axios.post(`${store.ip}/api/teacher/updateChapter`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    if (res.data.ret === 0) {
      ElMessage.success('重命名成功');
      getChapterList();
      renameDialogVisible.value = false;
    } else {
      ElMessage.error('重命名失败：' + res.data.msg);
    }
  }).catch(() => {
    ElMessage.error('重命名失败：网络错误');
  });
};

const showExercises = () => {
  localStorage.setItem('selectedChapter', JSON.stringify(selectedChapter.value));

  store.addTab('习题列表', A_Exercises);

}

onMounted(() => {
  courseId.value = localStorage.getItem('selectedCourseId');
  courseName.value = localStorage.getItem('selectedCourseName');
  console.log('mounted courseId:', courseId.value);
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
  padding: 12px 16px;
  margin-bottom: 4px;
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
  margin-right: 1rem;
}

.chapter-btn {
  flex-grow: 1;
  margin-right: 4px;
}


.chapterBtn {
  font-size: 10px;
  padding: 2px 2px;
  height: auto;
  min-height: 20px;
  border-radius: 4px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  background-color: transparent;
  color: var(--textColor2);
}

.chapterBtn:hover:not(:disabled) {
  transform: translateY(-2px);
  color: var(--textColor);
  border: 1px solid transparent;
}


.chapterBtn :deep(.el-icon) {
  font-size: 15px;
}

.nav-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--titleColor);
  margin-left: auto;
  margin-right: auto;
  padding: 20px 20px 28px 20px;
}

.chapterTitle {
  color:var(--titleColor);
}

.chapter-head {
  display: flex;
  flex-direction: row;
}


.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: transparent;
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

.header-btn {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: end;
  margin-right: 24px;
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
</style>