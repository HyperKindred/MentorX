<template>
  <div class="main">
    <div class="left-panel">
      <div class="course-header">
        <h2 class="course-name">{{ courseName }}</h2>
      </div>
      <div class="chapter-navigation">
        <div class="chapter-head">
        <h3 class="nav-title">课程章节</h3>
        <el-button type="primary" @click="dialogVisible = true" class="add-btn">新建章节</el-button>
        </div>

        <div class="sidebar">
          <div class="chapter-list">
            <el-space direction="vertical" fill>
              <div class="chapter-item" v-for="chapter in chapters" :key="chapter.id" @click="handleChapterClick(chapter)">
                <span class="chapter-title">{{ chapter.name }}</span>
                <el-button type="text" class='chapterBtn' style="color: white;" @click.stop="renameChapter(chapter)">重命名</el-button>
                <el-button type="text" class='chapterBtn' style="color: red" @click.stop="deleteChapter(chapter.id)">删除</el-button>
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
        <el-button type="primary" class='head-btn' @click="showExercises">习题</el-button>
        <el-button type="primary" class='head-btn' @click="toggleEditContent">
          {{ isEditing ? '保存' : '修改' }}
        </el-button>
        <el-button type="primary" @click="exportToWord" class='head-btn'>导出为 Word</el-button>
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

    <el-dialog v-model="dialogVisible" title="新建章节" width="30%">
      <el-input v-model="Cname" placeholder="请输入章节名称" clearable />
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAddChapter">新建</el-button>
      </template>
    </el-dialog>

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
import T_Exercises from '../Exercises/index.vue'
const store = mainStore();
const courseId = ref('');
const courseName = ref('');
const chapters = ref([]);
const dialogVisible = ref(false);
const Cname = ref('');
const selectedChapter = ref<any>(null);
const isEditing = ref(false);
const editedContent = ref('');
const renameDialogVisible = ref(false);
const renameValue = ref('');
const renameTargetId = ref(0);


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




const handleAddChapter = () => {
  if (!Cname.value.trim()) {
    ElMessage.warning('请输入章节名称');
    return;
  }
  const formData = new FormData();
  formData.append('chapter', Cname.value)
  formData.append('Cno', courseId)
  axios({
    method: 'post',
    url: `${store.ip}/api/teacher/generate_teachcontent`,
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
    data: formData,
  })
    .then((response) => {
      const res = response.data;
      if (res.ret === 0) {
        ElMessage.success('课件生成成功！');
        Cname.value = '';
        dialogVisible.value = false;
        getChapterList();
      } else {
        ElMessage.error('课件生成失败：' + res.msg);
      }
    })
    .catch(() => {
      ElMessage.error('请求失败，请稍后重试！');
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

  store.addTab('习题列表', T_Exercises);

}

onMounted(() => {
  courseId.value = localStorage.getItem('selectedCourseID');
  courseName.value = localStorage.getItem('selectedCourseName');
  getChapterList();
});


</script>

<style scoped>
.main {
  display: flex;
  height: 100%;
  background-color: transparent;
}

.left-panel {
  width: 300px;
  background: transparent;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}
.course-header {
  padding: 24px 20px;
  border-bottom: 1.5px solid #e4e7ed;
  background: transparent;
  color: #f8f8f8;
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

.chapter-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 4px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  background-color: #208bf6ab;
}

.chapter-item:hover {
  background-color: #65b2ffa9;
  color: #f8f8f8;
}

.chapter-item.active {
  background-color: #e8f4fd;
  border-color: #409eff;
  color: #409eff;
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
  color: #f8f8f8;
  margin-left: 5.5rem;
  padding: 20px 20px 16px 20px;
}
.add-btn {
  width: 4rem;
  height: 2rem;
  margin-top: 1rem;
  margin-left: 0.7rem;
  font-size: 11px;
}

.chapterTitle {
  color:black;
}

.chapter-head {
  display: flex;
  flex-direction: row;
}


.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
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
  margin-right: 2rem;
}

.head-btn {
  
}


.read-only-content {
  padding: 12px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  white-space: pre-wrap;
  max-height: 70vh;
  color: black;
}

.edit-content {

}
</style>