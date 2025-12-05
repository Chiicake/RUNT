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
        </div>
      </div>
      <div class="hero-image">
        <img src="https://images.unsplash.com/photo-1633356122102-3fe601e05bd2?w=800&h=600&fit=crop&crop=entropy&auto=format&q=80" alt="算力网络示意图" onerror="this.src='https://via.placeholder.com/800x600?text=算力网络示意图'" />
      </div>
    </section>
    
    <main class="main-content">
      <!-- 平台简介 -->
      <section class="section overview">
        <h3>平台简介</h3>
        <div class="overview-content">
          <div class="overview-text">
            <p>本平台聚焦强化学习模型在算力网络资源分配优化中的训练与仿真需求，支持用户通过灵活配置参数开展模型训练、实时监控训练过程，同时提供训练后模型的仿真推理与结果可视化，助力高效验证算力网络资源分配算法的性能。</p>
          </div>
          <div class="overview-image">
            <img src="https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&h=400&fit=crop&crop=entropy&auto=format&q=80" alt="强化学习示意图" onerror="this.src='https://via.placeholder.com/600x400?text=强化学习示意图'" />
          </div>
        </div>
      </section>
      
      <!-- 核心功能 -->
      <section class="section features">
        <h3>核心功能</h3>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-image">
              <img src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&h=300&fit=crop&crop=entropy&auto=format&q=80" alt="模型训练" onerror="this.src='https://via.placeholder.com/400x300?text=模型训练'" />
            </div>
            <h4>强化学习模型训练</h4>
            <ul>
              <li>支持灵活配置算法超参数与环境参数</li>
              <li>实时展示训练过程关键指标</li>
              <li>自动保存模型文件，支持版本管理</li>
            </ul>
          </div>
          
          <div class="feature-card">
            <div class="feature-image">
              <img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400&h=300&fit=crop&crop=entropy&auto=format&q=80" alt="仿真模拟" onerror="this.src='https://via.placeholder.com/400x300?text=仿真模拟'" />
            </div>
            <h4>算力网络仿真模拟</h4>
            <ul>
              <li>支持加载已保存的强化学习模型</li>
              <li>实时可视化仿真推理结果</li>
              <li>动态展示资源分配决策过程</li>
            </ul>
          </div>
        </div>
      </section>
      
      <!-- 核心优势 -->
      <section class="section advantages">
        <h3>平台优势</h3>
        <div class="advantages-grid">
          <div class="advantage-item">
            <div class="advantage-icon">🎯</div>
            <h4>场景贴合性</h4>
            <p>1:1复刻论文仿真环境，参数配置与论文保持一致</p>
          </div>
          <div class="advantage-item">
            <div class="advantage-icon">💡</div>
            <h4>操作便捷性</h4>
            <p>直观的参数输入界面、实时可视化图表，降低技术门槛</p>
          </div>
          <div class="advantage-item">
            <div class="advantage-icon">🔄</div>
            <h4>功能完整性</h4>
            <p>覆盖全流程，满足算力网络算法验证的闭环需求</p>
          </div>
        </div>
      </section>
      
      <!-- 技术支撑 -->
      <section class="section technology">
        <h3>核心技术</h3>
        <div class="technology-content">
          <div class="technology-item">
            <h4>算法适配</h4>
            <p>深度兼容RA-MASAC算法，同时支持随机卸载等对比基线算法</p>
          </div>
          <div class="technology-item">
            <h4>场景还原</h4>
            <p>严格遵循论文系统模型，确保仿真场景的真实性</p>
          </div>
          <div class="technology-item">
            <h4>指标对齐</h4>
            <p>训练与仿真结果指标完全参照论文标准</p>
          </div>
        </div>
      </section>
    </main>
    
    <!-- 页脚 -->
    <footer class="footer">
      <p>© 2025 算力网络模拟仿真平台. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    handleLogout() {
      localStorage.removeItem('isLoggedIn')
      this.$router.push('/login')
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
  padding: 2rem;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
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
  margin-bottom: 2rem;
  font-size: 2rem;
  text-align: center;
  position: relative;
}

.section h3::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

/* 平台简介 */
.overview-content {
  display: flex;
  gap: 3rem;
  align-items: center;
  flex-wrap: wrap;
}

.overview-text {
  flex: 1;
  min-width: 300px;
}

.overview-text p {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #666;
}

.overview-image {
  flex: 1;
  min-width: 300px;
}

.overview-image img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 核心功能 */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.feature-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.feature-image {
  height: 200px;
  overflow: hidden;
}

.feature-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.feature-card:hover .feature-image img {
  transform: scale(1.05);
}

.feature-card h4 {
  padding: 1.5rem 1.5rem 0.5rem;
  margin: 0;
  color: #333;
  font-size: 1.3rem;
}

.feature-card ul {
  padding: 0 1.5rem 1.5rem;
  margin: 0;
  list-style-position: inside;
}

.feature-card li {
  margin-bottom: 0.5rem;
  line-height: 1.6;
  color: #666;
}

/* 核心优势 */
.advantages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.advantage-item {
  text-align: center;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  transition: all 0.3s;
}

.advantage-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.advantage-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.advantage-item h4 {
  margin-bottom: 0.5rem;
  color: #333;
  font-size: 1.2rem;
}

.advantage-item p {
  color: #666;
  line-height: 1.6;
}

/* 技术支撑 */
.technology-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.technology-item {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.technology-item h4 {
  margin-bottom: 0.5rem;
  color: #333;
  font-size: 1.2rem;
}

.technology-item p {
  color: #666;
  line-height: 1.6;
}

/* 页脚 */
.footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 2rem;
  margin-top: auto;
}

.footer p {
  margin: 0;
  opacity: 0.8;
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