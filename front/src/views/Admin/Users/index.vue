<template>
  <div class="main">
    <div class="students-list">
      <div class="left-title">
        <h2>学生列表</h2>
      </div>
      <div class="user-item" v-for="item in students" :key="item.id">
            <div class="info-name">
            <template v-if="item.editName">
              <div class="name">
              <strong>姓名：</strong>
              <el-input v-model="item.name" size="small" class="inline-input" />
              </div>
              <div class="name_btn">
              <el-button size="small" @click="cancelEditName(item)" class="edit-btn">取消</el-button>
              <el-button size="small" type="success" @click="saveInfo('name', item)" class="edit-btn">保存</el-button>
              </div>
            </template>
            <template v-else>
              <div class="name">
              <strong>姓名：</strong>
              <span>{{ item.name }}</span>
              </div>
              <el-button size="small" @click="startEditName(item)" class="edit-btn">修改</el-button>
            </template>
            </div>

            <div class="info_account"><strong>账号：</strong>{{ item.phone_number }}</div>

          <div class="info-gender">
            <template v-if="item.editGender">
              <div class="gender">
                <strong>性别：</strong>
                <el-select v-model="item.gender" placeholder="请选择" size="small" class="genderSelect">
                  <el-option label="男" value="male" />
                  <el-option label="女" value="female" />
                  <el-option label="保密" value="unknow" />
                </el-select>
              </div>
              <div class="gender_btn">
              <el-button size="small" @click="cancelEditGender(item)" class="edit-btn">取消</el-button>
              <el-button size="small" type="success" @click="saveInfo('gender', item)" class="edit-btn">保存</el-button>
              </div>

            </template>
            <template v-else>
              <div class="gender">
                <strong>性别：</strong>
              <span>{{ getGenderLabel(item.gender) }}</span>
              </div>              
              <el-button size="small" @click="startEditGender(item)" class="edit-btn">修改</el-button>
            </template>
          </div>

            <div class="info_time"><strong>在线时长：</strong>{{ formatDuration(item.sum_time) }}</div>
        <el-button @click="deleteStudent(item.id)" class="delete-btn">删除</el-button>
      </div>
    </div>
    <div class="teacher-list">
      <div class="right-title">
      <h2>教师列表</h2>
      </div>
      <div class="user-item" v-for="item in teachers" :key="item.id">
            <div class="info-name">
            <template v-if="item.editName">
              <div class="name">
              <strong>姓名：</strong>
              <el-input v-model="item.name" size="small" class="inline-input" />
              </div>
              <div class="name_btn">
              <el-button size="small" @click="cancelEditName(item)" class="edit-btn">取消</el-button>
              <el-button size="small" type="success" @click="saveInfo('name', item)" class="edit-btn">保存</el-button>
              </div>
            </template>
            <template v-else>
              <div class="name">
              <strong>姓名：</strong>
              <span>{{ item.name }}</span>
              </div>
              <el-button size="small" @click="startEditName(item)" class="edit-btn">修改</el-button>
            </template>
            </div>

            <div class="info_account"><strong>账号：</strong>{{ item.phone_number }}</div>

          <div class="info-gender">
            <template v-if="item.editGender">
              <div class="gender">
                <strong>性别：</strong>
                <el-select v-model="item.gender" placeholder="请选择" size="small" class="genderSelect">
                  <el-option label="男" value="male" />
                  <el-option label="女" value="female" />
                  <el-option label="保密" value="unknow" />
                </el-select>
              </div>
              <div class="gender_btn">
              <el-button size="small" @click="cancelEditGender(item)" class="edit-btn">取消</el-button>
              <el-button size="small" type="success" @click="saveInfo('gender', item)" class="edit-btn">保存</el-button>
              </div>

            </template>
            <template v-else>
              <div class="gender">
                <strong>性别：</strong>
              <span>{{ getGenderLabel(item.gender) }}</span>
              </div>              
              <el-button size="small" @click="startEditGender(item)" class="edit-btn">修改</el-button>
            </template>
          </div>

            <div class="info_time"><strong>在线时长：</strong>{{ formatDuration(item.sum_time) }}</div>
        <el-button @click="deleteStudent(item.id)" class="delete-btn">删除</el-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
const store = mainStore();
const students = ref([]);
const teachers = ref([]);
const originalName = ref('');
const originalGender = ref('');
const genderMap: Record<string, string> = {
  male: '男',
  female: '女',
  unknow: '保密'
};

const getGenderLabel = (gender: string): string => {
  return genderMap[gender];
};

const formatDuration = (seconds: number): string => {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return `${h}小时 ${m}分钟 ${s}秒`;
};


onMounted(() => {
    getStudentList();
    getTeacherList();
});

const getStudentList = () => {
    const formData = new FormData();
    formData.append('type', 'S');
    axios({
        method: 'post',
        url: `${store.ip}/api/admin/getUserList`,
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
                if (Array.isArray(responseData.userList)) {
                    responseData.userList.forEach(item => {
                        item.editName = false;
                        item.editGender = false;
                    });
                    students.value = responseData.userList;
                } else {
                    students.value = [];
                }
            } else {
                ElMessage({
                    message: '获取学生列表失败：' + responseData.msg,
                    type: 'error',
                });
            }
        })
        .catch((error) => {
            console.error('Error posting data:', error);
            ElMessage({
                message: '获取学生列表失败：网络错误，请稍后重试！',
                type: 'error',
                duration: 5000,
                grouping: true,
            });
        });
};

const getTeacherList = () => {
    const formData = new FormData();
    formData.append('type', 'T');
    axios({
        method: 'post',
        url: `${store.ip}/api/admin/getUserList`,
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
                if (Array.isArray(responseData.userList)) {
                    responseData.userList.forEach(item => {
                        item.editName = false;
                        item.editGender = false;
                    });
                    teachers.value = responseData.userList;
                } else {
                    teachers.value = [];
                }
            } else {
                ElMessage({
                    message: '获取教师列表失败：' + responseData.msg,
                    type: 'error',
                });
            }
        })
        .catch((error) => {
            console.error('Error posting data:', error);
            ElMessage({
                message: '获取教师列表失败：网络错误，请稍后重试！',
                type: 'error',
                duration: 5000,
                grouping: true,
            });
        });
};

const saveInfo = (field: 'name' | 'gender', item: any) => {
  const formData = new FormData();
  formData.append('id', item.id);

  if (field === 'name') {
    formData.append('name', item.name);
  }
  if (field === 'gender') {
    formData.append('gender', item.gender);
  }

  axios.post(`${store.ip}/api/updateInfo`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
  .then((res) => {
    if (res.data.ret === 0) {
      ElMessage.success('保存成功！');
      if (field === 'name') item.editName = false;
      if (field === 'gender') item.editGender = false;
    } else {
      ElMessage.error('保存失败：' + res.data.msg);
    }
  })
  .catch(() => {
    ElMessage.error('请求失败，请稍后重试！');
  });
};


const deleteStudent = (id: number) => {
    const formData = new FormData();
    formData.append('id', id);
    axios({
        method: 'post',
        url: `${store.ip}/api/admin/deleteUser`,
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
                ElMessage.success('删除成功');
                getStudentList();
            } else {
                ElMessage({
                    message: '删除失败：' + responseData.msg,
                    type: 'error',
                });
            }
        })
        .catch((error) => {
            console.error('Error posting data:', error);
            ElMessage({
                message: '删除失败：网络错误，请稍后重试！',
                type: 'error',
                duration: 5000,
                grouping: true,
            });
        });
}

const deleteTeacher = (id: number) => {
    const formData = new FormData();
    formData.append('id', id);
    axios({
        method: 'post',
        url: `${store.ip}/api/admin/deleteUser`,
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
                ElMessage.success('删除成功');
                getTeacherList();
            } else {
                ElMessage({
                    message: '删除失败：' + responseData.msg,
                    type: 'error',
                });
            }
        })
        .catch((error) => {
            console.error('Error posting data:', error);
            ElMessage({
                message: '删除失败：网络错误，请稍后重试！',
                type: 'error',
                duration: 5000,
                grouping: true,
            });
        });
}

const startEditName = (item: any) => {
  originalName.value = item.name;
  item.editName = true;
};
const cancelEditName = (item: any) => {
  item.name = originalName.value;
  item.editName = false;
};

const startEditGender = (item: any) => {
  originalGender.value = item.gender;
  item.editGender = true;
};
const cancelEditGender = (item: any) => {
item.gender = originalGender.value;
  item.editGender = false;
};

</script>

<style scoped>
.main {
  display: flex;
  height: 100%;
  background-color: transparent;
  font-family: Arial, Helvetica, sans-serif;
}

.students-list {
  width: 50%;
  background-color: transparent;
  display: flex;
  flex-direction: column;
  padding-right: 1rem;
}

.teacher-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: transparent;
}
.left-title {
  color: var(--titleColor);
  margin-bottom: 1rem;
  margin-top: 1rem;
}
.right-title {
  color: var(--titleColor);
  margin-bottom: 1rem;
  margin-top: 1rem;
}

.user-item {
  color: #080808;
  margin-bottom: 0.7rem;
  padding: 1rem;
  text-align: left;
  display: flex;
  flex-direction: column;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px var(--shadowColor);
  transition: all 0.3s ease;

}

.user-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px var(--shadowColor2);
}

.info-account {
  font-size: 16px;
  margin-bottom: 12px;
  display: flex;
  flex-direction: row;
  justify-content: left;
}

.info-name {
  font-size: 16px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.info-gender {
  font-size: 16px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  border-left: 0;
}
.gender {
  padding: 0;
}
.info-time {
  font-size: 16px;
  margin-bottom: 12px;
  display: flex;
  flex-direction: row;
  justify-content: left;
}

.edit-btn {
  margin-left: 10px;
  background-color: #417dff;
  color: #f8f8f8;
  outline: none;
  cursor: pointer;
  border-radius: 8px;
}
.edit-btn:hover {
  background-color: #719eff;
}


.genderSelect {
  width: 4rem;
}

.inline-input {
  max-width: 5rem;
  height: 1.5rem;
  width: auto;
  overflow-x: hidden;
}

.delete-btn {
  border: 1.2px solid red;
  color: red;
}

.delete-btn:hover {
  background-color: rgba(255, 163, 163, 0.271);
}

</style>