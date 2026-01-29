# 数据库表
模型表 rl_model
字段
- id
- algorithm
- target_episode
- current_episode
- status 0: 训练中, 1: 训练完成
- task_size_average
- task_comsumption_average
- task_time_average
- task_arrival_rate
- n_UE
- UE_computation_capacity
- MEC_computation_capacity
- seed
- learning_rate
- batch_size
- buffer_size
- gamma

训练数据表 training_data
字段
- model_id
- episode
- reward
- smoothed_reward


# 接口
## 训练接口 
### 开始训练
POST /train

调用训练接口，传入参数开始训练。返回模型id。在训练过程中，将模型的测试数据保存在数据库中。
#### input
- task_size_average
- task_comsumption_average
- task_time_average
- task_arrival_rate
- n_UE
- UE_computation_capacity
- MEC_computation_capacity
- seed

#### output
- model_id

### 获取训练结果
POST /result

调用获取训练结果接口，传入模型id，返回模型的测试数据。
#### input
- model_id
- episode

#### output
- reward
- smoothed_reward

### 获取训练状态
POST /status
调用获取训练状态接口，传入模型id，返回模型的训练状态。
#### input
- model_id

#### output
- episode
- status

