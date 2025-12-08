# 训练助手API配置文件
# 用于存储敏感信息，如API密钥等

import os
from dotenv import load_dotenv

# 加载.env文件（如果存在）
load_dotenv()

# 检查是否存在.env文件，如果不存在，尝试加载.env.example
if not os.path.exists('.env') and os.path.exists('.env.example'):
    load_dotenv('.env.example')

class Config:
    # DeepSeek配置
    # 优先使用DEEPSEEK_API_KEY，如果不存在则使用OPENAI_API_KEY作为兼容
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", os.getenv("OPENAI_API_KEY", ""))
    DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", os.getenv("OPENAI_API_BASE", "https://api.deepseek.com"))
    DEEPSEEK_MODEL_NAME = os.getenv("DEEPSEEK_MODEL_NAME", os.getenv("OPENAI_MODEL_NAME", "deepseek-chat"))
    
    # 应用配置
    APP_NAME = "Training Assistant API"
    APP_VERSION = "1.0.0"
    
    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # 流式响应配置
    STREAM_CHUNK_SIZE = 1024

# 创建配置实例
config = Config()