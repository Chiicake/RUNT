CREATE DATABASE IF NOT EXISTS `RUNT` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `RUNT`;
CREATE TABLE IF NOT EXISTS `rl_model` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID，自增',
  `algorithm` VARCHAR(100) NOT NULL COMMENT '算法名称',
  `target_episode` INT UNSIGNED NOT NULL COMMENT '目标训练回合数',
  `current_episode` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '当前训练回合数',
  `status` TINYINT NOT NULL DEFAULT 0 COMMENT '训练状态：0-训练中，1-训练完成',
  `task_size_average` DECIMAL(10, 4) DEFAULT NULL COMMENT '任务平均大小',
  `task_comsumption_average` DECIMAL(10, 4) DEFAULT NULL COMMENT '任务平均消耗',
  `task_time_average` DECIMAL(10, 4) DEFAULT NULL COMMENT '任务平均耗时',
  `task_arrival_rate` DECIMAL(8, 4) DEFAULT NULL COMMENT '任务到达率',
  `n_UE` INT UNSIGNED DEFAULT NULL COMMENT '用户设备(UE)数量',
  `UE_computation_capacity` DECIMAL(10, 2) DEFAULT NULL COMMENT 'UE计算能力',
  `MEC_computation_capacity` DECIMAL(12, 2) DEFAULT NULL COMMENT 'MEC服务器计算能力',
  `seed` INT UNSIGNED DEFAULT NULL COMMENT '随机种子',
  `learning_rate` DECIMAL(8, 6) DEFAULT NULL COMMENT '学习率',
  `batch_size` INT UNSIGNED DEFAULT NULL COMMENT '批次大小',
  `buffer_size` BIGINT UNSIGNED DEFAULT NULL COMMENT '经验回放缓冲区大小',
  `gamma` DECIMAL(8, 6) DEFAULT NULL COMMENT '折扣因子γ',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='强化学习模型参数表';

CREATE TABLE IF NOT EXISTS `training_data` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID，自增',
  `model_id` BIGINT UNSIGNED NOT NULL COMMENT '关联模型ID（外键）',
  `episode` INT UNSIGNED NOT NULL COMMENT '训练回合数',
  `reward` DECIMAL(10, 4) DEFAULT NULL COMMENT '当前回合奖励值',
  `smoothed_reward` DECIMAL(10, 4) DEFAULT NULL COMMENT '平滑奖励值（如滑动平均）',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_model_episode` (`model_id`, `episode`) COMMENT '保证同一模型同一回合数据唯一',
  KEY `idx_model_id` (`model_id`) COMMENT '模型ID索引，提升查询效率',
  CONSTRAINT `fk_train_data_model_id` FOREIGN KEY (`model_id`) REFERENCES `rl_model` (`id`) ON DELETE CASCADE ON UPDATE CASCADE COMMENT '关联rl_model表主键'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='强化学习训练数据表';

CREATE TABLE IF NOT EXISTS `train_data` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID，自增',
  `model_id` BIGINT UNSIGNED NOT NULL COMMENT '关联模型ID（外键）',
  `episode` INT UNSIGNED NOT NULL COMMENT '训练回合数',
  `reward` DECIMAL(10, 4) DEFAULT NULL COMMENT '当前回合奖励值',
  `smoothed_reward` DECIMAL(10, 4) DEFAULT NULL COMMENT '平滑奖励值（如滑动平均）',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_model_episode` (`model_id`, `episode`) COMMENT '保证同一模型同一回合数据唯一',
  KEY `idx_model_id` (`model_id`) COMMENT '模型ID索引，提升查询效率'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='强化学习训练数据表';

