import { defineStore } from 'pinia';
import { ref, onMounted } from 'vue';
import Home from '../views/Home/index.vue';
import T_home from '../views/Teacher/index.vue'
import M_home from '../views/Manager/index.vue'
import S_home from '../views/Student/index.vue'
// 定义 Store
export const mainStore = defineStore('main', {
  state: () => ({
    ip:'http://10.16.202.197:5000',
    tabs: [
      { name: 'home', title: '首页', component: Home, closable: false }
    ],
    activeTab: 'home',
    tabIndex: 1,
    account: '',
    password: '',
    gender: 'unknown',
    type: 'U',
    name: '请登录',
    token: ''

  }),
  getters: {},
  actions: {
    addTab(title: string, component: any) {
      const newName = `tab${this.tabIndex++}`;
      this.tabs.push({ name: newName, title, component, closable: true });
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
      } else if (this.type === 'M') {
        homeComponent = M_home;
      }

      this.tabs[0] = {
        name: 'home',
        title: '首页',
        component: homeComponent,
        closable: false
      };
    }

  },
});
