# RUNT Web API 文档

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
user = User(username='admin', password='123456')
user.save()
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
| current_episode | 整数 | 否 | 当前训练回合数，默认0 | INT UNSIGNED |
| status | 整数 | 否 | 训练状态：0-训练中，1-训练完成，默认0 | TINYINT |
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
    current_episode=0;
    status=0;
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
```
