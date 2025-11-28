from django.db import models


class RLModel(models.Model):
    """模型信息表"""
    # 状态选择项（规范状态值）
    TRAINING = 0
    COMPLETED = 1
    STATUS_CHOICES = (
        (TRAINING, '训练中'),
        (COMPLETED, '训练完成'),
    )

    id = models.BigAutoField(primary_key=True, verbose_name='模型ID')
    target_episode = models.IntegerField(verbose_name='目标训练轮次')
    current_episode = models.IntegerField(default=0, verbose_name='当前训练轮次')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=TRAINING, verbose_name='训练状态')
    task_size_average = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='任务平均大小')
    # 修正字段拼写错误，通过db_column映射数据库原字段名
    task_consumption_average = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True,
        db_column='task_comsumption_average', verbose_name='任务平均消耗'
    )
    task_time_average = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='任务平均耗时')
    task_arrival_rate = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True, verbose_name='任务到达率')
    n_UE = models.IntegerField(null=True, blank=True, verbose_name='UE数量')
    UE_computation_capacity = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='UE计算能力')
    MEC_computation_capacity = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='MEC计算能力')
    seed = models.IntegerField(null=True, blank=True, verbose_name='随机种子')

    class Meta:
        db_table = 'model'  # 指定数据库表名
        verbose_name = '模型信息'
        verbose_name_plural = '模型信息'
        db_table_comment = '模型信息表'  # Django 3.2+支持表注释