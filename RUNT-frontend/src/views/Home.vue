<template>
  <div class="container">
    <header class="header">
      <h1>算力网络模拟仿真平台</h1>
      <nav class="nav">
        <router-link to="/home" class="nav-link active">首页</router-link>
        <router-link to="/model-training" class="nav-link">模型训练</router-link>
        <router-link to="/simulation-demo" class="nav-link">仿真演示</router-link>
        <button @click="handleLogout" class="logout-button">退出登录</button>
      </nav>
    </header>
    
    <!-- 英雄区域 -->
    <section class="hero">
      <div class="hero-content">
        <h2>欢迎使用算力网络模拟仿真平台</h2>
        <p>基于RIS-UAV辅助THz通信的云-边-端协同算力网络架构，打造一站式强化学习模型训练管理系统</p>
        <div class="hero-actions">
          <router-link to="/model-training" class="btn btn-primary">开始训练</router-link>
          <router-link to="/simulation-demo" class="btn btn-secondary">查看仿真</router-link>
          <button @click="openPaperModal" class="btn btn-secondary">查看论文</button>
        </div>
      </div>
      
      <!-- 论文查看模态框 -->
      <div v-if="isPaperModalOpen" class="modal-overlay" @click="closePaperModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>论文查看</h3>
            <button class="modal-close" @click="closePaperModal">×</button>
          </div>
          <div class="modal-body">
            <embed :src="pdfUrl" type="application/pdf" width="100%" height="600px" />
          </div>
        </div>
      </div>
      <div class="hero-image">
        <img src="../assets/sysmodel.png" alt="算力网络示意图" onerror="this.src='https://via.placeholder.com/800x600?text=算力网络示意图'" />
      </div>
    </section>
    
    <main class="main-content">
      <!-- 平台简介和核心功能合并为左右分栏 -->
      <section class="section combined-section">
        <div class="combined-grid">
          <!-- 左侧：平台简介 -->
          <div class="section-column overview-column">
            <h3>平台简介</h3>
            <div class="overview-content">
              <div class="overview-text">
                <p>本平台聚焦强化学习模型在算力网络资源分配优化中的训练与仿真需求，支持用户灵活配置参数开展模型训练、实时监控训练过程，同时提供训练后模型的仿真推理与结果可视化，助力高效验证算力网络资源分配算法的性能。</p>
              </div>
              <div class="overview-image">
                <img src="https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&h=400&fit=crop&crop=entropy&auto=format&q=80" alt="强化学习示意图" onerror="this.src='https://via.placeholder.com/600x400?text=强化学习示意图'" />
              </div>
            </div>
          </div>
          
          <!-- 右侧：核心功能 -->
          <div class="section-column features-column">
            <h3>核心功能</h3>
            <div class="features-grid">
              <div class="feature-item">
                <h4>强化学习模型训练</h4>
                <ul>
                  <li>灵活配置算法超参数与环境参数</li>
                  <li>实时监控训练过程关键指标</li>
                  <li>自动保存模型文件</li>
                  <li>智能分析训练参数</li>
                </ul>
              </div>
              
              <div class="feature-item">
                <h4>算力网络仿真模拟</h4>
                <ul>
                  <li>加载已保存的强化学习模型</li>
                  <li>实时可视化仿真推理结果</li>
                  <li>动态展示资源分配决策过程</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

    </main>
    

  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      isPaperModalOpen: false,
      pdfUrl: ''
    }
  },
  methods: {
    handleLogout() {
      localStorage.removeItem('isLoggedIn')
      this.$router.push('/login')
    },
    openPaperModal() {
      this.isPaperModalOpen = true
      // 在Vue 3 + Vite项目中，使用import.meta.url构建正确的静态资源路径
      this.pdfUrl = new URL('../assets/paper.pdf', import.meta.url).href
    },
    closePaperModal() {
      this.isPaperModalOpen = false
    }
  }
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
  position: sticky;
  top: 0;
  z-index: 100;
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

/* 英雄区域 */
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4rem;
  flex-wrap: wrap;
}

.hero-content {
  max-width: 600px;
}

.hero-content h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 4px;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-block;
  text-align: center;
}

.btn-primary {
  background-color: white;
  color: #667eea;
}

.btn-primary:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-secondary {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.hero-image {
  max-width: 600px;
  flex: 1;
  min-width: 300px;
}

.hero-image img {
  width: 100%;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.main-content {
  flex: 1;
  max-width: 1380px;
  width: 100%;
  margin: 0 auto;
  padding: 0 2rem;
}

.section {
  margin-bottom: 3rem;
  background-color: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.section h3 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  text-align: left;
  position: relative;
}

.section h3::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

/* 合并布局样式 */
.combined-section {
  margin-bottom: 3rem;
  background-color: transparent;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: none;
  width: 100%;
  margin: 0 auto;
}

.combined-grid {
  display: grid;
  grid-template-columns: 1.15fr 1.15fr;
  gap: 2rem;
  align-items: flex-start;
  max-width: 1380px;
  margin: 0 auto;
}

.section-column {
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.section-column:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

/* 平台简介样式 */
.overview-column {
  transform: translateX(-65px);
  width: 110%;
}

.overview-column h3 {
  margin-bottom: 1rem;
}

.overview-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.overview-text p {
  font-size: 1rem;
  line-height: 1.7;
  color: #666;
  margin: 0;
}

.overview-image {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.overview-image img {
  width: 100%;
  height: auto;
  object-fit: cover;
  display: block;
}

/* 核心功能样式 */
.features-column {
  transform: translateX(20px);
  width: 110%;
}

.features-column h3 {
  margin-bottom: 1.5rem;
}

.features-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.feature-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.feature-item h4 {
  margin: 0 0 1rem;
  color: #333;
  font-size: 1.2rem;
}

.feature-item ul {
  padding: 0;
  margin: 0;
  list-style-type: none;
}

.feature-item li {
  margin-bottom: 0.5rem;
  line-height: 1.6;
  color: #666;
  font-size: 0.95rem;
  position: relative;
  padding-left: 0;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .combined-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .section h3 {
    text-align: center;
  }
  
  .section h3::after {
    left: 50%;
    transform: translateX(-50%);
  }
}



/* 论文模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s ease;
}

.modal-overlay {
  opacity: 1;
  visibility: visible;
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 1000px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background-color: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

.modal-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.2rem;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.8rem;
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
  line-height: 1;
}

.modal-close:hover {
  background-color: #ecf5ff;
  color: #409eff;
}

.modal-body {
  padding: 1.5rem;
  flex: 1;
  overflow: auto;
  background-color: white;
}

.modal-body embed {
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

/* 响应式模态框 */
@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    max-height: 95vh;
  }
  
  .modal-header {
    padding: 1rem;
  }
  
  .modal-body {
    padding: 1rem;
  }
  
  .modal-body embed {
    height: 500px;
  }
}

@media (max-width: 480px) {
  .modal-body embed {
    height: 400px;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header {
    padding: 0 1rem;
  }
  
  .header h1 {
    font-size: 1.2rem;
  }
  
  .nav {
    gap: 0.5rem;
  }
  
  .nav-link {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
  
  .logout-button {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
  
  .hero {
    padding: 2rem 1rem;
    text-align: center;
  }
  
  .hero-content h2 {
    font-size: 2rem;
  }
  
  .hero-actions {
    justify-content: center;
  }
  
  .main-content {
    padding: 1rem;
  }
  
  .section {
    padding: 1.5rem;
  }
  
  .section h3 {
    font-size: 1.6rem;
  }
  
  .overview-content {
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .advantages-grid {
    grid-template-columns: 1fr;
  }
  
  .technology-content {
    grid-template-columns: 1fr;
  }
}
</style>