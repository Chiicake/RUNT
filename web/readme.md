# RUNT Web API 文档

## 数据库配置

### 配置说明

项目使用MySQL数据库，配置信息如下：

- **数据库类型**: MySQL
- **主机地址**: localhost
- **端口号**: 3306
- **用户名**: root
- **密码**: 2512
- **数据库名**: runt

### 数据库初始化

1. 确保MySQL服务已启动

2. 创建名为`runt`的数据库

3. 在项目根目录执行以下命令生成迁移文件：

   ```bash
   python manage.py makemigrations
   ```

4. 执行迁移命令创建表：

   ```bash
   python manage.py migrate
   ```

### 用户管理

#### 创建初始用户

可以通过Django的shell创建初始用户：

```bash
python manage.py shell
```

在shell中执行以下命令：

```python
from web.models import User
user = User(uername='admin', password='123456')
user.save()
```

## 

## 模型列表查询接口

### 接口概述
用于查询强化学习模型列表的HTTP接口，支持分页查询，返回模型的基本信息和状态。

### 接口详情

#### 请求信息
- **URL**: `/models/`
- **方法**: `GET`
- **内容类型**: `application/json`

#### 请求参数
| 参数名 | 类型 | 必须 | 描述 |
|--------|------|------|------|
| page | 整数 | 否 | 页码，默认1 |
| page_size | 整数 | 否 | 每页条数，默认10 |

#### 响应信息
- **内容类型**: `application/json`

#### 响应示例

##### 成功响应
```json
{
  "status": "success",
  "message": "查询成功",
  "data": {
    "total": 17,
    "page": 1,
    "page_size": 10,
    "total_pages": 2,
    "models": [
      {
        "id": 17,
        "algorithm": "DQN",
        "target_episode": 5,
        "current_episode": 0,
        "status": 0,
        "status_text": "训练中",
        "task_size_average": 1024.5,
        "task_comsumption_average": 512.25,
        "task_time_average": 10.5,
        "task_arrival_rate": 2.5,
        "n_UE": 10,
        "UE_computation_capacity": 10000.0,
        "MEC_computation_capacity": 100000.0,
        "seed": 42,
        "learning_rate": 0.0001,
        "batch_size": 64,
        "buffer_size": null,
        "gamma": 0.99,
        "create_time": "2025-12-04 20:09:25",
        "update_time": "2025-12-04 20:09:25"
      }
    ]
  }
}
```

##### 失败响应
```json
{
  "status": "error",
  "message": "参数错误: 页码和每页条数必须大于0"
}
```

### 使用示例

#### curl命令示例
```bash
curl -X GET "http://127.0.0.1:8000/models/?page=1&page_size=10"
```

#### PowerShell命令示例
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/models/?page=1&page_size=10" -Method GET
```

## 模型训练数据查询接口

### 接口概述
用于查询特定强化学习模型训练数据的HTTP接口，支持分页查询，返回模型的训练回合奖励数据。

### 接口详情

#### 请求信息
- **URL**: `/models/<model_id>/train-data/`
- **方法**: `GET`
- **内容类型**: `application/json`

#### 请求参数
| 参数名 | 类型 | 必须 | 描述 |
|--------|------|------|------|
| model_id | 整数 | 是 | 模型ID，从URL路径中获取 |
| page | 整数 | 否 | 页码，默认1 |
| page_size | 整数 | 否 | 每页条数，默认20 |

#### 响应信息
- **内容类型**: `application/json`

#### 响应示例

##### 成功响应
```json
{
  "status": "success",
  "message": "查询成功",
  "data": {
    "model_id": 17,
    "model_algorithm": "DQN",
    "total": 5,
    "page": 1,
    "page_size": 20,
    "total_pages": 1,
    "train_data": [
      {
        "id": 1,
        "episode": 1,
        "reward": -2122.6564,
        "smoothed_reward": -2122.6564,
        "create_time": "2025-12-04 20:09:25",
        "update_time": "2025-12-04 20:09:25"
      }
    ]
  }
}
```

##### 失败响应
```json
{
  "status": "error",
  "message": "模型ID 999 不存在"
}
```

### 使用示例

#### curl命令示例
```bash
curl -X GET "http://127.0.0.1:8000/models/17/train-data/?page=1&page_size=20"
```

#### PowerShell命令示例
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/models/17/train-data/?page=1&page_size=20" -Method GET
```

## 运行说明

### 启动服务
在项目根目录执行以下命令启动Django开发服务器：

```bash
D:\anaconda\envs\myrl\python.exe manage.py runserver
```

### 访问接口
服务器启动后，接口可通过以下地址访问：

```
http://127.0.0.1:8000/login/
http://127.0.0.1:8000/train/
http://127.0.0.1:8000/models/
http://127.0.0.1:8000/models/<model_id>/train-data/
```

## 登录接口

### 接口概述
用于用户登录验证的HTTP接口，从MySQL数据库的user表中验证用户名和密码，验证成功后返回成功信息，失败则返回错误信息。

### 接口详情

#### 请求信息
- **URL**: `/login/`
- **方法**: `POST`
- **内容类型**: `application/x-www-form-urlencoded`

#### 请求参数
| 参数名 | 类型 | 必须 | 描述 |
|--------|------|------|------|
| username | 字符串 | 是 | 用户名 |
| password | 字符串 | 是 | 密码 |

#### 响应信息
- **内容类型**: `application/json`

#### 响应示例

##### 成功响应
```json
{
  "status": "success",
  "message": "登录成功"
}
```

##### 失败响应
```json
{
  "status": "error",
  "message": "用户名或密码错误"
}
```

### 使用示例

#### curl命令示例
```bash
curl -X POST http://127.0.0.1:8000/login/ -d "username=admin&password=123456"
```

#### PowerShell命令示例
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/login/ -Method POST -Body @{username='admin';password='123456'}
```

## 训练接口

### 接口概述
用于创建强化学习模型训练任务的HTTP接口，接收训练参数并写入rl_model表，同时创建以自增主键ID命名的txt文件。

### 接口详情

#### 请求信息
- **URL**: `/train/`
- **方法**: `POST`
- **内容类型**: `application/x-www-form-urlencoded`

#### 请求参数
| 参数名 | 类型 | 必须 | 描述 | 数据库类型 |
|--------|------|------|------|------------|
| algorithm | 字符串 | 是 | 算法名称（如DQN、PPO等） | VARCHAR(100) |
| target_episode | 整数 | 是 | 目标训练回合数 | INT UNSIGNED |
| task_size_average | 小数 | 否 | 任务平均大小，保留4位小数 | DECIMAL(10, 4) |
| task_comsumption_average | 小数 | 否 | 任务平均消耗，保留4位小数 | DECIMAL(10, 4) |
| task_time_average | 小数 | 否 | 任务平均耗时，保留4位小数 | DECIMAL(10, 4) |
| task_arrival_rate | 小数 | 否 | 任务到达率，保留4位小数 | DECIMAL(8, 4) |
| n_UE | 整数 | 否 | 用户设备(UE)数量 | INT UNSIGNED |
| UE_computation_capacity | 小数 | 否 | UE计算能力，保留2位小数 | DECIMAL(10, 2) |
| MEC_computation_capacity | 小数 | 否 | MEC服务器计算能力，保留2位小数 | DECIMAL(12, 2) |
| seed | 整数 | 否 | 随机种子 | INT UNSIGNED |
| learning_rate | 小数 | 否 | 学习率，保留6位小数 | DECIMAL(8, 6) |
| batch_size | 整数 | 否 | 批次大小 | INT UNSIGNED |
| gamma | 小数 | 否 | 折扣因子γ，保留6位小数 | DECIMAL(8, 6) |

#### 响应信息
- **内容类型**: `application/json`

#### 响应示例

##### 成功响应
```json
{
  "status": "success",
  "message": "训练任务创建成功",
  "id": 1
}
```

##### 失败响应

###### 参数验证失败
```json
{
  "status": "error",
  "message": "algorithm参数不能为空"
}
```

###### 服务器内部错误
```json
{
  "status": "error",
  "message": "服务器内部错误: [具体错误信息]"
}
```

### 使用示例

#### PowerShell命令示例
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/train/ -Method Post -Body @{
    algorithm='DQN';
    target_episode=1000;
    task_size_average=10.5;
    task_comsumption_average=5.2;
    task_time_average=2.3;
    task_arrival_rate=0.1;
    n_UE=10;
    UE_computation_capacity=100.5;
    learning_rate=0.001;
    batch_size=32;
    gamma=0.99
}
```

## 模型推理接口

### 接口概述
用于使用预训练模型执行推理的HTTP接口，接收模型ID和初始观测值，执行100步推理并返回结果。

### 接口详情

#### 请求信息
- **URL**: `/testmodel/`
- **方法**: `POST`
- **内容类型**: `application/json`

#### 请求参数
| 参数名 | 类型 | 必须 | 描述 |
|--------|------|------|------|
| model_id | 字符串 | 是 | 模型ID |
| observation | 数组 | 是 | 初始观测值数组，包含浮点数 |

#### 响应信息
- **内容类型**: `application/json`

#### 响应示例

##### 成功响应
```json
{
  "observation": [[0.1, 0.2, ...], [0.3, 0.4, ...], ...],
  "action": [[0.5, 0.6, ...], [0.7, 0.8, ...], ...],
  "rewards": [1.0, 2.0, ...]
}
```

##### 失败响应
```json
{
  "status": "error",
  "message": "模型ID 123 不存在"
}
```

### 使用示例

#### curl命令示例
```bash
curl -X POST http://127.0.0.1:8000/testmodel/ -H "Content-Type: application/json" -d '{"model_id": "123", "observation": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]}'
```

#### PowerShell命令示例
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/testmodel/ -Method POST -ContentType "application/json" -Body '{"model_id": "123", "observation": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]}'
```

## 接口列表

### 所有可用接口
| 接口路径 | 方法 | 描述 |
|----------|------|------|
| `/login/` | POST | 用户登录验证 |
| `/train/` | POST | 创建强化学习模型训练任务 |
| `/models/` | GET | 查询模型列表，支持分页 |
| `/models/<model_id>/train-data/` | GET | 查询特定模型的训练数据，支持分页 |
| `/testmodel/` | POST | 使用预训练模型执行推理 |

