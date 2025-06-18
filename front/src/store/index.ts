import { defineStore } from 'pinia';
import { ref, onMounted } from 'vue';
import Home from '../views/Home/index.vue';
import T_chapter from '../views/Teacher/Chapter/index.vue'
import T_exercises from '../views/Teacher/Exercises/index.vue'
import T_exercise from '../views/Teacher/Exercise/index.vue'
// 定义 Store
export const mainStore = defineStore('main', {
  state: () => ({
    ip:'http://10.16.206.102:5000',
    tabs: [
      { name: 'home', title: '首页', component: Home, closable: false }
    ],
    activeTab: 'home',
    tabIndex: 1,
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
    }

  },
});
