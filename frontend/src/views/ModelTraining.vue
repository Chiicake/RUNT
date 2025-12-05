<template>
  <div class="container">
    <header class="header">
      <h1>算力网络模拟仿真平台</h1>
      <nav class="nav">
        <router-link to="/home" class="nav-link">首页</router-link>
        <router-link to="/model-training" class="nav-link active">模型训练</router-link>
        <router-link to="/simulation-demo" class="nav-link">仿真演示</router-link>
        <button @click="handleLogout" class="logout-button">退出登录</button>
      </nav>
    </header>
    
    <main class="main-content">
      <h2>模型训练管理</h2>
      
      <div class="content-grid">
        <!-- 参数配置表单 -->
        <div class="content-card">
          <h3>参数配置</h3>
          <form @submit.prevent="handleTrain" class="train-form">
            <div class="form-row">
              <div class="form-group">
                <label for="algorithm">算法名称 *</label>
                <select id="algorithm" v-model="trainParams.algorithm" required class="form-input">
                  <option value="SAC">SAC</option>
                </select>
              </div>
              <div class="form-group">
                <label for="target_episode">目标训练回合数 *</label>
                <input type="number" id="target_episode" v-model.number="trainParams.target_episode" required min="1" class="form-input">
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="task_size_average">任务平均大小</label>
                <input type="number" id="task_size_average" v-model.number="trainParams.task_size_average" min="0" step="0.0001" class="form-input">
              </div>
              <div class="form-group">
                <label for="task_comsumption_average">任务平均消耗</label>
                <input type="number" id="task_comsumption_average" v-model.number="trainParams.task_comsumption_average" min="0" step="0.0001" class="form-input">
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="task_time_average">任务平均耗时</label>
                <input type="number" id="task_time_average" v-model.number="trainParams.task_time_average" min="0" step="0.0001" class="form-input">
              </div>
              <div class="form-group">
                <label for="task_arrival_rate">任务到达率</label>
                <input type="number" id="task_arrival_rate" v-model.number="trainParams.task_arrival_rate" min="0" step="0.0001" class="form-input">
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="n_UE">用户设备数量</label>
                <input type="number" id="n_UE" v-model.number="trainParams.n_UE" min="1" class="form-input">
              </div>
              <div class="form-group">
                <label for="seed">随机种子</label>
                <input type="number" id="seed" v-model.number="trainParams.seed" min="0" class="form-input">
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="UE_computation_capacity">UE计算能力</label>
                <input type="number" id="UE_computation_capacity" v-model.number="trainParams.UE_computation_capacity" min="0" step="0.01" class="form-input">
              </div>
              <div class="form-group">
                <label for="MEC_computation_capacity">MEC计算能力</label>
                <input type="number" id="MEC_computation_capacity" v-model.number="trainParams.MEC_computation_capacity" min="0" step="0.01" class="form-input">
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="learning_rate">学习率</label>
                <input type="number" id="learning_rate" v-model.number="trainParams.learning_rate" min="0" step="0.000001" class="form-input">
              </div>
              <div class="form-group">
                <label for="batch_size">批次大小</label>
                <input type="number" id="batch_size" v-model.number="trainParams.batch_size" min="1" class="form-input">
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="gamma">折扣因子γ</label>
                <input type="number" id="gamma" v-model.number="trainParams.gamma" min="0" max="1" step="0.000001" class="form-input">
              </div>
            </div>
            
            <div class="form-actions">
              <button type="submit" class="submit-button" :disabled="isLoading || trainingStatus.isTraining">
                {{ isLoading ? '提交中...' : (trainingStatus.isTraining ? '训练中...' : '开始训练') }}
              </button>
              <button type="button" @click="resetForm" class="reset-button">重置参数</button>
              <button type="button" v-if="trainingStatus.isTraining" @click="handleCancel" class="cancel-button">
                取消训练
              </button>
            </div>
          </form>
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </div>
        
        <!-- 训练状态和奖励展示 -->
        <div class="content-card">
          <h3>训练状态</h3>
          <div class="status-section">
            <div class="status-item">
              <span class="status-label">当前状态:</span>
              <span class="status-value" :class="trainingStatus.isTraining ? 'status-training' : 'status-idle'">
                {{ trainingStatus.isTraining ? '训练中' : '空闲' }}
              </span>
            </div>
            <div class="status-item">
              <span class="status-label">当前模型ID:</span>
              <span class="status-value">{{ trainingStatus.currentModelId || '无' }}</span>
            </div>
            <div class="status-item">
              <span class="status-label">当前回合:</span>
              <span class="status-value">{{ trainingStatus.currentEpisode || 0 }} / {{ trainingStatus.targetEpisode || 0 }}</span>
            </div>
            <div class="status-item">
              <span class="status-label">最新奖励:</span>
              <span class="status-value">{{ latestReward || 'N/A' }}</span>
            </div>
          </div>
          
          <!-- 奖励可视化图表 -->
          <div class="chart-section">
            <h4>奖励变化趋势</h4>
            <div id="rewardChart" ref="rewardChart" class="chart-container"></div>
          </div>
        </div>
      </div>
      
      <!-- 训练历史记录 -->
      <div class="content-card">
        <h3>训练历史记录</h3>
        <div class="history-section">
          <div v-if="isLoadingHistory" class="loading">加载历史记录中...</div>
          <div v-else-if="modelHistory.length === 0" class="empty-state">暂无训练历史记录</div>
          <table v-else class="history-table">
            <thead>
              <tr>
                <th>模型ID</th>
                <th>算法</th>
                <th>目标回合</th>
                <th>当前回合</th>
                <th>状态</th>
                <th>创建时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="model in modelHistory" :key="model.id">
                <td>{{ model.id }}</td>
                <td>{{ model.algorithm }}</td>
                <td>{{ model.target_episode }}</td>
                <td>{{ model.current_episode }}</td>
                <td><span :class="`status-badge ${model.status_text === '训练中' ? 'status-training' : 'status-completed'}`">{{ model.status_text }}</span></td>
                <td>{{ model.create_time }}</td>
                <td>
                  <button @click="viewTrainingData(model.id)" class="view-button">查看训练数据</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import * as echarts from 'echarts'

const router = useRouter()

// 训练参数
const trainParams = reactive({
  algorithm: 'SAC',
  target_episode: 100,
  // 从config.py获取的默认值
  task_size_average: 450,
  task_comsumption_average: 4500,
  task_time_average: 5,
  task_arrival_rate: 0.3,
  n_UE: 5,
  UE_computation_capacity: 1000,
  MEC_computation_capacity: 5000,
  seed: 777,
  // 算法相关参数
  learning_rate: 0.003,
  batch_size: 64,
  gamma: 0.99
})

// 训练状态
const trainingStatus = reactive({
  isTraining: false,
  currentModelId: null,
  currentEpisode: 0,
  targetEpisode: 0
})

// 加载状态
const isLoading = ref(false)
const isLoadingHistory = ref(false)

// 错误信息
const errorMessage = ref('')

// 奖励数据
const rewardData = ref([])
const latestReward = ref(null)

// 模型历史记录
const modelHistory = ref([])

// 图表实例
let rewardChartInstance = null
let pollingInterval = null

// 退出登录
const handleLogout = () => {
  localStorage.removeItem('isLoggedIn')
  router.push('/login')
}

// 重置表单
const resetForm = () => {
  Object.assign(trainParams, {
    algorithm: 'SAC',
    target_episode: 100,
    // 从config.py获取的默认值
    task_size_average: 450,
    task_comsumption_average: 4500,
    task_time_average: 5,
    task_arrival_rate: 0.3,
    n_UE: 5,
    UE_computation_capacity: 1000,
    MEC_computation_capacity: 5000,
    seed: 777,
    // 算法相关参数
    learning_rate: 0.003,
    batch_size: 64,
    gamma: 0.99
  })
  errorMessage.value = ''
}

// 开始训练
const handleTrain = async () => {
  try {
    isLoading.value = true
    errorMessage.value = ''
    
    // 过滤掉null值
    const params = {}
    for (const [key, value] of Object.entries(trainParams)) {
      if (value !== null && value !== '') {
        params[key] = value
      }
    }
    
    // 调用训练接口
    const response = await axios.post('http://127.0.0.1:8000/train/', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    
    if (response.data.status === 'success') {
      const modelId = response.data.id
      trainingStatus.isTraining = true
      trainingStatus.currentModelId = modelId
      trainingStatus.targetEpisode = trainParams.target_episode
      trainingStatus.currentEpisode = 0
      
      // 初始化奖励数据
      rewardData.value = []
      latestReward.value = null
      updateRewardChart()
      
      // 开始轮询奖励数据
      startPolling(modelId)
      
      // 刷新历史记录
      fetchModelHistory()
    } else {
      errorMessage.value = response.data.message || '训练任务创建失败'
    }
  } catch (error) {
    console.error('训练失败:', error)
    errorMessage.value = `训练任务创建失败: ${error.message}`
  } finally {
    isLoading.value = false
  }
}

// 取消训练
const handleCancel = () => {
  if (confirm('确定要取消当前训练任务吗？')) {
    stopPolling()
    trainingStatus.isTraining = false
    trainingStatus.currentModelId = null
    trainingStatus.currentEpisode = 0
    trainingStatus.targetEpisode = 0
  }
}

// 开始轮询奖励数据
const startPolling = (modelId) => {
  // 清除之前的轮询
  stopPolling()
  
  // 每10秒轮询一次
  pollingInterval = setInterval(async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/models/${modelId}/train-data/`)
      
      if (response.data.status === 'success') {
        const trainData = response.data.data.train_data
        if (trainData && trainData.length > 0) {
          // 获取最新的训练数据
          const latestData = trainData[trainData.length - 1]
          latestReward.value = latestData.reward
          
          // 更新当前回合
          trainingStatus.currentEpisode = latestData.episode
          
          // 添加到奖励数据中（去重）
          const exists = rewardData.value.some(item => item.episode === latestData.episode)
          if (!exists) {
            rewardData.value.push({
              episode: latestData.episode,
              reward: latestData.reward,
              smoothed_reward: latestData.smoothed_reward
            })
            
            // 更新图表
            updateRewardChart()
          }
          
          // 检查是否训练完成
          if (latestData.episode >= trainingStatus.targetEpisode) {
            stopPolling()
            trainingStatus.isTraining = false
          }
        }
      }
    } catch (error) {
      console.error('轮询奖励数据失败:', error)
    }
  }, 2000)
}

// 停止轮询
const stopPolling = () => {
  if (pollingInterval) {
    clearInterval(pollingInterval)
    pollingInterval = null
  }
}

// 获取模型历史记录
const fetchModelHistory = async () => {
  try {
    isLoadingHistory.value = true
    const response = await axios.get('http://127.0.0.1:8000/models/')
    
    if (response.data.status === 'success') {
      modelHistory.value = response.data.data.models
    }
  } catch (error) {
    console.error('获取模型历史记录失败:', error)
  } finally {
    isLoadingHistory.value = false
  }
}

// 查看训练数据
const viewTrainingData = (modelId) => {
  router.push(`/training-data/${modelId}`)
}

// 初始化奖励图表
const initRewardChart = () => {
  const chartDom = document.getElementById('rewardChart')
  if (chartDom) {
    rewardChartInstance = echarts.init(chartDom)
    updateRewardChart()
  }
}

// 更新奖励图表
const updateRewardChart = () => {
  if (!rewardChartInstance) return
  
  // 计算Y轴范围
  let minValue = Infinity
  let maxValue = -Infinity
  
  if (rewardData.value.length > 0) {
    // 获取所有奖励值
    const allRewards = [...rewardData.value.map(item => item.reward), ...rewardData.value.map(item => item.smoothed_reward)]
    minValue = Math.min(...allRewards)
    maxValue = Math.max(...allRewards)
  }
  
  // 计算Y轴上下限
  const yMin = minValue - 1000
  const yMax = maxValue + 1000
  
  const option = {
    title: {
      text: '奖励变化趋势',
      left: 'center',
      textStyle: {
        fontSize: 14
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        let result = `回合: ${params[0].name}<br/>`
        params.forEach(param => {
          result += `${param.seriesName}: ${param.value.toFixed(4)}<br/>`
        })
        return result
      }
    },
    legend: {
      data: ['奖励', '平滑奖励'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: rewardData.value.map(item => item.episode),
      name: '回合数',
      nameLocation: 'middle',
      nameGap: 30
    },
    yAxis: {
      type: 'value',
      name: '奖励值',
      nameLocation: 'middle',
      nameGap: 50,
      min: yMin,
      max: yMax
    },
    series: [
      {
        name: '奖励',
        type: 'line',
        data: rewardData.value.map(item => item.reward),
        smooth: true,
        lineStyle: {
          color: '#5470c6'
        },
        itemStyle: {
          color: '#5470c6'
        }
      },
      {
        name: '平滑奖励',
        type: 'line',
        data: rewardData.value.map(item => item.smoothed_reward),
        smooth: true,
        lineStyle: {
          color: '#91cc75'
        },
        itemStyle: {
          color: '#91cc75'
        }
      }
    ]
  }
  
  rewardChartInstance.setOption(option)
}

// 监听窗口大小变化， resize图表
const handleResize = () => {
  if (rewardChartInstance) {
    rewardChartInstance.resize()
  }
}

// 组件挂载时
onMounted(() => {
  // 初始化图表
  initRewardChart()
  
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
  
  // 获取模型历史记录
  fetchModelHistory()
})

// 组件卸载时
onUnmounted(() => {
  // 停止轮询
  stopPolling()
  
  // 销毁图表实例
  if (rewardChartInstance) {
    rewardChartInstance.dispose()
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

.main-content h2 {
  color: #333;
  margin-bottom: 1.5rem;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.content-card {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.content-card h3 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
}

.content-card h4 {
  color: #666;
  margin: 1rem 0;
  font-size: 1rem;
}

/* 表单样式 */
.train-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.9rem;
  color: #666;
}

.form-input {
  padding: 0.75rem;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #409eff;
}

.form-input:required:invalid {
  border-color: #f56c6c;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
}

.submit-button {
  padding: 0.75rem 1.5rem;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover:not(:disabled) {
  background-color: #66b1ff;
}

.submit-button:disabled {
  background-color: #a0cfff;
  cursor: not-allowed;
}

.reset-button {
  padding: 0.75rem 1.5rem;
  background-color: #909399;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.reset-button:hover {
  background-color: #a6a9ad;
}

.cancel-button {
  padding: 0.75rem 1.5rem;
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-button:hover {
  background-color: #f78989;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #fef0f0;
  color: #f56c6c;
  border-radius: 4px;
  font-size: 0.9rem;
}

/* 状态样式 */
.status-section {
  background-color: #fafafa;
  padding: 1.5rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}

.status-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  font-size: 0.9rem;
}

.status-item:last-child {
  margin-bottom: 0;
}

.status-label {
  color: #666;
}

.status-value {
  color: #333;
  font-weight: 500;
}

.status-training {
  color: #67c23a;
}

.status-idle {
  color: #909399;
}

.status-completed {
  color: #e6a23c;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: 500;
}

/* 图表样式 */
.chart-section {
  margin-top: 1.5rem;
}

.chart-container {
  width: 100%;
  height: 300px;
}

/* 历史记录样式 */
.history-section {
  overflow-x: auto;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #909399;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.history-table th,
.history-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
}

.history-table th {
  background-color: #fafafa;
  color: #606266;
  font-weight: 500;
}

.history-table tr:hover {
  background-color: #f5f7fa;
}

.view-button {
  padding: 0.375rem 0.75rem;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: background-color 0.3s;
}

.view-button:hover {
  background-color: #66b1ff;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-wrap: wrap;
  }
}
</style>