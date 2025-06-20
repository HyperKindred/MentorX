<template>
    <el-dialog v-model="dialogVisible" class="signin-wrapper" width="400px" center :show-close="false">
        <div class="container" ref="containerRef">
            <div class="form-container sign-up-container">
                <form action="#">
                    <h1>用户注册</h1> 
                    <input type="text" v-model="account" placeholder="请输入手机号">
                    <input type="text" v-model="name" placeholder="请输入姓名">
                    <input type="password" v-model="password" placeholder="请设置密码">
                    <div class="type">
                        <h2 class="input-title">请选择身份</h2>
                        <el-select v-model="type" placeholder="身份" style="width: 115px" size="large">
                        <el-option label="教师" value="T" />
                        <el-option label="学生" value="S" />
                        <el-option label="管理员" value="A" />
                        </el-select>
                    </div>
                    <div class="gender">
                        <h2 class="input-title">请选择性别</h2>
                        <el-select v-model="gender" placeholder="性别" style="width: 115px" size="large">
                        <el-option label="男" value="male" />
                        <el-option label="女" value="female" />
                        <el-option label="保密" value="unknow" />
                        </el-select>
                    </div>
                    <button @click.prevent="signUp()">
                        注册
                    </button>

                </form>
            </div>
            <div class="form-container sign-in-container">
                <form action="#">
                    <h1>用户登录</h1>
                    <div>
                    <input type="text" v-model="account" placeholder="请输入手机号">
                    <input type="password" v-model="password" placeholder="请输入密码">
                    </div>
                    <button @click.prevent="signIn()">
                        登录
                    </button>
                </form>
            </div>
            <div class="overlay-container">
                <div class="overlay">
                    <div class="overlay-pannel overlay-left">
                        <h1>已有账号?</h1>
                        <p>用现有账号直接登录</p>
                        <button class="ghost" @click="goSignIn">登录</button>
                    </div>
                    <div class="overlay-pannel overlay-right">
                        <h1>没有账号?</h1>
                        <p>注册一个账号</p>
                        <button class="ghost" @click="goSignUp">注册</button>
                    </div>
                </div>
            </div>
        </div>
    </el-dialog>
</template>
<script setup lang="ts" >
import router from "../../router/index.ts";
import { mainStore } from '../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { ref, watch, onMounted  } from 'vue';

const store = mainStore();
const account = ref('');
const password = ref('');
const name = ref('');
const type = ref('');
const gender = ref('');
const containerRef = ref<HTMLElement | null>(null);
const props = defineProps<{ visible: boolean }>()
const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
  (e: 'close-login'): void
}>()
const dialogVisible = ref(props.visible)
watch(() => props.visible, (val) => {
  dialogVisible.value = val
})
watch(dialogVisible, (val) => {
  emit('update:visible', val)
})

const signUp = () => {
    if (account.value === '' || password.value === '' || name.value === '' || type.value === '' || gender.value === '') {
        ElMessage({message: '请完整填写信息', type: 'error', duration: 5 * 1000, grouping: true});
        return;
    }
    let formData = new FormData();
    formData.append('phone_number', account.value);
    formData.append('password', password.value);
    formData.append('name', name.value);
    formData.append('type', type.value);
    formData.append('gender', gender.value);

    axios({
        method: 'post', 
        url: `${store.ip}/api/register`, 
        data: formData, 
        headers:{'Content-Type': 'multipart/form-data'}}
    )
    .then(response => {
        let responseData = response.data;
        if (responseData.ret === 0) {
        localStorage.setItem('account', account.value);
        localStorage.setItem('name', name.value);
        goSignIn();
        } else if(responseData.ret === 1) {
        ElMessage({message: '注册失败：' + responseData.msg, type: 'error', duration: 5 * 1000, grouping: true});
        }
    })
}

const signIn = () =>{
    if (account.value === '' || password.value === '') {
        ElMessage({message: '账号和密码不能为空', type: 'error', duration: 5 * 1000, grouping: true});
        return;
    }
    
    let formData = new FormData();
    formData.append('phone_number', account.value);
    formData.append('password', password.value);
    
    axios({
        method: 'post',        
        url: `${store.ip}/api/signIn`, 
        data: formData, 
        headers:{'Content-Type': 'multipart/form-data'}}
    )
    .then(response => {
        localStorage.setItem('password', password.value);
        let responseData = response.data;
        if (responseData.ret === 0) {
            localStorage.setItem('account', account.value);
            localStorage.setItem('gender', responseData.gender);
            localStorage.setItem('type', responseData.type);
            localStorage.setItem('name', responseData.name);
            localStorage.setItem('token', response.data.jwt);
            emit('close-login');
            store.getUserInfo();           
        } else if(responseData.ret === 1) {
            ElMessage({message: '登录失败：' + responseData.msg, type: 'error', duration: 5 * 1000, grouping: true});
        }
    })
    .catch(error => {
        console.error('Error posting data:', error);
        ElMessage({message: '登录失败：网络错误，请稍后重试！', type: 'error', duration: 5 * 1000, grouping: true});
    });

}

const goSignIn = () => {
  containerRef.value?.classList.remove('right-pannel-active');
};

const goSignUp = () => {
  containerRef.value?.classList.add('right-pannel-active');
};

onMounted(() => {

});
</script>
<style>
 * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
 }

 .signin-wrapper {
    font-family: Arial, Helvetica, sans-serif;
    background-color: #f8f8f800;
    background-attachment: fixed;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    margin: 0 auto;
    color: #080808;
 }

/* 使用 :deep() 正确覆盖 Element Plus 内部样式 */
.signin-wrapper :deep(.el-dialog) {
  background-color: transparent !important;
  border: none !important;
  padding: 0 !important;
}

.signin-wrapper :deep(.el-dialog__header) {
  display: none !important;
  box-shadow: none !important;
}

.el-dialog {
    box-shadow: none !important;
}
.signin-wrapper :deep(.el-dialog__body) {
  padding: 0 !important;
}

/* 透明遮罩层（可选） */
.signin-wrapper :deep(.el-overlay) {
  background-color: transparent !important;
}


.h1 {
    margin: 0.2rem;
    font-size: 1.2rem;
}

.p {
    font-size: 1rem;
    line-height: 1.5rem;
    font-weight: 100;
    margin: 1.2rem 0;
    letter-spacing: 0.1rem;
}

.h2 {
    margin: 0.2rem;
    font-size: 1rem;
}

.container {
    position: relative;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
    padding: 0.6rem;
    width: 50rem;
    height: 35rem;
    overflow: hidden;
    max-width: 100vw;
    min-height: 70vh;
}

.form-container form {
    background-color: #fff;
    display: flex;
    flex-direction: column;
    padding: 0 1.8rem;
    height: 100%;
    justify-content: center;
    align-items: center;
}

.form-container input {
    width: 100%;
    height: 2.2rem;
    text-indent: 1rem;
    border: 1px solid #ccc;
    border-left: none;
    border-top: none;
    border-right: none;
    outline: none;
    margin: 0.6rem 0;
}

.form-container button:active {
    transform: scale(0.95 0.95);
}

.form-container button:hover {
    background-color: #417dffd8;
}

.form-container button {
    padding: 0.4rem 1rem;
    background-color: #417dff;
    color: white;
    border: 1px solid #fff;
    outline: none;
    cursor: pointer;
    width: 5rem;
    border-radius: 8px;
    transition: all 100ms ease-in;
    margin: 0.6rem 0;
    font-size: 0.6rem;
    padding: 0.5rem 0;
}

button#register {
    width: 100%;
}

button.ghost{
    background: transparent;
    border-color: #fff;
    border: 1px solid #fff;
    outline: none;
    cursor: pointer;
    width: 5rem;
    border-radius: 8px;
    transition: all 800ms ease-in;
    margin: 0.6rem 0;
    padding: 0.5rem 0;
    color: white;
    font-size: 0.6rem;
}

button.ghost:active{
    transform: scale(0.95 0.95);
}

button.ghost:hover{
    color: rgb(225, 225, 225);
    border-color: rgb(225, 225, 225);
}

.form-container {
    position: absolute;
    top: 0;
    height: 100%;
    transition: all 0.5s ease-in;
}

.sign-in-container {
    left: 0;
    width: 50%;
    z-index: 2;
}

.sign-up-container {
    left: 0;
    width: 50%;
    opacity: 0;
    z-index: 1;
}

.overlay {
    background-color: #417dff;
    width: 200%;
    height: 100%;
    position: relative;
    left: -100%;
    transition: all 0.6s ease-in-out;
    color: white;
}

.overlay-container {
    position: absolute;
    top: 0;
    right: 0;
    width: 50%;
    height: 100%;
    overflow: hidden;
    transition: all 0.6s ease-in-out;
    z-index: 99;
}

.overlay-pannel {
    position: absolute;
    top: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 50%;
    height: 100%;
    padding: 0 2.2rem;
}

.overlay-right {
    right: 0;
}

.container.right-pannel-active .overlay-container {
    transform: translateX(-100%);
}

.container.right-pannel-active .sign-in-container {
    transform: translateX(100%);
} 

.container.right-pannel-active .sign-up-container {
    transform: translateX(100%);
    opacity: 1;
    z-index: 5;
    transition: all 0.6s ease-in-out;
} 

.container.right-pannel-active .overlay {
    transform: translateX(50%);
}

.container.right-pannel-active .overlay-left {
    transform: translateX(0);
    transition: all 0.6s ease-in-out;
}

.container.right-pannel-active .overlay-right {
    transform: translateX(20%);
    transition: all 0.6s ease-in-out;
}


</style>