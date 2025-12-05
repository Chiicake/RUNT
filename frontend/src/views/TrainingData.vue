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
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { Chart, registerables } from 'chart.js'

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
      updateChart()
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

// 切换页码
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    fetchTrainData()
  }
}

// 创建或更新图表
const updateChart = () => {
  // 获取canvas元素
  const ctx = document.getElementById('rewardChart')
  if (!ctx) {
    console.error('Canvas element not found')
    return
  }
  
  // 销毁现有图表实例
  if (rewardChartInstance) {
    rewardChartInstance.destroy()
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
  }
  
  // 计算Y轴上下限
  const yMin = minValue - 1000
  const yMax = maxValue + 1000
  
  // 创建新的图表实例
  rewardChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: '奖励',
          data: rewardData,
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
          data: smoothedRewardData,
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
          title: {
            display: true,
            text: '训练回合',
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
          // 动态调整坐标轴范围
          min: yMin,
          max: yMax,
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
  fetchModelInfo()
  fetchTrainData()
})

// 组件挂载时
onMounted(() => {
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
  
  // 获取数据
  fetchModelInfo()
  fetchTrainData()
})

// 监听训练数据变化，自动更新图表
watch(() => trainData.value, () => {
  updateChart()
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
</style>