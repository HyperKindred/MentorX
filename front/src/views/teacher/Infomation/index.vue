<template>
  <div class="Main">
    <el-card class="info-card">
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="info-item">
            <strong>账号：</strong>{{ account }}
          </div>
        </el-col>

        <el-col :span="12">
          <div class="info-item">
            <strong>密码：</strong>
            <span>******</span>
            <el-button size="small" type="primary" @click="showPasswordEdit = !showPasswordEdit" class="edit-btn">
              修改密码
            </el-button>
          </div>
        </el-col>

        <el-col :span="12">
          <div class="info-item">
            <strong>性别：</strong>
            <template v-if="editGender">
              <el-select v-model="gender" placeholder="请选择" size="small">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
                <el-option label="保密" value="unknow" />
              </el-select>
              <el-button size="small" type="success" @click="saveInfo('gender')" class="edit-btn">保存</el-button>
            </template>
            <template v-else>
              <span>{{ genderText }}</span>
              <el-button size="small" @click="editGender = true" class="edit-btn">修改</el-button>
            </template>
          </div>
        </el-col>

        <el-col :span="12">
          <div class="info-item">
            <strong>身份：</strong>{{ type }}
          </div>
        </el-col>

        <el-col :span="12">
          <div class="info-item">
            <strong>姓名：</strong>
            <template v-if="editName">
              <el-input v-model="name" size="small" class="inline-input" />
              <el-button size="small" type="success" @click="saveInfo('name')" class="edit-btn">保存</el-button>
            </template>
            <template v-else>
              <span>{{ name }}</span>
              <el-button size="small" @click="editName = true" class="edit-btn">修改</el-button>
            </template>
          </div>
        </el-col>
      </el-row>

      <div v-if="showPasswordEdit" class="password-edit">
        <el-input
          v-model="newPassword1"
          placeholder="请输入新密码"
          show-password
          type="password"
          class="password-input"
        />
        <el-input
          v-model="newPassword2"
          placeholder="请再次输入新密码"
          show-password
          type="password"
          class="password-input"
        />
        <el-button type="success" @click="saveInfo('password')">保存新密码</el-button>
      </div>
    </el-card>
  </div>
</template>



<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue';
import { mainStore } from '../../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
const store = mainStore();
const router = useRouter();
const account = ref(localStorage.getItem('account') || '');
const password = ref(localStorage.getItem('password') || '');
const gender = ref(localStorage.getItem('gender') || '');
const type = ref(localStorage.getItem('type') || '');
const name = ref(localStorage.getItem('name') || '');
const editName = ref(false);
const editGender = ref(false);
const showPasswordEdit = ref(false);


const genderText = computed(() => {
  if (gender.value === 'male') return '男';
  if (gender.value === 'female') return '女';
  return '保密';
});

onMounted(() => {

});

const saveInfo = (field: 'name' | 'gender' | 'password') => {
  const formData = new FormData();

  if (field === 'name') {
    formData.append('name', name.value);
  }

  if (field === 'gender') {
    formData.append('gender', gender.value);
  }

  if (field === 'password') {
    if (newPassword1.value !== newPassword2.value || newPassword1.value.length === 0) {
      ElMessage.error('两次输入的密码不一致或为空');
      return;
    }
    formData.append('password', newPassword1.value);
  }

  axios({
    method: 'post',
    url: `${store.ip}/api/updateInfo`,
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
    data: formData,
  })
    .then((response) => {
      const res = response.data;
      if (res.ret === 0) {
        ElMessage.success('保存成功！');
        if (field === 'name') editName.value = false;
        if (field === 'gender') editGender.value = false;
        if (field === 'password') {
          showPasswordEdit.value = false;
          password.value = newPassword1.value;
          newPassword1.value = '';
          newPassword2.value = '';
          localStorage.setItem('password', password.value);
        }
        // 同步本地
        localStorage.setItem('name', name.value);
        localStorage.setItem('gender', gender.value);
        store.getUserInfo();
      } else {
        ElMessage.error('保存失败：' + res.msg);
      }
    })
    .catch(() => {
      ElMessage.error('请求失败，请稍后重试！');
    });
};


</script>

<style scoped>

.info-card {
  width: 60%;
  margin: 50px auto;
  padding: 20px;
}
.info-item {
  font-size: 16px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.inline-input {
  width: 60%;
}
.edit-btn {
  margin-left: 10px;
}
.password-edit {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.password-input {
  width: 300px;
}



</style>