import { defineStore } from 'pinia';
import { ref, onMounted, markRaw } from 'vue';
import Home from '../views/Home/index.vue';
import T_home from '../views/Teacher/index.vue'
import A_home from '../views/Admin/index.vue'
import S_home from '../views/Student/index.vue'

/**
 * 标签页接口定义
 */
interface Tab {
  name: string;
  title: string;
  component: any;
  closable: boolean;
  props?: any;
}

// 定义 Store
export const mainStore = defineStore('main', {
  state: () => ({
    ip:'http://10.19.130.90:5000',
    tabs: [
      { name: 'home', title: '首页', component: markRaw(Home), closable: false, props: {} }
    ] as Tab[],
    activeTab: 'home',
    tabIndex: 1,
    account: '',
    password: '',
    gender: 'unknown',
    type: 'U',
    name: '请登录',
    token: '',
    theme: localStorage.getItem('theme') || 'dark',
  }),
  getters: {},
  actions: {
    /**
     * 添加新标签页
     * @param title 标签页标题
     * @param component 组件
     * @param props 传递给组件的props（可选）
     */
    addTab(title: string, component: any, props?: any) {
      // 使用唯一的tabIndex生成name，确保每个标签页都有唯一标识
      const newName = `tab${this.tabIndex++}`;
      this.tabs.push({ 
        name: newName, 
        title, 
        component: markRaw(component), 
        closable: true, 
        props: props || {} 
      });
      this.activeTab = newName;
    },
    removeTab(name: string) {
      if (name === 'home') return;
      const index = this.tabs.findIndex(tab => tab.name === name);
      if (index !== -1) {
        this.tabs.splice(index, 1);
        if (this.activeTab === name) {
          this.activeTab = this.tabs[Math.max(0, index - 1)].name;
        }
      }
    },
    getUserInfo(){
      this.account = localStorage.getItem('account') || '';
      this.password = localStorage.getItem('password') || '';
      this.gender = localStorage.getItem('gender') || 'unknown';
      this.type = localStorage.getItem('type') || 'U';
      this.name = localStorage.getItem('name') || '请登录';
      this.token = localStorage.getItem('token') || '';

      let homeComponent = Home;
      if (this.type === 'T') {
        homeComponent = T_home;
      } else if (this.type === 'S') {
        homeComponent = S_home;
      } else if (this.type === 'A') {
        homeComponent = A_home;
      }

      this.tabs[0] = {
        name: 'home',
        title: '首页',
        component: markRaw(homeComponent),
        closable: false,
        props: {}
      };
    },
  },
});
