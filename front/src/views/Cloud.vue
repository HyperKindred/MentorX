<script>
import { onMounted, onBeforeUnmount, ref } from 'vue';
import * as THREE from 'three'; // 导入 Three.js
import CLOUDS from 'vanta/src/vanta.clouds'; // 导入动态样式逻辑

export default {
    setup() {
        // 使用 `ref` 创建响应式 DOM 引用
        const vantaRef = ref(null);
        let vantaEffect = null;

        // 在组件挂载时初始化 Vanta 动画
        onMounted(() => {
            vantaEffect = CLOUDS({
                el: vantaRef.value, // 使用 Vue 3 的 `ref` 值
                THREE: THREE,
                mouseControls: true,
                touchControls: true,
                gyroControls: false,
                minHeight: 200.00,
                minWidth: 200.00
            });
        });

        // 在组件卸载前销毁 Vanta 动画
        onBeforeUnmount(() => {
            if (vantaEffect) {
                vantaEffect.destroy();
                vantaEffect = null;
            }
        });

        return {
            vantaRef,
        };
    },
};
</script>

<template>
    <!-- 设置覆盖背景的容器 -->
    <div ref="vantaRef" class="vanta-background"></div>
</template>

<style scoped>
.vanta-background {
    position: absolute;
    /* 让背景定位相对于父级元素 */
    top: 0;
    left: 0;
    width: 100%;
    /* 覆盖整个父级元素 */
    height: 100%;
    /* 覆盖整个父级元素 */
    z-index: -1;
    /* 将背景放在内容后面 */
}
</style>