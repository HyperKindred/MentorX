<template>
  <div class="Main">
    <el-card class="info-card">
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="info-account">
            <strong>账号：</strong>{{ account }}
          </div>
        </el-col>

        <el-col :span="12">
          <div class="info-name">
            <template v-if="editName">
              <div class="name">
              <strong>姓名：</strong>
              <el-input v-model="name" size="small" class="inline-input" />
              </div>
              <div class="name_btn">
              <el-button size="small" @click="cancelEditName" class="edit-btn">取消</el-button>
              <el-button size="small" type="success" @click="saveInfo('name')" class="edit-btn">保存</el-button>
              </div>
            </template>
            <template v-else>
              <div class="name">
              <strong>姓名：</strong>
              <span>{{ name }}</span>
              </div>
              <el-button size="small" @click="startEditName" class="edit-btn">修改</el-button>
            </template>
          </div>
        </el-col>


        <el-col :span="12">
          <div class="info-gender">
            <template v-if="editGender">
              <div class="gender">
                <strong>性别：</strong>
                <el-select v-model="gender" placeholder="请选择" size="small" class="genderSelect">
                  <el-option label="男" value="male" />
                  <el-option label="女" value="female" />
                  <el-option label="保密" value="unknow" />
                </el-select>
              </div>
              <div class="gender_btn">
              <el-button size="small" @click="cancelEditGender" class="edit-btn">取消</el-button>
              <el-button size="small" type="success" @click="saveInfo('gender')" class="edit-btn">保存</el-button>
              </div>

            </template>
            <template v-else>
              <div class="gender">
                <strong>性别：</strong>
              <span>{{ genderText }}</span>
              </div>              
              <el-button size="small" @click="startEditGender" class="edit-btn">修改</el-button>
            </template>
          </div>
        </el-col>

        <el-col :span="12">
          <div class="info-type">
            <strong>身份：</strong>{{ getTypeLabel(type) }}
          </div>
        </el-col>


        <el-col :span="12">
          <div class="info-password">
            <div class="password">
            <strong>密码：</strong>
            <span>******</span>
            </div>

            <el-button size="small" type="primary" @click="showPasswordEdit = !showPasswordEdit" class="edit-btn">
              {{ showPasswordEdit ? '取消修改' : '修改密码' }}
            </el-button>
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
        <el-button type="success" @click="saveInfo('password')" class="edit-btn">保存新密码</el-button>
      </div>
    </el-card>
  </div>
</template>



<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue';
import { mainStore } from '../../store/index.ts';
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
const originalName = ref(name.value);
const originalGender = ref(gender.value);
const newPassword1 = ref('');
const newPassword2 = ref('');



const genderText = computed(() => {
  if (gender.value === 'male') return '男';
  if (gender.value === 'female') return '女';
  return '未知';
});

const typeMap: Record<string, string> = {
  T: '教师',
  S: '学生',
  A: '管理员'
};

const getTypeLabel = (type: string): string => {
  return typeMap[type] || '未知';
};

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

const startEditName = () => {
  originalName.value = name.value;
  editName.value = true;
};
const cancelEditName = () => {
  name.value = originalName.value;
  editName.value = false;
};

const startEditGender = () => {
  originalGender.value = gender.value;
  editGender.value = true;
};
const cancelEditGender = () => {
  gender.value = originalGender.value;
  editGender.value = false;
};


</script>

<style scoped>

.info-card {
  font-family: Arial, Helvetica, sans-serif;
  width: 80%;
  margin: 50px auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
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
  margin-bottom: 12px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.info-gender {
  font-size: 16px;
  margin-bottom: 12px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.info-type {
  font-size: 16px;
  margin-bottom: 12px;
  display: flex;
  flex-direction: row;
  justify-content: left;
}
.info-password {
  font-size: 16px;
  margin-bottom: 12px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
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
.password-edit {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 0.5rem;
}
.password-input {
  width: 300px;
  margin-bottom: 0.5rem;
  border: none;
}



</style>