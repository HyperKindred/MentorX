<template>
    <div class="container">
        <Cloud />
        <div class="signin-wrapper">
            <h1 class="header">
                注册
            </h1>
            <div class="form-wrapper">
                <h2 class="input-title">手机号</h2>
                <input type="text" v-model="account" placeholder="请输入手机号" class="input-item">
                <h2 class="input-title">姓名</h2>
                <input type="text" v-model="name" placeholder="请输入姓名" class="input-item">
                <h2 class="input-title">密码</h2>
                <input type="password" v-model="password" placeholder="请输入密码" class="input-item">
                <h2 class="input-title">请选择身份</h2>
                <el-select v-model="type" placeholder="身份" style="width: 115px" size="large">
                <el-option label="教师" value="T" />
                <el-option label="学生" value="S" />
                <el-option label="管理员" value="A" />
                </el-select>
                <h2 class="input-title">请选择性别</h2>
                <el-select v-model="gender" placeholder="性别" style="width: 115px" size="large">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
                <el-option label="保密" value="unknow" />
                </el-select>
                <button @click="signUp()" class="btn">
                    注册
                </button>
            </div>
            <div class="msg">
                已有账户？
                <router-link to="/SignIn" class="link">立即登录</router-link>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import { mainStore } from '../../store/index.ts';
import router from "../../router";
import Cloud from '../Cloud.vue';

const store = mainStore();
const account = ref('');
const password = ref('');
const name = ref('');
const type = ref('');
const gender = ref('');



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
        url: `${store.ip}/api/signUp`, 
        data: formData, 
        headers:{'Content-Type': 'multipart/form-data'}}
    )
    .then(response => {
        let responseData = response.data;
        if (responseData.ret === 0) {
        localStorage.setItem('account', account.value);
        localStorage.setItem('name', name.value);
        router.push({path:'/SignIn'})
        } else if(responseData.ret === 1) {
        ElMessage({message: '注册失败：' + responseData.msg, type: 'error', duration: 5 * 1000, grouping: true});
        }
    })
}
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
        height: 628px;
        border-radius: 15px;
        padding: 0 50px;
        display: flex;
        flex-direction: column;
        position: relative;
        left: 50%;
        top: 50%;
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
        color: #ffffff;
    }
    .input-title {
        opacity: 0.7;
        font-size: 18px;
        color: #ffffff;
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
</style>