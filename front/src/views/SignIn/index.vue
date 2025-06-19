<template>
  <el-dialog v-model="dialogVisible" class="signin-wrapper" width="400px" center>
        <h1 class="header">登录</h1>
        <div class="form-wrapper">
          <h2 class="input-title">账号</h2>
          <input type="text" v-model="account" placeholder="请输入手机号" class="input-item">
          <h2 class="input-title">密码</h2>
          <input type="password" v-model="password" placeholder="请输入密码" class="input-item">
          <button @click="signIn" class="btn">登录</button>
        </div>
        <div class="msg">
          没有账户？
          <span class="link-button" @click="$emit('switch-to-signup')">立即注册</span>
        </div>
  </el-dialog>
</template>


<script setup lang="ts" >
import router from "../../router/index.ts";
import { mainStore } from '../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { ref, watch } from 'vue';

const store = mainStore();
const account = ref('');
const password = ref('');
const props = defineProps<{ visible: boolean }>()
const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
  (e: 'switch-to-signup'): void
}>()

const dialogVisible = ref(props.visible)
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

watch(() => props.visible, (val) => {
    dialogVisible.value = val
})

watch(dialogVisible, (val) => {
    emit('update:visible', val)
})
</script>

<style scoped>
    .container {
        height: 100vh;
    }
    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
        position: absolute;
        left: 0%;
        top: 0%;
        z-index: -1;
    }
    .signin-wrapper {
        background-color: rgba(136, 169, 202, 0.8); 
        width: 358px;
        height: 548px;
        border-radius: 15px;
        padding: 0 50px;
        display: flex;
        flex-direction: column;
        position: relative;
        left: 50%;
        top: 47%;
        transform: translate(-50%, -50%);
        backdrop-filter: blur(5px);
    }
    .header {
        opacity: 0.7;
        font-size: 38px;
        font-weight: bold;
        text-align: center;
        margin-top: 60px;
        margin-bottom: 40px;
        color: #000000;
    }
    .input-title {
        opacity: 0.7;
        font-size: 18px;
        color: #000000;
    }
    .input-item {
        opacity: 0.7;
        display: block;
        width: 100%;
        height: 35px;
        margin-bottom: 20px;
        border: 0;
        padding: 2px;
        padding-left: 10px;
        font-size: 18px;
        outline: none;
        background-color: #577594;
        color: #f8f8f8;
        border-radius: 10px;
        border: 2px solid transparent;
        transition: border-color 0.2s ease;
    }
    .input-item:hover,
    .input-item:focus {
        border-color: #66a1cb;
    }
    .input-item::placeholder {
        color: #c3c3c3;
    }
    .btn {
        opacity: 0.7;
        text-align: center;
        outline: none;
        padding: 10px;
        width: 100%;
        margin-top: 40px;
        background-color: #334e68;
        color: #fff;
    }
    .link {
        opacity: 0.9;
        color: #04073d;
    }
    .msg {
        opacity: 0.7;
        text-align: center;
        line-height: 88px;
        color: #eeeeee;
    }

    .hide {
        color: #04073d00;
    }
    .link-button {
    display: inline-block;
    padding: 6px 12px;
    margin-left: 5px;
    background-color: #334e68;
    color: #ffffff;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease, color 0.2s ease;
    font-weight: bold;
    font-size: 14px;
    }

    .link-button:hover {
    background-color: #577594;
    color: #e0f0ff;
    }
</style>