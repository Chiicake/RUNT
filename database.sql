CREATE DATABASE IF NOT EXISTS `RUNT` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `RUNT`;
CREATE TABLE `model` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '模型ID（主键，自增）',
  `target_episode` INT NOT NULL COMMENT '目标训练轮次',
  `current_episode` INT NOT NULL DEFAULT 0 COMMENT '当前训练轮次',
  `status` TINYINT NOT NULL DEFAULT 0 COMMENT '训练状态：0-训练中，1-训练完成',
  `task_size_average` DECIMAL(10, 4) DEFAULT NULL COMMENT '任务平均大小',
  `task_comsumption_average` DECIMAL(10, 4) DEFAULT NULL COMMENT '任务平均消耗（注：字段名comsumption为拼写，建议可修正为consumption）',
  `task_time_average` DECIMAL(10, 4) DEFAULT NULL COMMENT '任务平均耗时',
  `task_arrival_rate` DECIMAL(8, 4) DEFAULT NULL COMMENT '任务到达率',
  `n_UE` INT DEFAULT NULL COMMENT 'UE数量',
  `UE_computation_capacity` DECIMAL(12, 4) DEFAULT NULL COMMENT 'UE计算能力',
  `MEC_computation_capacity` DECIMAL(12, 4) DEFAULT NULL COMMENT 'MEC计算能力',
  `seed` INT DEFAULT NULL COMMENT '随机种子',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='模型信息表';