<template>
  <div class="container">
    <header class="header">
      <h1>算力网络模拟仿真平台</h1>
      <nav class="nav">
        <router-link to="/home" class="nav-link">首页</router-link>
        <router-link to="/model-training" class="nav-link">模型训练</router-link>
        <router-link to="/simulation-demo" class="nav-link">仿真演示</router-link>
        <button @click="handleLogout" class="logout-button">退出登录</button>
      </nav>
    </header>
    
    <main class="main-content">
      <div class="content-header">
        <h2>训练数据详情</h2>
        <button @click="$router.back()" class="back-button">返回</button>
      </div>
      
      <div class="content-card">
        <div v-if="isLoading" class="loading">加载中...</div>
        <div v-else-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        <div v-else>
          <!-- 模型基本信息 -->
          <div class="model-info">
            <h3>模型信息</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">模型ID:</span>
                <span class="info-value">{{ modelInfo.id }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">算法:</span>
                <span class="info-value">{{ modelInfo.algorithm }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">目标回合:</span>
                <span class="info-value">{{ modelInfo.target_episode }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">当前回合:</span>
                <span class="info-value">{{ modelInfo.current_episode }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">状态:</span>
                <span class="info-value">{{ modelInfo.status_text }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">创建时间:</span>
                <span class="info-value">{{ modelInfo.create_time }}</span>
              </div>
            </div>
          </div>
          
          <!-- 训练数据图表 -->
          <div class="chart-section">
            <h3>训练奖励趋势</h3>
            <div class="chart-wrapper">
              <canvas id="rewardChart" ref="rewardChart" class="chart-container"></canvas>
            </div>
          </div>
          
          <!-- 训练数据表格 -->
          <div class="data-table-section">
            <h3>训练数据明细</h3>
            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>回合</th>
                    <th>奖励</th>
                    <th>平滑奖励</th>
                    <th>创建时间</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="data in trainData" :key="data.id">
                    <td>{{ data.episode }}</td>
                    <td>{{ data.reward }}</td>
                    <td>{{ data.smoothed_reward }}</td>
                    <td>{{ data.create_time }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- 分页控件 -->
            <div class="pagination">
              <button 
                @click="changePage(currentPage - 1)" 
                :disabled="currentPage === 1"
                class="page-button"
              >
                上一页
              </button>
              <span class="page-info">
                第 {{ currentPage }} / {{ totalPages }} 页
              </span>
              <button 
                @click="changePage(currentPage + 1)" 
                :disabled="currentPage === totalPages"
                class="page-button"
              >
                下一页
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <!-- 训练分析悬浮按钮 -->
    <div class="train-assistant-container">
      <button 
        class="train-assistant-btn" 
        @click="toggleAssistantWindow"
        :class="{ 'active': isAssistantWindowOpen }"
        title="训练分析"
      >
        <span class="btn-icon">📊</span>
        <span class="btn-text">训练分析</span>
      </button>
      
      <!-- 训练分析悬浮窗 -->
      <div 
        class="assistant-window" 
        v-if="isAssistantWindowOpen"
        :class="{ 'visible': isAssistantWindowOpen }"
      >
        <div class="assistant-header">
          <h3>训练分析</h3>
          <button class="close-btn" @click="toggleAssistantWindow">×</button>
        </div>
        <div class="assistant-content">
          <div v-if="isAnalyzing" class="loading-state">
            <div class="loading-spinner"></div>
            <p>正在分析训练数据...</p>
          </div>
          <div v-else-if="analysisError" class="error-state">
            <p>{{ analysisError }}</p>
            <button class="retry-btn" @click="startAnalysis">重试</button>
          </div>
          <div v-else class="result-state" ref="analysisResult">
            <div v-if="analysisResultText" class="markdown-content" v-html="parsedMarkdown"></div>
            <p v-else class="empty-state">点击"开始分析"按钮获取训练分析结果</p>
          </div>
        </div>
        <div class="assistant-footer">
          <button 
            class="analyze-btn" 
            @click="startAnalysis"
            :disabled="isAnalyzing"
          >
            {{ isAnalyzing ? '分析中...' : '开始分析' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { Chart, registerables } from 'chart.js'
import { marked } from 'marked'

const router = useRouter()
const route = useRoute()

// 模型ID
const modelId = ref(route.params.id)

// 模型信息
const modelInfo = ref({
  id: '',
  algorithm: '',
  target_episode: 0,
  current_episode: 0,
  status_text: '',
  create_time: ''
})

// 训练数据
const trainData = ref([])
const totalPages = ref(1)
const currentPage = ref(1)
const pageSize = ref(20)

// 加载状态和错误信息
const isLoading = ref(false)
const errorMessage = ref('')

// 训练分析相关状态
const isAssistantWindowOpen = ref(false)
const isAnalyzing = ref(false)
const analysisResultText = ref('')
const analysisError = ref('')
const analysisResult = ref(null)
const allTrainData = ref([])

// 注册Chart.js组件
Chart.register(...registerables)

// 图表配置状态
const isSmooth = ref(true)
const chartColors = {
  reward: '#5470c6',
  smoothedReward: '#91cc75'
}

// 图表实例
let rewardChartInstance = null

// 初始化图表
const initRewardChart = () => {
  // 获取canvas元素
  const ctx = document.getElementById('rewardChart')
  if (ctx) {
    // 如果已有实例，先销毁
    if (rewardChartInstance) {
      rewardChartInstance.destroy()
    }
    // 注册Chart.js组件（确保只注册一次）
    if (!Chart.getChart(ctx)) {
      rewardChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [
            {
              label: '奖励',
              data: [],
              borderColor: chartColors.reward,
              backgroundColor: `${chartColors.reward}20`,
              borderWidth: 2,
              fill: true,
              tension: isSmooth.value ? 0.4 : 0,
              pointBackgroundColor: chartColors.reward,
              pointBorderColor: '#fff',
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6
            },
            {
              label: '平滑奖励',
              data: [],
              borderColor: chartColors.smoothedReward,
              backgroundColor: `${chartColors.smoothedReward}20`,
              borderWidth: 2,
              fill: true,
              tension: isSmooth.value ? 0.4 : 0,
              pointBackgroundColor: chartColors.smoothedReward,
              pointBorderColor: '#fff',
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: `模型${modelId.value}训练奖励趋势`,
              font: {
                size: 16,
                weight: 'bold'
              },
              color: '#333'
            },
            legend: {
              display: true,
              position: 'bottom',
              labels: {
                font: {
                  size: 12
                },
                color: '#666'
              }
            },
            tooltip: {
              mode: 'index',
              intersect: false,
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              titleColor: '#333',
              bodyColor: '#666',
              borderColor: '#ddd',
              borderWidth: 1,
              padding: 12,
              cornerRadius: 6,
              callbacks: {
                title: function(context) {
                  return `回合: ${context[0].label}`;
                },
                label: function(context) {
                  return `${context.dataset.label}: ${context.parsed.y.toFixed(6)}`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: {
                color: '#f0f0f0',
                drawBorder: false
              },
              ticks: {
                color: '#666',
                font: {
                  size: 11
                },
                maxRotation: 45,
                minRotation: 45
              }
            },
            y: {
              title: {
                display: true,
                text: '奖励值',
                color: '#666',
                font: {
                  size: 14
                }
              },
              grid: {
                color: '#f0f0f0',
                drawBorder: false
              },
              ticks: {
                color: '#666',
                font: {
                  size: 11
                },
                // 使用科学计数法显示大数值
                callback: function(value) {
                  // 如果数值绝对值大于1000或小于0.001，使用科学计数法
                  if (Math.abs(value) >= 1000 || Math.abs(value) < 0.001) {
                    return value.toExponential(2);
                  }
                  // 否则使用普通格式，保留2位小数
                  return value.toFixed(2);
                },
                // 设置最大刻度数
                maxTicksLimit: 8,
                // 使用Chart.js内置的自动刻度算法
                autoSkip: true,
                autoSkipPadding: 10
              }
            }
          },
          interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
          },
          animation: {
            duration: 1000,
            easing: 'easeInOutQuart'
          }
        }
      })
    }
  }
}

// 更新图表
const updateRewardChart = () => {
  if (!rewardChartInstance) {
    initRewardChart()
    return
  }
  
  // 准备数据
  const labels = trainData.value.map(item => item.episode)
  const rewardData = trainData.value.map(item => item.reward)
  const smoothedRewardData = trainData.value.map(item => item.smoothed_reward)
  
  // 计算Y轴范围
  let minValue = Infinity
  let maxValue = -Infinity
  
  if (trainData.value.length > 0) {
    // 获取所有奖励值
    const allRewards = [...rewardData, ...smoothedRewardData]
    minValue = Math.min(...allRewards)
    maxValue = Math.max(...allRewards)
    
    // 确保Y轴有合理的范围
    const range = maxValue - minValue
    if (range === 0) {
      minValue -= 1
      maxValue += 1
    } else {
      // 添加10%的边距
      const margin = range * 0.1
      minValue -= margin
      maxValue += margin
    }
  } else {
    // 如果没有数据，设置默认范围
    minValue = 0
    maxValue = 100
  }
  
  // 更新图表数据和选项
  rewardChartInstance.data.labels = labels
  rewardChartInstance.data.datasets[0].data = rewardData
  rewardChartInstance.data.datasets[1].data = smoothedRewardData
  rewardChartInstance.options.scales.y.min = minValue
  rewardChartInstance.options.scales.y.max = maxValue
  
  // 更新图表
  rewardChartInstance.update()
}

// 获取模型信息
const fetchModelInfo = async () => {
  try {
    isLoading.value = true
    errorMessage.value = ''
    
    // 从模型列表中获取模型信息
    const response = await axios.get(`http://127.0.0.1:8000/models/?page=1&page_size=100`)
    
    if (response.data.status === 'success') {
      const models = response.data.data.models
      const model = models.find(m => m.id === parseInt(modelId.value))
      if (model) {
        modelInfo.value = model
      } else {
        errorMessage.value = '未找到该模型信息'
      }
    } else {
      errorMessage.value = response.data.message || '获取模型信息失败'
    }
  } catch (error) {
    console.error('获取模型信息失败:', error)
    errorMessage.value = `获取模型信息失败: ${error.message}`
  } finally {
    isLoading.value = false
  }
}

// 获取所有训练数据，用于训练分析
const fetchAllTrainData = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/models/${modelId.value}/train-data/`, {
      params: {
        page: 1,
        page_size: 10000 // 足够大的页码，确保获取所有数据
      }
    })
    
    if (response.data.status === 'success') {
      allTrainData.value = response.data.data.train_data
      return true
    }
    return false
  } catch (error) {
    console.error('获取所有训练数据失败:', error)
    return false
  }
}

// 获取训练数据
const fetchTrainData = async () => {
  try {
    isLoading.value = true
    errorMessage.value = ''
    
    const response = await axios.get(`http://127.0.0.1:8000/models/${modelId.value}/train-data/`, {
      params: {
        page: currentPage.value,
        page_size: pageSize.value
      }
    })
    
    if (response.data.status === 'success') {
      const data = response.data.data
      trainData.value = data.train_data
      totalPages.value = data.total_pages
      
      // 更新图表
      updateRewardChart()
    } else {
      errorMessage.value = response.data.message || '获取训练数据失败'
    }
  } catch (error) {
    console.error('获取训练数据失败:', error)
    errorMessage.value = `获取训练数据失败: ${error.message}`
  } finally {
    isLoading.value = false
  }
}

// 切换助手窗口显示状态
const toggleAssistantWindow = () => {
  isAssistantWindowOpen.value = !isAssistantWindowOpen.value
  if (isAssistantWindowOpen.value) {
    // 每次打开窗口时清空之前的结果
    analysisResultText.value = ''
    analysisError.value = ''
    // 获取所有训练数据
    fetchAllTrainData()
  }
}

// 解析Markdown内容
const parsedMarkdown = computed(() => {
  if (!analysisResultText.value) return ''
  return marked(analysisResultText.value)
})

// 开始训练分析
const startAnalysis = async () => {
  if (!modelId.value) {
    analysisError.value = '请先选择一个模型'
    return
  }
  
  isAnalyzing.value = true
  analysisResultText.value = ''
  analysisError.value = ''
  
  // 如果还没有获取所有训练数据，先获取
  if (allTrainData.value.length === 0) {
    const success = await fetchAllTrainData()
    if (!success) {
      analysisError.value = '获取训练数据失败'
      isAnalyzing.value = false
      return
    }
  }
  
  try {
    // 调用 /trainingassistant 接口获取训练分析
    const response = await fetch('http://127.0.0.1:8000/trainingassistent/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        hyperparameters: {
          algorithm: modelInfo.value.algorithm,
          target_episode: modelInfo.value.target_episode,
          // 从模型信息中获取其他超参数
          task_size_average: 0,
          task_comsumption_average: 0,
          task_time_average: 0,
          task_arrival_rate: 0,
          n_UE: 5,
          UE_computation_capacity: 0,
          MEC_computation_capacity: 0,
          seed: 0,
          learning_rate: 0,
          batch_size: 0,
          buffer_size: 0,
          gamma: 0
        },
        rewards: allTrainData.value.map(item => item.reward)
      })
    })
    
    if (!response.ok) {
      throw new Error('分析请求失败')
    }
    
    // 处理流式响应
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      
      // 将新数据添加到结果中
      analysisResultText.value += decoder.decode(value)
      
      // 自动滚动到底部
      if (analysisResult.value) {
        analysisResult.value.scrollTop = analysisResult.value.scrollHeight
      }
    }
  } catch (error) {
    console.error('训练分析失败:', error)
    analysisError.value = `训练分析失败: ${error.message}`
  } finally {
    isAnalyzing.value = false
  }
}

// 切换页码
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    fetchTrainData()
  }
}

// 监听窗口大小变化，调整图表大小
const handleResize = () => {
  if (rewardChartInstance) {
    rewardChartInstance.resize()
  }
}

// 退出登录
const handleLogout = () => {
  localStorage.removeItem('isLoggedIn')
  router.push('/login')
}

// 监听模型ID变化
watch(() => route.params.id, (newId) => {
  modelId.value = newId
  currentPage.value = 1
  // 重新初始化图表
  initRewardChart()
  fetchModelInfo()
  fetchTrainData()
})

// 组件挂载时
onMounted(() => {
  // 初始化图表
  initRewardChart()
  
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
  
  // 获取数据
  fetchModelInfo()
  fetchTrainData()
})

// 监听训练数据变化，自动更新图表
watch(() => trainData.value, () => {
  updateRewardChart()
}, { deep: true })

// 组件卸载时
onUnmounted(() => {
  // 销毁图表实例
  if (rewardChartInstance) {
    rewardChartInstance.destroy()
  }
  
  // 移除事件监听
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.header {
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

.header h1 {
  font-size: 1.5rem;
  color: #333;
  margin: 0;
}

.nav {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  padding: 0.5rem 1rem;
  color: #666;
  text-decoration: none;
  border-radius: 4px;
  transition: all 0.3s;
}

.nav-link:hover {
  color: #409eff;
  background-color: #ecf5ff;
}

.nav-link.active {
  color: #409eff;
  background-color: #ecf5ff;
  font-weight: 500;
}

.logout-button {
  padding: 0.5rem 1rem;
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-button:hover {
  background-color: #f78989;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.content-header h2 {
  color: #333;
  margin: 0;
}

.back-button {
  padding: 0.75rem 1.5rem;
  background-color: #909399;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: #a6a9ad;
}

.content-card {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error-message {
  padding: 1rem;
  background-color: #fef0f0;
  color: #f56c6c;
  border-radius: 4px;
  margin-bottom: 1rem;
}

/* 模型信息样式 */
.model-info {
  margin-bottom: 2rem;
}

.model-info h3 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  background-color: #fafafa;
  padding: 1.5rem;
  border-radius: 4px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-size: 0.85rem;
  color: #909399;
}

.info-value {
  font-size: 1rem;
  color: #333;
  font-weight: 500;
}

/* 图表样式 */
.chart-section {
  margin-bottom: 2rem;
}

.chart-section h3 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
}

.chart-wrapper {
  position: relative;
}

.chart-container {
  width: 100%;
  height: 400px;
  border-radius: 4px;
  background-color: #fafafa;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.chart-controls {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
  justify-content: flex-end;
}

.control-button {
  padding: 0.5rem 1rem;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.control-button:hover {
  background-color: #66b1ff;
}

/* 数据表格样式 */
.data-table-section h3 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
}

.table-container {
  overflow-x: auto;
  margin-bottom: 1.5rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.data-table th,
.data-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
}

.data-table th {
  background-color: #fafafa;
  color: #606266;
  font-weight: 500;
}

.data-table tr:hover {
  background-color: #f5f7fa;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.page-button {
  padding: 0.5rem 1rem;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.page-button:hover:not(:disabled) {
  background-color: #66b1ff;
}

.page-button:disabled {
  background-color: #a0cfff;
  cursor: not-allowed;
}

.page-info {
  color: #666;
  font-size: 0.9rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .info-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .chart-container {
    height: 300px;
  }
}

/* 训练分析样式 */
.train-assistant-container {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 1rem;
}

.train-assistant-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.train-assistant-btn:hover {
  background-color: #66b1ff;
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.4);
  transform: translateY(-2px);
}

.train-assistant-btn.active {
  background-color: #67c23a;
  box-shadow: 0 6px 16px rgba(103, 194, 58, 0.4);
}

.train-assistant-btn .btn-icon {
  font-size: 1.25rem;
}

.train-assistant-btn .btn-text {
  display: inline-block;
}

/* 响应式：小屏幕上只显示图标 */
@media (max-width: 768px) {
  .train-assistant-btn .btn-text {
    display: none;
  }
  
  .train-assistant-btn {
    padding: 1rem;
    border-radius: 50%;
  }
}

/* 悬浮窗样式 */
.assistant-window {
  width: 400px;
  max-width: 90vw;
  max-height: 600px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  opacity: 0;
  transform: translateY(20px) scale(0.95);
  transition: all 0.3s ease;
  pointer-events: none;
}

.assistant-window.visible {
  opacity: 1;
  transform: translateY(0) scale(1);
  pointer-events: all;
}

.assistant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background-color: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
  border-radius: 12px 12px 0 0;
}

.assistant-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.assistant-header .close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #909399;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.assistant-header .close-btn:hover {
  background-color: #ecf5ff;
  color: #409eff;
}

.assistant-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  background-color: white;
  font-size: 0.9rem;
  line-height: 1.6;
  text-align: left;
}

.assistant-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: #333;
}

.assistant-footer {
  padding: 1rem 1.5rem;
  background-color: #f5f7fa;
  border-top: 1px solid #ebeef5;
  border-radius: 0 0 12px 12px;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  padding: 2rem;
  color: #606266;
  text-align: left;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #ebeef5;
  border-top: 4px solid #409eff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
  align-self: center;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 错误状态 */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  padding: 2rem;
  color: #f56c6c;
  text-align: left;
}

.error-state .retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  align-self: flex-start;
}

.error-state .retry-btn:hover {
  background-color: #66b1ff;
}

/* 结果状态 */
.result-state {
  max-height: 400px;
  overflow-y: auto;
  text-align: left;
}

.result-state .empty-state {
  color: #909399;
  text-align: left;
  padding: 2rem;
  margin: 0;
}

/* 分析按钮 */
.analyze-btn {
  padding: 0.75rem 1.5rem;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.analyze-btn:hover:not(:disabled) {
  background-color: #66b1ff;
  transform: translateY(-1px);
}

.analyze-btn:disabled {
  background-color: #a0cfff;
  cursor: not-allowed;
  transform: none;
}

/* Markdown内容样式 */
.markdown-content {
  color: #333;
  line-height: 1.8;
}

/* 标题样式 */
.markdown-content h1 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 1.5rem 0 1rem;
  color: #2c3e50;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 0.5rem;
}

.markdown-content h2 {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 1.2rem 0 0.8rem;
  color: #2c3e50;
}

.markdown-content h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 1rem 0 0.6rem;
  color: #2c3e50;
}

.markdown-content h4, .markdown-content h5, .markdown-content h6 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0.8rem 0 0.5rem;
  color: #2c3e50;
}

/* 段落样式 */
.markdown-content p {
  margin: 0.8rem 0;
}

/* 列表样式 */
.markdown-content ul, .markdown-content ol {
  margin: 0.8rem 0;
  padding-left: 1.5rem;
}

.markdown-content li {
  margin: 0.3rem 0;
}

.markdown-content ul li {
  list-style-type: disc;
}

.markdown-content ol li {
  list-style-type: decimal;
}

/* 粗体和斜体 */
.markdown-content strong {
  font-weight: 600;
  color: #2c3e50;
}

.markdown-content em {
  font-style: italic;
  color: #666;
}

/* 代码样式 */
.markdown-content code {
  background-color: #f5f5f5;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.85rem;
  color: #e74c3c;
}

.markdown-content pre {
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1rem 0;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.85rem;
  line-height: 1.5;
}

.markdown-content pre code {
  background-color: transparent;
  padding: 0;
  border-radius: 0;
  color: #333;
}

/* 链接样式 */
.markdown-content a {
  color: #409eff;
  text-decoration: none;
  transition: color 0.3s ease;
}

.markdown-content a:hover {
  color: #66b1ff;
  text-decoration: underline;
}

/* 引用样式 */
.markdown-content blockquote {
  margin: 1rem 0;
  padding: 0.8rem 1rem;
  background-color: #f0f8ff;
  border-left: 4px solid #409eff;
  color: #666;
  border-radius: 0 4px 4px 0;
}

.markdown-content blockquote p {
  margin: 0;
}

/* 分割线样式 */
.markdown-content hr {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 1.5rem 0;
}

/* 表格样式 */
.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.9rem;
}

.markdown-content th, .markdown-content td {
  padding: 0.6rem 0.8rem;
  text-align: left;
  border: 1px solid #e0e0e0;
}

.markdown-content th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #2c3e50;
}

.markdown-content tr:nth-child(even) {
  background-color: #fafafa;
}

/* 滚动条样式 */
.assistant-content::-webkit-scrollbar,
.result-state::-webkit-scrollbar {
  width: 6px;
}

.assistant-content::-webkit-scrollbar-track,
.result-state::-webkit-scrollbar-track {
  background-color: #f5f7fa;
  border-radius: 3px;
}

.assistant-content::-webkit-scrollbar-thumb,
.result-state::-webkit-scrollbar-thumb {
  background-color: #c0c4cc;
  border-radius: 3px;
}

.assistant-content::-webkit-scrollbar-thumb:hover,
.result-state::-webkit-scrollbar-thumb:hover {
  background-color: #909399;
}

/* 响应式悬浮窗 */
@media (max-width: 480px) {
  .assistant-window {
    width: 95vw;
    max-height: 70vh;
  }
  
  .train-assistant-container {
    bottom: 1rem;
    right: 1rem;
  }
}
</style>