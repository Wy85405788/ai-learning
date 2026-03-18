<!-- frontend/src/App.vue -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

// 🔥 与 FastAPI 的 Pydantic 模型严格对齐
interface AITask {
  id: number
  description: string
  status: string
  priority: '高' | '中' | '低'
  estimated_hours: number
  tags: string[]
  created_at: string
}

const task = ref<AITask | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const fetchTask = async () => {
  loading.value = true
  error.value = null
  try {
    const { data } = await axios.get<AITask>('http://localhost:8003/task/today')
    task.value = data
  } catch (err) {
    console.error('AI 任务获取失败:', err)
    error.value = '❌ AI 服务暂时不可用，请确保后端正在运行'
  } finally {
    loading.value = false
  }
}

onMounted(fetchTask)
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 py-12 px-4 sm:px-6">
    <div class="max-w-2xl mx-auto">
      <!-- 标题 -->
      <header class="text-center mb-10">
        <h1 class="text-3xl md:text-4xl font-bold text-blue-600 flex items-center justify-center gap-2">
          🤖 AI 今日开发任务
        </h1>
        <p class="text-gray-500 mt-2">由 Qwen3 大模型智能生成</p>
      </header>

      <!-- 主内容区 -->
      <main class="bg-white rounded-2xl shadow-lg overflow-hidden">
        <!-- 加载状态 -->
        <div v-if="loading" class="p-12 text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500 mb-4"></div>
          <p class="text-gray-600">AI 正在思考中...</p>
        </div>

        <!-- 错误状态 -->
        <div v-else-if="error" class="p-8 text-center">
          <p class="text-red-600">{{ error }}</p>
        </div>

        <!-- 成功显示任务 -->
        <div v-else-if="task" class="p-6 md:p-8">
          <div class="space-y-5">
            <!-- 任务描述 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">📝 任务描述</label>
              <p class="text-gray-900 leading-relaxed whitespace-pre-line">{{ task.description }}</p>
            </div>

            <!-- 状态 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">📌 状态</label>
              <span class="inline-block bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full">
                {{ task.status }}
              </span>
            </div>

            <!-- 优先级 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">🔥 优先级</label>
              <span
                class="text-lg font-bold"
                :class="{
                  'text-red-600': task.priority === '高',
                  'text-yellow-600': task.priority === '中',
                  'text-green-600': task.priority === '低'
                }"
              >
                {{ task.priority }}
              </span>
            </div>

            <!-- 预估耗时 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">⏱️ 预估耗时</label>
              <span>{{ task.estimated_hours }} 小时</span>
            </div>

            <!-- 标签 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">🏷️ 标签</label>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="tag in task.tags"
                  :key="tag"
                  class="bg-gray-100 text-gray-800 text-xs px-2.5 py-1 rounded-md"
                >
                  {{ tag }}
                </span>
              </div>
            </div>

            <!-- 日期 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">📅 生成日期</label>
              <span>{{ task.created_at }}</span>
            </div>
          </div>
        </div>
      </main>

      <!-- 刷新按钮 -->
      <button
        @click="fetchTask"
        class="mt-8 w-full py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl transition transform hover:scale-[1.02] active:scale-[0.98] shadow-md"
      >
        🔄 获取新任务
      </button>

      <!-- 底部提示 -->
      <p class="text-center text-gray-400 text-sm mt-10">
        每次刷新都会生成一个全新 AI 任务
      </p>
    </div>
  </div>
</template>
