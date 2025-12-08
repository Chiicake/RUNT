# RuntBoxEnv 动作空间与观察空间分析

## 1. 环境概述

`RuntBoxEnv`是一个基于`RuntSystem`的强化学习环境，用于模拟和优化无线通信系统中的资源管理。该环境采用Box空间作为动作和观察空间，方便与各种强化学习算法集成。

## 2. 动作空间（Action Space）

### 2.1 基本信息

- **类型**：`gym.spaces.Box`
- **范围**：`[0, 1]`
- **数据类型**：`np.float32`
- **大小**：`3*n_ues + 3 + n_element`
  - `n_ues`：用户设备数量（默认5）
  - `n_element`：RIS反射元素数量（默认5）
  - 总大小：默认 `3*5 + 3 + 5 = 23`

### 2.2 动作分解与含义

动作向量由5个部分组成，按顺序排列如下：

| 索引范围 | 长度 | 含义 | 转换方式 | 实际范围 |
|---------|------|------|----------|----------|
| 0:n_ues | n_ues | 卸载决策（Offload Decision） | 0.5为阈值，<0.5→0（本地执行），≥0.5→1（卸载到MEC） | {0, 1} |
| n_ues:2*n_ues | n_ues | 计算能力分配（Computation Capacity Allocation） | 归一化后按比例分配MEC计算资源 | [0, MEC_computation_capacity] |
| 2*n_ues:3*n_ues | n_ues | 传输功率列表（Transmission Power List） | 乘以UE_maximum_transmit_power | [0, UE_maximum_transmit_power] |
| 3*n_ues:3*n_ues+n_element | n_element | RIS相位变化（Phase Change） | 乘以2π | [0, 2π] |
| 3*n_ues+n_element: | 3 | UAV移动向量（Movement Vector） | 减去0.5后乘以uav_max_mov | [-uav_max_mov/2, uav_max_mov/2] |

### 2.3 详细转换过程

```python
# 动作数据处理函数
def action_data_process(self, raw_action):
    # 1. 卸载决策：二值化处理
    action_offload_decision = [(0 if i<0.5 else 1) for i in raw_action[0:self.n_ues]]
    
    # 2. 计算能力分配：按比例分配MEC资源
    action_computation_capacity_allocate = ([(i*self.bs.get_mec_current_computation_capacity())
                                            /(np.sum(np.array(raw_action[self.n_ues:2*self.n_ues])
                                            *np.array(action_offload_decision))+1e-6)
                                            for i in raw_action[self.n_ues:2*self.n_ues]])
    
    # 3. 传输功率：映射到最大传输功率
    action_transmission_power_list = [i*self.cfg['UE_maximum_transmit_power'] 
                                    for i in raw_action[2*self.n_ues:3*self.n_ues]]
    
    # 4. RIS相位变化：映射到[0, 2π]
    action_phase_change = [i*2*np.pi for i 
                            in raw_action[3*self.n_ues:3*self.n_ues+self.ris_uav.get_n_elements()]]
    
    # 5. UAV移动向量：映射到[-max_mov/2, max_mov/2]
    action_movement_vector = [(i-0.5)*self.ris_uav.get_uav_max_mov()
                                for i in raw_action[3*self.n_ues+self.ris_uav.get_n_elements():]]
    
    return (action_offload_decision, action_computation_capacity_allocate, 
            action_transmission_power_list, action_phase_change, action_movement_vector)
```

## 3. 观察空间（Observation Space）

### 3.1 基本信息

- **类型**：`gym.spaces.Box`
- **范围**：`[0, 1]`
- **数据类型**：`np.float32`
- **大小**：`4*n_ues + 4`
  - `n_ues`：用户设备数量（默认5）
  - 总大小：默认 `4*5 + 4 = 24`

### 3.2 观察分解与含义

观察向量由6个部分组成，按顺序排列如下：

| 索引范围 | 长度 | 含义 | 归一化方式 | 原始数据范围 |
|---------|------|------|------------|--------------|
| 0:n_ues | n_ues | 任务计算消耗列表（Task Computation Consumption List） | 除以2*task_comsumption_average，上限1 | [0, 2*task_comsumption_average] |
| n_ues:2*n_ues | n_ues | 任务大小列表（Task Size List） | 除以2*task_size_average，上限1 | [0, 2*task_size_average] |
| 2*n_ues:3*n_ues | n_ues | 任务时间限制列表（Task Time Limit List） | 除以最大值归一化 | [0, max_task_time_limit] |
| 3*n_ues:4*n_ues | n_ues | UE剩余执行时间列表（UE Remaining Execution Time List） | 除以20，上限1 | [0, 20] |
| 4*n_ues:4*n_ues+3 | 3 | RIS-UAV位置（RIS-UAV Position） | 按uav_area范围归一化 | uav_area范围内 |
| 4*n_ues+3: | 1 | BS-MEC当前计算能力（BS-MEC Current Computation Capacity） | 除以MEC_computation_capacity | [0, MEC_computation_capacity] |

### 3.3 详细转换过程

```python
# 观察数据处理函数
def observation_data_process(self, raw_observation):
    # 1. 任务计算消耗：归一化到[0, 1]
    observation_task_computation_consumption_list = [min(1, i/(2*self.cfg['task_comsumption_average'])) for i in raw_observation[0:self.n_ues]]
    
    # 2. 任务大小：归一化到[0, 1]
    observation_task_size_list = [min(1, i/(2*self.cfg['task_size_average'])) for i in raw_observation[self.n_ues:2*self.n_ues]]
    
    # 3. 任务时间限制：除以最大值归一化
    observation_task_time_limit_list = [i/max(raw_observation[2*self.n_ues:3*self.n_ues]) for i in raw_observation[2*self.n_ues:3*self.n_ues]]
    
    # 4. UE剩余执行时间：归一化到[0, 1]
    observation_ue_remaining_execution_time_list = [min(1, i/20) for i in raw_observation[3*self.n_ues:4*self.n_ues]]
    
    # 5. RIS-UAV位置：按区域范围归一化
    observation_ris_uav_position = [(raw_observation[4*self.n_ues+i]-self.cfg['uav_area'][0][i])/(self.cfg['uav_area'][1][i]-self.cfg['uav_area'][0][i]) for i in range(3)]
    
    # 6. BS-MEC当前计算能力：归一化到[0, 1]
    observation_bs_mec_current_computation_capacity = raw_observation[-1]/self.cfg['MEC_computation_capacity']
    
    return (observation_task_computation_consumption_list + observation_task_size_list + 
            observation_task_time_limit_list + observation_ue_remaining_execution_time_list + 
            observation_ris_uav_position + [observation_bs_mec_current_computation_capacity])
```

## 4. 原始观察数据来源

观察数据来自`RuntSystem`的`get_state()`方法，原始数据结构如下：

```python
def get_state(self):
    # 收集每个UE的状态
    task_computation_consumption_list = [i.get_task_consumption() for i in self.ue_list]
    task_size_list = [i.get_task_size() for i in self.ue_list]
    task_time_limit_list = [i.get_task_time_limit() for i in self.ue_list]
    ue_remaining_execution_time_list = [i.get_remaining_execution_time() for i in self.ue_list]
    
    # 收集RIS-UAV和BS状态
    ris_uav_position = self.ris_uav.get_position()
    bs_mec_capacity = [self.bs.get_mec_current_computation_capacity()]
    
    # 组合所有状态
    state_list = (task_computation_consumption_list + task_size_list + task_time_limit_list +
                 ue_remaining_execution_time_list + ris_uav_position + bs_mec_capacity)
    
    return state_list
```

## 5. 关键配置参数

| 参数名称 | 默认值 | 描述 |
|---------|--------|------|
| n_UE | 5 | 用户设备数量 |
| n_element | 5 | RIS反射元素数量 |
| MEC_computation_capacity | 5000 | MEC服务器计算能力 |
| UE_maximum_transmit_power | 5 | UE最大传输功率 |
| uav_max_mov | 10 | UAV最大移动距离 |
| uav_area | [[-10, -10, 0], [10, 10, 10]] | UAV活动区域 |
| task_comsumption_average | 4500 | 任务计算消耗平均值 |
| task_size_average | 450 | 任务大小平均值 |

## 6. 系统工作流程

1. **初始化**：创建`RuntBoxEnv`实例，初始化`RuntSystem`和空间定义
2. **重置**：调用`reset()`方法重置环境状态
3. **动作执行**：
   - 智能体生成动作向量（Box空间格式）
   - 调用`action_data_process()`转换为系统可执行格式
   - 调用`step()`执行动作，更新系统状态
4. **状态观察**：
   - 系统生成原始状态向量
   - 调用`observation_data_process()`转换为Box空间格式
   - 返回观察结果和奖励给智能体
5. **循环**：重复步骤3-4，直到达到终止条件

## 7. 代码优化建议

1. **参数验证**：在`action_data_process()`中添加参数范围验证，确保转换后的值在合理范围内
2. **状态归一化**：考虑使用更鲁棒的归一化方法，如使用历史最大最小值而非固定值
3. **文档完善**：为关键方法和参数添加更详细的注释
4. **性能优化**：对于大规模场景，考虑使用向量化操作替代循环
5. **灵活性提升**：允许通过配置文件自定义动作和观察空间的组成

## 8. 总结

`RuntBoxEnv`的动作空间和观察空间设计合理，能够全面反映无线通信系统中的关键状态和决策变量。通过Box空间的设计，该环境可以方便地与各种强化学习算法集成，用于研究和优化边缘计算、资源分配、RIS相位调整和UAV移动等问题。

理解动作和观察空间的详细含义对于设计有效的强化学习算法至关重要，希望本分析能够为相关研究和开发工作提供帮助。