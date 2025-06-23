<template>
  <div class="Main">
    <div class="students-list">
      <h2>学生列表</h2>
      <div class="user-item" v-for="item in students" :key="item.id">
        <div class="user-account">手机号：{{ item.phone_number }}</div>
            <strong>姓名：</strong>
            <template v-if="item.editName">
              <el-input v-model="item.name" size="small" class="inline-input" />
              <el-button size="small" @click="cancelEditName(item)" class="edit-btn">取消</el-button>
              <el-button size="small" type="success" @click="saveInfo('name', item)" class="edit-btn">保存</el-button>
            </template>
            <template v-else>
              <span>{{ item.name }}</span>
              <el-button size="small" @click="startEditName(item)" class="edit-btn">修改</el-button>
            </template>
        <strong>性别：</strong>
            <template v-if="item.editGender">
              <el-select v-model="item.gender" placeholder="请选择" size="small" class="genderSelect">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
                <el-option label="保密" value="unknow" />
              </el-select>
              <el-button size="small" @click="cancelEditGender(item)" class="edit-btn">取消</el-button>
              <el-button size="small" type="success" @click="saveInfo('gender', item)" class="edit-btn">保存</el-button>
            </template>
            <template v-else>
              <span>{{ getGenderLabel(item.gender) }}</span>
              <el-button size="small" @click="startEditGender(item)" class="edit-btn">修改</el-button>
            </template>
        <el-button @click="deleteStudent(item.id)">删除</el-button>
      </div>
    </div>
    <div class="teacher-list">
      <h2>教师列表</h2>
      <div class="user-item" v-for="item in teachers" :key="item.id">
        <div class="user-account">手机号：{{ item.phone_number }}</div>
            <strong>姓名：</strong>
            <template v-if="item.editName">
              <el-input v-model="item.name" size="small" class="inline-input" />
              <el-button size="small" @click="cancelEditName(item)" class="edit-btn">取消</el-button>
              <el-button size="small" type="success" @click="saveInfo('name', item.id)" class="edit-btn">保存</el-button>
            </template>
            <template v-else>
              <span>{{ item.name }}</span>
              <el-button size="small" @click="startEditName(item)" class="edit-btn">修改</el-button>
            </template>
        <strong>性别：</strong>
            <template v-if="item.editGender">
              <el-select v-model="item.gender" placeholder="请选择" size="small" class="genderSelect">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
                <el-option label="保密" value="unknow" />
              </el-select>
              <el-button size="small" @click="cancelEditGender(item)" class="edit-btn">取消</el-button>
              <el-button size="small" type="success" @click="saveInfo('gender', item)" class="edit-btn">保存</el-button>
            </template>
            <template v-else>
              <span>{{ getGenderLabel(item.gender) }}</span>
              <el-button size="small" @click="startEditGender(item)" class="edit-btn">修改</el-button>
            </template>
        <el-button @click="deleteTeacher(item.id)">删除</el-button>
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
  unknown: '未知'
};

const getGenderLabel = (gender: string): string => {
  return genderMap[gender];
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


</style>