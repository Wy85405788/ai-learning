<!-- src/components/TaskCard.vue -->
<template>
  <div
    class="bg-white rounded-xl shadow-md overflow-hidden transition-all duration-300"
    :class="isToday ? 'ring-2 ring-blue-400/50' : ''"
  >
    <div
      class="px-5 py-3 border-b"
      :class="isToday ? 'bg-blue-50 border-blue-200' : 'bg-gray-50 border-gray-200'"
    >
      <div class="flex items-center justify-between">
        <h2 class="font-semibold text-gray-800">{{ date }}</h2>
        <span v-if="isToday" class="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded-full">
          今日
        </span>
      </div>
    </div>

    <div class="p-5">
      <div v-if="loading" class="flex items-center text-gray-500">
        <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        AI 正在生成今日任务...
      </div>

      <div v-else-if="task" class="space-y-3">
        <div class="flex items-start gap-2">
          <span class="text-blue-500 mt-0.5">🧠</span>
          <p class="text-gray-700 leading-relaxed">{{ task.description }}</p>
        </div>
        <div class="flex items-center text-xs text-gray-500 gap-2">
          <span>状态: <span class="font-medium text-green-600">{{ task.status }}</span></span>
          <span>•</span>
          <span>创建于 {{ task.created_at }}</span>
        </div>
      </div>

      <div v-else class="text-gray-500 italic">
        暂无任务数据（请确保 FastAPI 正在运行）
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

const props = defineProps({
  date: { type: String, required: true }
});

const task = ref(null);
const loading = ref(false);

const isToday = computed(() => {
  const now = new Date();
  const localToday = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
  return props.date === localToday;
});

const loadTodayTask = async () => {
  if (!isToday.value) return;
  loading.value = true;
  try {
    const response = await fetch('http://localhost:8000/task/today');
    if (response.ok) {
      task.value = await response.json();
    }
  } catch (error) {
    console.error('加载失败:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadTodayTask();
});
</script>