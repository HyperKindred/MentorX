<template>
  <div class="Main">
    <div class="sidebar">
      <el-button type="primary" @click="dialogVisible = true" class="add-btn">新建章节</el-button>
      <div class="chapter-list">
        <el-space direction="vertical" fill>
          <div
            class="chapter-item"
            v-for="chapter in chapters"
            :key="chapter.id"
          >
            <el-button
              type="default"
              class="chapter-btn"
              @click="handleChapterClick(chapter)"
            >
              {{ chapter.name }}
            </el-button>
            <el-button type="text" @click.stop="renameChapter(chapter)">重命名</el-button>
            <el-button type="text" style="color: red" @click.stop="deleteChapter(chapter.id)">删除</el-button>
          </div>
        </el-space>
      </div>
    </div>
    <div class="content-area" v-if="selectedChapter">
      <div class="header">
        <h3>{{ selectedChapter.name }}</h3>
        <el-button type="primary" @click="showExercises">习题</el-button>
        <el-button type="primary" @click="toggleEditContent">
          {{ isEditing ? '保存' : '修改课件内容' }}
        </el-button>
      </div>

      <div class="chapter-content">
        <el-input
          v-if="isEditing"
          type="textarea"
          v-model="editedContent"
          rows="20"
          resize="none"
        />
        <el-scrollbar v-else class="read-only-content">
          <pre>{{ selectedChapter.content }}</pre>
        </el-scrollbar>
      </div>
    </div>
    <div class="content-area" v-else>
      <p style="text-align: center; margin-top: 100px; color: #999;">请先选择一个章节</p>
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
import { ref, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import T_exercise from '../Exercise/index.vue'
const store = mainStore();
const courseId = ref('');
const chapters = ref([]);
const dialogVisible = ref(false);
const Cname = ref('');
const selectedChapter = ref<any>(null);
const isEditing = ref(false);
const editedContent = ref('');
const renameDialogVisible = ref(false);
const renameValue = ref('');
const renameTargetId = ref(0);

const handleAddChapter = () => {
  if (!Cname.value.trim()) {
    ElMessage.warning('请输入章节名称');
    return;
  }
  const formData = new FormData();
  formData.append('chapter', Cname.value)
  formData.append('Cno', courseId.value)
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
  formData.append('id', courseId.value)
  axios({
    method: 'post',
    url: `${store.ip}/api/getChapterList`,
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
    .then((response) => {
      const responseData = response.data;
      if (responseData.ret === 0) {
        if (responseData.chapterList?.chapter){
        chapters.value = Array.isArray(responseData.chapterList.chapter)
          ? responseData.chapterList.chapter
          : [responseData.chapterList.chapter];
          }
          else {
            chapters.value = [];
          }
      } else {
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
  courseId.value = localStorage.getItem('selectedCourseId');
  getChapterList();
});


</script>

<style scoped>

.sidebar {
  width: 20%;
  background-color: #fff;
  border-right: 1px solid #ddd;
  padding: 16px;
  box-sizing: border-box;
  overflow-y: auto;
}

.chapter-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chapter-btn {
  flex-grow: 1;
  margin-right: 4px;
}

.add-btn {
  width: 100%;
  margin-bottom: 16px;
}

.content-area {
  flex-grow: 1;
  padding: 24px;
  overflow-y: auto;
  background-color: #f9f9f9;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chapter-content {
  margin-top: 16px;
}

.read-only-content {
  padding: 12px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  white-space: pre-wrap;
  max-height: 70vh;
}

</style>