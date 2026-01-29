<template>
  <div class="login-container">
    <div class="login-form">
      <h2>算力网络模拟仿真平台</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            placeholder="请输入用户名" 
            required
          >
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="请输入密码" 
            required
          >
        </div>
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        <button type="submit" class="login-button" :disabled="isLoading">
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      error: '',
      isLoading: false
    }
  },
  methods: {
    async handleLogin() {
      this.error = ''
      this.isLoading = true
      
      try {
        const response = await axios.post('http://127.0.0.1:8000/login/', 
          new URLSearchParams({
            username: this.username,
            password: this.password
          }),
          {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          }
        )
        
        if (response.data.status === 'success') {
          localStorage.setItem('isLoggedIn', 'true')
          this.$router.push('/home')
        } else {
          this.error = response.data.message || '登录失败'
        }
      } catch (error) {
        this.error = '登录失败，请检查网络连接或服务器状态'
        console.error('登录请求失败:', error)
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.login-form {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-form h2 {
  margin-bottom: 1.5rem;
  color: #333;
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #409eff;
}

.error-message {
  color: #f56c6c;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  text-align: center;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover:not(:disabled) {
  background-color: #66b1ff;
}

.login-button:disabled {
  background-color: #c6e2ff;
  cursor: not-allowed;
}
</style>