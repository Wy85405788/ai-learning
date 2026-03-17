<!-- src/App.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-4 sm:p-6 flex justify-center">
    <!-- 主容器：限制最大宽度，水平居中 -->
    <div class="w-full max-w-screen-xl flex flex-col">

      <!-- 标题区域 -->
      <header class="text-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-gray-800 flex items-center justify-center gap-2.5">
          <span class="text-2xl">🤖</span>
          AI 学习进度看板
        </h1>
        <p class="text-gray-600 mt-2 text-sm md:text-base">
          每日任务由 AI 动态生成 · {{ today }}
        </p>
      </header>

      <!-- 主内容：移动竖屏 / 桌面横屏 -->
      <main class="flex flex-col md:flex-row gap-6">
        <!-- 左侧：学习计划 -->
        <section class="w-full md:w-1/3 flex flex-col">
          <div class="bg-white rounded-xl shadow-md p-5 flex-1 flex flex-col">
            <h2 class="font-semibold text-gray-800 text-lg mb-4 flex items-center gap-2">
              <span>📅</span> 本周学习计划
            </h2>
            <ul class="space-y-3 flex-1">
              <li class="flex items-start gap-2.5 text-sm text-gray-700">
                <span class="text-green-500 mt-0.5">✓</span>
                <span>Day 1: 开发环境搭建与项目初始化</span>
              </li>
              <li class="flex items-start gap-2.5 text-sm text-gray-700">
                <span class="text-green-500 mt-0.5">✓</span>
                <span>Day 2: FastAPI 后端任务管理 API</span>
              </li>
              <li class="flex items-start gap-2.5 text-sm text-gray-700">
                <span class="text-blue-600 font-bold mt-0.5">●</span>
                <span class="font-medium">Day 3: Vue + Tailwind 前端界面开发</span>
              </li>
              <li class="flex items-start gap-2.5 text-sm text-gray-700 opacity-70">
                <span class="text-gray-400 mt-0.5">○</span>
                <span>Day 4: 接入 Qwen 大模型生成任务描述</span>
              </li>
              <li class="flex items-start gap-2.5 text-sm text-gray-700 opacity-70">
                <span class="text-gray-400 mt-0.5">○</span>
                <span>Day 5: 部署上线与自动化流程</span>
              </li>
            </ul>
          </div>
        </section>

        <!-- 右侧：今日 AI 任务 -->
        <section class="w-full md:w-2/3 flex flex-col">
          <div class="bg-white rounded-xl shadow-md overflow-hidden flex-1 flex flex-col">
            <div class="px-5 py-3.5 bg-blue-50 border-b border-blue-200">
              <h2 class="font-semibold text-gray-800 text-lg flex items-center gap-2">
                <span class="text-blue-500">🧠</span> 今日 AI 推荐任务
              </h2>
            </div>
            <div class="p-5 flex-1">
              <!-- 加载状态 -->
              <div v-if="loading" class="flex items-center text-gray-500">
                <svg
                  class="animate-spin -ml-1 mr-2 h-5 w-5 text-blue-500"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                AI 正在思考今日任务...
              </div>

              <!-- 有数据 -->
              <div v-else-if="task" class="space-y-4">
                <p class="text-gray-700 leading-relaxed text-base md:text-lg">
                  {{ task.description }}
                </p>
                <div class="flex flex-wrap gap-2">
                  <span class="px-2.5 py-1 bg-green-100 text-green-700 text-xs rounded-full font-medium">
                    状态: {{ task.status }}
                  </span>
                  <span class="px-2.5 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                    创建于 {{ task.created_at }}
                  </span>
                </div>
              </div>

              <!-- 无数据 -->
              <div v-else class="text-gray-500 italic text-sm">
                ⚠️ 未获取到任务数据，请确保后端服务正在运行（http://localhost:8000）
              </div>
            </div>
          </div>
        </section>
      </main>

      <!-- 底部提示 -->
      <footer class="mt-8 text-center text-gray-500 text-sm">
        💡 AI 将根据你的完成情况动态调整后续任务难度与内容
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const today = ref('');
const task = ref(null);
const loading = ref(false);

onMounted(() => {
  const now = new Date();
  today.value = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
  loadTodayTask();
});

const loadTodayTask = async () => {
  loading.value = true;
  try {
    const response = await fetch('http://localhost:8000/task/today');
    if (response.ok) task.value = await response.json();
  } catch (err) {
    console.error('❌ 无法连接到后端:', err);
  } finally {
    loading.value = false;
  }
};
</script>