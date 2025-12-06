<template>
  <div class="container">
    <header class="header">
      <h1>算力网络模拟仿真平台</h1>
      <nav class="nav">
        <router-link to="/home" class="nav-link">首页</router-link>
        <router-link to="/model-training" class="nav-link">模型训练</router-link>
        <router-link to="/simulation-demo" class="nav-link active">仿真演示</router-link>
        <button @click="handleLogout" class="logout-button">退出登录</button>
      </nav>
    </header>
    
    <main class="main-content">
      <h2>仿真演示</h2>
      
      <!-- 顶部配置区域 -->
      <section class="section model-section">
        <h3>模型选择</h3>
        <div class="model-selection-container">
          <!-- 左侧：模型可视化区域 -->
          <div class="visualization-area">
            <h4>系统可视化</h4>
            <div class="visualization-container" ref="visualizationRef">
              <!-- 基站 (BS) -->
              <div class="visualization-element bs-element" :style="bsStyle">
                <img src="../runtassets/BS.png" alt="基站" class="element-image">
                <div class="element-label">基站</div>
              </div>
              
              <!-- UAV -->
              <div class="visualization-element uav-element" :style="uavStyle">
                <img src="../runtassets/UAV.png" alt="无人机" class="element-image">
                <div class="element-label">UAV</div>
              </div>
              
              <!-- 用户设备 (UEs) -->
              <div 
                v-for="(ue, index) in ueElements" 
                :key="index" 
                class="visualization-element ue-element"
                :style="ue.style"
              >
                <img src="../runtassets/UE.png" alt="用户设备" class="element-image">
                <div class="element-label">UE {{ index + 1 }}</div>
              </div>
            </div>
          </div>
          
          <!-- 右侧：模型选择和详情 -->
          <div class="model-info-container">
            <div class="model-selection">
              <div class="form-group">
                <label for="model-select">选择模型：</label>
                <select 
                  id="model-select" 
                  v-model="selectedModelId" 
                  @change="onModelChange" 
                  :disabled="isLoadingModels"
                >
                  <option value="">请选择模型</option>
                  <option 
                    v-for="model in models" 
                    :key="model.id" 
                    :value="model.id"
                  >
                    {{ model.algorithm }} - ID: {{ model.id }} (状态: {{ model.status_text }})
                  </option>
                </select>
                <div v-if="isLoadingModels" class="loading-indicator">加载中...</div>
              </div>
              
              <!-- 推理控制 -->
              <div class="inference-control">
                <button 
                  @click="startInference" 
                  :disabled="!selectedModelId || isLoadingInference"
                  class="primary-button"
                >
                  {{ isLoadingInference ? '推理中...' : '开始推理' }}
                </button>
                <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
              </div>
              
              <!-- 模型详情 - 单列 -->
              <div v-if="selectedModel" class="model-details">
                <h4>模型详情</h4>
                <div class="model-info-list">
                  <div class="info-item">
                    <span class="label">算法：</span>
                    <span class="value">{{ selectedModel.algorithm }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">目标回合数：</span>
                    <span class="value">{{ selectedModel.target_episode }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">当前回合数：</span>
                    <span class="value">{{ selectedModel.current_episode }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">UE数量：</span>
                    <span class="value">{{ selectedModel.n_UE }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">学习率：</span>
                    <span class="value">{{ selectedModel.learning_rate }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">批次大小：</span>
                    <span class="value">{{ selectedModel.batch_size }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <!-- 推理过程展示区域 -->
      <section v-if="inferenceData" class="section process-section">
        <h3>推理过程</h3>
        

        
        <!-- 当前步骤信息 - 多栏布局 -->
        <div class="current-step-container">
          <!-- 左侧：步骤信息和奖励 -->
          <div class="step-column step-info-column">
            <div class="step-card">
              <h4>步骤 {{ currentStep + 1 }}</h4>
              <div class="info-section">
                <h5>奖励 (Reward)</h5>
                <div class="reward-value">{{ currentReward }}</div>
              </div>
            </div>
          </div>
          
          <!-- 中间：系统状态 -->
          <div class="step-column observation-column">
            <div class="step-card">
              <h5>系统状态 (Observation)</h5>
              <div class="observation-content">
                <div v-if="currentObservationDesc" class="observation-desc">
                  {{ currentObservationDesc }}
                </div>
                <div v-else class="loading-indicator">解析中...</div>
              </div>
            </div>
          </div>
          
          <!-- 右侧：系统决策 -->
          <div class="step-column action-column">
            <div class="step-card">
              <h5>系统决策 (Action)</h5>
              <div class="action-content">
                <div v-if="currentActionDesc" class="action-desc">
                  {{ currentActionDesc }}
                </div>
                <div v-else class="loading-indicator">解析中...</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 原始数据（可选展示） -->
        <div class="raw-data-section" v-if="showRawData">
          <h5>原始数据</h5>
          <div class="data-grid">
            <div class="data-item">
              <span class="label">Observation：</span>
              <span class="value">{{ inferenceData.observation[currentStep] }}</span>
            </div>
            <div class="data-item">
              <span class="label">Action：</span>
              <span class="value">{{ inferenceData.action[currentStep] }}</span>
            </div>
          </div>
        </div>
      </section>
      

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// 状态管理
const models = ref([])
const selectedModelId = ref('')
const selectedModel = ref(null)
const isLoadingModels = ref(false)
const isLoadingInference = ref(false)
const errorMessage = ref('')
const inferenceData = ref(null)
const currentStep = ref(0)
const isPlaying = ref(true)
const jumpStep = ref(1)
const showRawData = ref(false)

// 可视化相关状态
const visualizationRef = ref(null)
const visualizationWidth = ref(400)
const visualizationHeight = ref(300)
const uavPosition = ref({ x: 0, y: 0, z: 0 })
const ueElements = ref([])

// 定时器
let playbackTimer = null

// 初始化获取模型列表
onMounted(() => {
  fetchModels()
})

// 清理定时器
onUnmounted(() => {
  if (playbackTimer) {
    clearInterval(playbackTimer)
  }
})

// 监听currentStep变化，更新jumpStep
watch(currentStep, (newStep) => {
  jumpStep.value = newStep + 1
})

// 获取模型列表
const fetchModels = async () => {
  try {
    isLoadingModels.value = true
    const response = await axios.get('http://127.0.0.1:8000/models/')
    if (response.data.status === 'success') {
      models.value = response.data.data.models
    } else {
      throw new Error('获取模型列表失败')
    }
  } catch (error) {
    errorMessage.value = `获取模型列表失败：${error.message}`
    console.error('获取模型列表失败：', error)
  } finally {
    isLoadingModels.value = false
  }
}

// 模型选择变化处理
const onModelChange = () => {
  if (selectedModelId.value) {
    selectedModel.value = models.value.find(model => model.id === parseInt(selectedModelId.value))
    // 重置推理数据
    inferenceData.value = null
    currentStep.value = 0
    isPlaying.value = true
  } else {
    selectedModel.value = null
  }
}

// 开始推理
const startInference = async () => {
  if (!selectedModelId.value || !selectedModel.value) {
    errorMessage.value = '请先选择模型'
    return
  }
  
  try {
    isLoadingInference.value = true
    errorMessage.value = ''
    
    // 根据selectedModel获取n_ue
    const n_ue = selectedModel.value.n_UE || 5 // 默认值为5
    
    // 根据RUNT_env_analysis.md文档生成observation
    // observation大小：4*n_ues + 4
    // 组成部分：
    // 0:n_ues - 任务计算消耗列表
    // n_ues:2*n_ues - 任务大小列表
    // 2*n_ues:3*n_ues - 任务时间限制列表
    // 3*n_ues:4*n_ues - UE剩余执行时间列表
    // 4*n_ues:4*n_ues+3 - RIS-UAV位置
    // 4*n_ues+3: - BS-MEC当前计算能力
    
    const observationSize = 4 * n_ue + 4
    const observation = []
    
    // 生成任务计算消耗列表 (0:n_ue)
    for (let i = 0; i < n_ue; i++) {
      observation.push(Math.random() * 2) // 归一化值，范围[0, 1]
    }
    
    // 生成任务大小列表 (n_ue:2*n_ue)
    for (let i = 0; i < n_ue; i++) {
      observation.push(Math.random() * 2) // 归一化值，范围[0, 1]
    }
    
    // 生成任务时间限制列表 (2*n_ue:3*n_ue)
    for (let i = 0; i < n_ue; i++) {
      observation.push(Math.random()) // 归一化值，范围[0, 1]
    }
    
    // 生成UE剩余执行时间列表 (3*n_ue:4*n_ue)
    for (let i = 0; i < n_ue; i++) {
      observation.push(Math.random()) // 归一化值，范围[0, 1]
    }
    
    // 生成RIS-UAV位置 (4*n_ue:4*n_ue+3) - x, y, z
    observation.push(Math.random() * 2 - 1) // x坐标，范围[-1, 1]
    observation.push(Math.random() * 2 - 1) // y坐标，范围[-1, 1]
    observation.push(Math.random()) // z坐标，范围[0, 1]
    
    // 生成BS-MEC当前计算能力 (4*n_ue+3:)
    observation.push(Math.random()) // 归一化值，范围[0, 1]
    
    // 调用推理接口
    const response = await axios.post(
      'http://127.0.0.1:8000/testmodel/',
      {
        model_id: String(selectedModelId.value),
        observation: observation
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
    
    // 保存推理数据
    inferenceData.value = response.data
    currentStep.value = 0
    isPlaying.value = true
    
    // 开始自动播放
    startPlayback()
  } catch (error) {
    errorMessage.value = `推理失败：${error.message}`
    console.error('推理失败：', error)
  } finally {
    isLoadingInference.value = false
  }
}

// 开始播放
const startPlayback = () => {
  if (playbackTimer) {
    clearInterval(playbackTimer)
  }
  
  playbackTimer = setInterval(() => {
    if (isPlaying.value && currentStep.value < inferenceData.value.rewards.length - 1) {
      currentStep.value++
    } else if (currentStep.value >= inferenceData.value.rewards.length - 1) {
      // 播放结束
      isPlaying.value = false
      clearInterval(playbackTimer)
      playbackTimer = null
    }
  }, 1000) // 每秒一条
}

// 切换播放状态
const togglePlayback = () => {
  isPlaying.value = !isPlaying.value
  if (isPlaying.value) {
    startPlayback()
  }
}

// 重置播放
const resetPlayback = () => {
  currentStep.value = 0
  isPlaying.value = true
  startPlayback()
}

// 跳转到指定步骤
const goToStep = () => {
  const step = Math.max(1, Math.min(jumpStep.value, inferenceData.value.rewards.length)) - 1
  currentStep.value = step
  isPlaying.value = false
}

// 计算当前步骤的observation描述
const currentObservationDesc = computed(() => {
  if (!inferenceData.value || currentStep.value >= inferenceData.value.observation.length) {
    return ''
  }
  
  const obs = inferenceData.value.observation[currentStep.value]
  const n_ue = selectedModel.value?.n_UE || 5
  return parseObservation(obs, n_ue)
})

// 计算当前步骤的action描述
const currentActionDesc = computed(() => {
  if (!inferenceData.value || currentStep.value >= inferenceData.value.action.length) {
    return ''
  }
  
  const action = inferenceData.value.action[currentStep.value]
  const n_ue = selectedModel.value?.n_UE || 5
  return parseAction(action, n_ue)
})

// 计算当前步骤的reward，并限制显示长度为最多8位数字
const currentReward = computed(() => {
  if (!inferenceData.value || currentStep.value >= inferenceData.value.rewards.length) {
    return 0
  }
  
  const reward = inferenceData.value.rewards[currentStep.value]
  // 转换为字符串并限制长度为最多8位数字
  const rewardStr = reward.toString()
  if (rewardStr.length > 8) {
    // 如果是小数，保留适当的小数位数，确保总长度不超过8位
    if (rewardStr.includes('.')) {
      const integerPart = rewardStr.split('.')[0]
      const decimalPart = rewardStr.split('.')[1]
      // 整数部分长度 + 小数点 + 小数部分长度 <= 8
      const maxDecimalLength = Math.max(0, 8 - integerPart.length - 1)
      return parseFloat(reward.toFixed(maxDecimalLength))
    } else {
      // 如果是整数，截取前8位
      return parseInt(rewardStr.substring(0, 8))
    }
  }
  return reward
})

// 可视化元素样式计算属性
const bsStyle = computed(() => {
  return {
    left: `${visualizationWidth.value / 2 - 25}px`, // 居中显示，减去图片宽度的一半
    top: `${visualizationHeight.value / 2 - 25}px`,  // 居中显示，减去图片高度的一半
    zIndex: 1
  }
})

const uavStyle = computed(() => {
  // 将UAV位置从归一化坐标转换为可视化容器中的像素坐标
  // 归一化坐标范围：x: [-1, 1], y: [-1, 1], z: [0, 1]
  const x = (uavPosition.value.x + 1) * (visualizationWidth.value - 50) / 2 // 转换为容器中的x坐标
  const y = (uavPosition.value.y + 1) * (visualizationHeight.value - 50) / 2 // 转换为容器中的y坐标
  const z = uavPosition.value.z * 10 // z坐标影响z-index和轻微的位置偏移
  
  return {
    left: `${x}px`,
    top: `${y}px`,
    zIndex: 3 + Math.floor(z),
    transform: `translateY(-${z}px)` // 模拟z轴高度，z值越大，元素越向上
  }
})

// 初始化UE元素
const initializeUEElements = () => {
  const n_ue = selectedModel.value?.n_UE || 5
  const elements = []
  
  // 根据n_ue创建UE元素，均匀分布在容器中
  for (let i = 0; i < n_ue; i++) {
    // 计算均匀分布的位置
    const angle = (i / n_ue) * Math.PI * 2
    const radius = Math.min(visualizationWidth.value, visualizationHeight.value) / 3
    const centerX = visualizationWidth.value / 2 - 25
    const centerY = visualizationHeight.value / 2 - 25
    
    const x = centerX + Math.cos(angle) * radius
    const y = centerY + Math.sin(angle) * radius
    
    elements.push({
      id: i,
      style: {
        left: `${x}px`,
        top: `${y}px`,
        zIndex: 2
      }
    })
  }
  
  ueElements.value = elements
}

// 更新可视化元素位置
const updateVisualization = () => {
  if (!inferenceData.value || currentStep.value >= inferenceData.value.observation.length) {
    return
  }
  
  const obs = inferenceData.value.observation[currentStep.value]
  const n_ue = selectedModel.value?.n_UE || 5
  
  // 解析UAV位置 (4*n_ue:4*n_ue+3)
  const uavPosIndex = 4 * n_ue
  const x = obs[uavPosIndex]
  const y = obs[uavPosIndex + 1]
  const z = obs[uavPosIndex + 2]
  
  uavPosition.value = { x, y, z }
}

// 监听当前步骤变化，更新可视化
watch(currentStep, () => {
  updateVisualization()
})

// 监听模型选择变化，初始化UE元素
watch(selectedModel, () => {
  if (selectedModel.value) {
    initializeUEElements()
  }
})

// 监听推理数据变化，初始化可视化
watch(inferenceData, () => {
  if (inferenceData.value && inferenceData.value.observation.length > 0) {
    updateVisualization()
  }
})

// 解析observation，转换为可读描述
const parseObservation = (observation, n_ues) => {
  // 根据RUNT_env_analysis.md文档，observation数组包含以下部分：
  // 0:n_ues - 任务计算消耗列表
  // n_ues:2*n_ues - 任务大小列表
  // 2*n_ues:3*n_ues - 任务时间限制列表
  // 3*n_ues:4*n_ues - UE剩余执行时间列表
  // 4*n_ues:4*n_ues+3 - RIS-UAV位置
  // 4*n_ues+3: - BS-MEC当前计算能力
  
  const desc = []
  
  // 任务计算消耗列表
  const taskConsumption = observation.slice(0, n_ues)
  desc.push(`任务计算消耗：${taskConsumption.map((val, i) => `UE${i+1}: ${val.toFixed(2)}`).join(', ')}`)
  
  // 任务大小列表
  const taskSize = observation.slice(n_ues, 2 * n_ues)
  desc.push(`任务大小：${taskSize.map((val, i) => `UE${i+1}: ${val.toFixed(2)}`).join(', ')}`)
  
  // 任务时间限制列表
  const taskTimeLimit = observation.slice(2 * n_ues, 3 * n_ues)
  desc.push(`任务时间限制：${taskTimeLimit.map((val, i) => `UE${i+1}: ${val.toFixed(2)}`).join(', ')}`)
  
  // UE剩余执行时间列表
  const ueRemainingTime = observation.slice(3 * n_ues, 4 * n_ues)
  desc.push(`UE剩余执行时间：${ueRemainingTime.map((val, i) => `UE${i+1}: ${val.toFixed(2)}`).join(', ')}`)
  
  // RIS-UAV位置
  const uavPosition = observation.slice(4 * n_ues, 4 * n_ues + 3)
  desc.push(`RIS-UAV位置：x=${uavPosition[0].toFixed(2)}, y=${uavPosition[1].toFixed(2)}, z=${uavPosition[2].toFixed(2)}`)
  
  // BS-MEC当前计算能力
  const mecCapacity = observation.slice(-1)[0]
  desc.push(`BS-MEC当前计算能力：${mecCapacity.toFixed(2)}`)
  
  return desc.join('\n')
}

// 解析action，转换为可读描述
const parseAction = (action, n_ues) => {
  // 根据RUNT_env_analysis.md文档，action数组包含以下部分：
  // 0:n_ues - 卸载决策
  // n_ues:2*n_ues - 计算能力分配
  // 2*n_ues:3*n_ues - 传输功率列表
  // 3*n_ues:3*n_ues+5 - RIS相位变化 (n_element固定为5)
  // 3*n_ues+5: - UAV移动向量
  
  const n_element = 5 // 固定为5
  const desc = []
  
  // 卸载决策
  const offloadDecision = action.slice(0, n_ues)
  desc.push(`卸载决策：${offloadDecision.map((val, i) => `UE${i+1}: ${val < 0.5 ? '本地执行' : '卸载到MEC'}`).join(', ')}`)
  
  // 计算能力分配
  const computationAllocation = action.slice(n_ues, 2 * n_ues)
  desc.push(`计算能力分配：${computationAllocation.map((val, i) => `UE${i+1}: ${val.toFixed(2)}`).join(', ')}`)
  
  // 传输功率列表
  const transmitPower = action.slice(2 * n_ues, 3 * n_ues)
  desc.push(`传输功率：${transmitPower.map((val, i) => `UE${i+1}: ${val.toFixed(2)}`).join(', ')}`)
  
  // RIS相位变化
  const risPhase = action.slice(3 * n_ues, 3 * n_ues + n_element)
  desc.push(`RIS相位变化：${risPhase.map((val, i) => `元素${i+1}: ${val.toFixed(2)}`).join(', ')}`)
  
  // UAV移动向量
  const uavMovement = action.slice(3 * n_ues + n_element)
  desc.push(`UAV移动向量：x=${uavMovement[0].toFixed(2)}, y=${uavMovement[1].toFixed(2)}, z=${uavMovement[2].toFixed(2)}`)
  
  return desc.join('\n')
}

// 退出登录
const handleLogout = () => {
  localStorage.removeItem('isLoggedIn')
  router.push('/login')
}
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
  overflow: hidden;
}

.main-content h2 {
  color: #333;
  margin-bottom: 1.5rem;
}

.section {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.section h3 {
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.section h4 {
  color: #409eff;
  margin-bottom: 0.8rem;
  font-size: 1.1rem;
}

.section h5 {
  color: #606266;
  margin-bottom: 0.6rem;
  font-size: 1rem;
}

/* 模型选择区域 - 左侧图片占位+右侧模型信息 */
.model-selection-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  align-items: start;
}

/* 左侧模型可视化区域 */
.visualization-area {
  background-color: #f0f2f5;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  height: 100%;
  min-height: 400px;
  padding: 1rem;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}

.visualization-area h4 {
  color: #409eff;
  margin-bottom: 1rem;
  text-align: center;
  font-size: 1.1rem;
}

.visualization-container {
  position: relative;
  width: 100%;
  height: 350px;
  background-color: white;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  background-image: linear-gradient(rgba(64, 158, 255, 0.1) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(64, 158, 255, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
  background-position: 0 0;
}

.visualization-element {
  position: absolute;
  width: 50px;
  height: 50px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.5s ease;
  cursor: pointer;
}

.visualization-element:hover {
  transform: scale(1.1);
  z-index: 10 !important;
}

.element-image {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.element-label {
  font-size: 0.8rem;
  font-weight: 500;
  color: #606266;
  margin-top: 2px;
  text-align: center;
  background-color: white;
  padding: 1px 4px;
  border-radius: 3px;
  border: 1px solid #dcdfe6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 元素类型特定样式 */
.bs-element {
  transition: all 0.3s ease;
}

.uav-element {
  transition: all 0.5s ease;
}

.ue-element {
  transition: all 0.3s ease;
}

/* 右侧模型信息容器 */
.model-info-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-height: 400px; /* 与可视化区域高度匹配 */
}

.model-selection {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #606266;
  min-width: 80px;
}

.form-group select {
  padding: 0.5rem;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 1rem;
  flex: 1;
  min-width: 200px;
}

.form-group select:disabled {
  background-color: #f5f7fa;
  cursor: not-allowed;
}

/* 模型详情 - 三列布局 */
.model-details {
  background-color: #fafafa;
  padding: 1rem;
  border-radius: 4px;
  border-left: 4px solid #409eff;
  max-height: 300px;
  overflow-y: auto;
}

.model-info-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0.6rem;
  background-color: white;
  border-radius: 4px;
  border: 1px solid #ebeef5;
  transition: all 0.3s;
}

.info-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.info-item .label {
  font-weight: 500;
  color: #606266;
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}

.info-item .value {
  color: #303133;
  font-weight: 500;
  font-size: 1rem;
}

/* 推理控制区域 */
.inference-control {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.primary-button {
  padding: 0.6rem 1.2rem;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  width: fit-content;
}

.primary-button:hover:not(:disabled) {
  background-color: #66b1ff;
}

.primary-button:disabled {
  background-color: #a0cfff;
  cursor: not-allowed;
}

.error-message {
  color: #f56c6c;
  font-size: 0.9rem;
}

/* 推理过程展示区域 */
.process-section {
  margin-bottom: 1.5rem;
}

.control-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fafafa;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.step-info {
  font-weight: 500;
  color: #303133;
}

.control-buttons {
  display: flex;
  gap: 0.5rem;
}

.control-button {
  padding: 0.4rem 0.8rem;
  background-color: #67c23a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.control-button:hover {
  background-color: #85ce61;
}

.step-navigation {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.step-navigation label {
  font-weight: 500;
  color: #606266;
}

.step-navigation input {
  padding: 0.4rem;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  width: 60px;
}

/* 当前步骤信息 - 三栏布局 */
.current-step-container {
  display: grid;
  grid-template-columns: 200px 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
  min-height: 300px;
}

.step-column {
  display: flex;
  flex-direction: column;
}

.step-card {
  background-color: #fafafa;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #ebeef5;
  flex: 1;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
}

.step-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.step-info-column .step-card {
  justify-content: space-between;
}

.observation-column .step-card,
.action-column .step-card {
  overflow: hidden;
}

.info-section {
  margin-bottom: 1rem;
}

.info-section:last-child {
  margin-bottom: 0;
  flex: 1;
  overflow: hidden;
}

.observation-content,
.action-content {
  background-color: white;
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  flex: 1;
  overflow-y: auto;
  white-space: pre-line;
  line-height: 1.5;
  font-size: 0.9rem;
}

.reward-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #f56c6c;
  padding: 1rem;
  background-color: white;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  display: inline-block;
  margin-top: 0.5rem;
}

/* 原始数据展示 */
.raw-data-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px dashed #dcdfe6;
}

.data-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.data-item {
  background-color: white;
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  overflow: hidden;
}

.data-item .label {
  font-weight: 500;
  color: #606266;
  margin-right: 0.5rem;
}

.data-item .value {
  font-family: monospace;
  color: #303133;
  font-size: 0.9rem;
  word-break: break-all;
  white-space: pre-wrap;
}



/* 加载指示器 */
.loading-indicator {
  color: #409eff;
  font-size: 0.9rem;
  text-align: center;
  padding: 1rem;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content {
    padding: 1.5rem;
  }
  
  .current-step-container {
    grid-template-columns: 1fr;
    min-height: auto;
  }
  
  .step-column {
    min-height: 200px;
  }
}

@media (max-width: 992px) {
  .model-selection-container {
    grid-template-columns: 1fr;
  }
  
  .image-placeholder {
    min-height: 200px;
  }
  
  .summary-grid-horizontal {
    flex-direction: row;
    justify-content: flex-start;
    overflow-x: auto;
    padding-bottom: 1rem;
    gap: 1rem;
  }
  
  .summary-item {
    flex: 0 0 200px;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .section {
    padding: 1rem;
    margin-bottom: 1rem;
  }
  
  .model-selection-container {
    gap: 1rem;
  }
  
  .form-group {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .form-group label {
    min-width: auto;
  }
  
  .form-group select {
    width: 100%;
    min-width: auto;
  }
  
  /* 模型详情响应式调整 */
  .model-info-list {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.8rem;
  }
  
  .info-item {
    padding: 0.5rem;
  }
  
  .control-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .current-step-container {
    gap: 1rem;
  }
  
  .step-card {
    padding: 0.8rem;
  }
  
  .observation-content,
  .action-content {
    padding: 0.8rem;
    font-size: 0.85rem;
  }
  
  .summary-grid-horizontal {
    justify-content: center;
  }
  
  .summary-item {
    flex: 0 0 100%;
    max-width: none;
  }
}

@media (max-width: 480px) {
  /* 模型详情在小屏幕上单列显示 */
  .model-info-list {
    grid-template-columns: 1fr;
  }
  
  .header {
    flex-direction: column;
    height: auto;
    padding: 1rem;
    gap: 1rem;
  }
  
  .nav {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
  }
  
  .nav-link {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
  
  .main-content h2 {
    font-size: 1.3rem;
  }
  
  .section h3 {
    font-size: 1.1rem;
  }
  
  .section h4 {
    font-size: 1rem;
  }
  
  .section h5 {
    font-size: 0.9rem;
  }
  
  .model-details {
    max-height: 150px;
  }
  
  .control-bar {
    padding: 0.8rem;
  }
  
  .control-button {
    padding: 0.3rem 0.6rem;
    font-size: 0.9rem;
  }
  
  .image-placeholder {
    min-height: 150px;
  }
  
  .placeholder-icon {
    font-size: 2rem;
  }
  
  .placeholder-text {
    font-size: 1rem;
  }
  
  .placeholder-subtext {
    font-size: 0.8rem;
  }
}
</style>