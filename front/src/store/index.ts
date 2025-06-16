import { defineStore } from 'pinia';
import { ref, onMounted } from 'vue';

// 定义 Store
export const mainStore = defineStore('main', {
  state: () => ({
    ip:'http://10.19.133.87:5000',
  }),
  getters: {},
  actions: {

  },
});
