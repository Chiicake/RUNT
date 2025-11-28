from django.db import models

class RLModel(models.Model):
    STATUS_TRAINING = 0  # 训练中
    STATUS_COMPLETED = 1  # 训练完成
    STATUS_CHOICES = (
        (STATUS_TRAINING, '训练中'),
        (STATUS_COMPLETED, '训练完成'),
    )

    id = models.BigAutoField(
        primary_key=True,
        verbose_name='主键ID',
        help_text='主键ID，自增'
    )
    algorithm = models.CharField(
        max_length=100,
        verbose_name='算法名称',
        help_text='算法名称（如DQN、PPO等）',
        null=False,
        blank=False
    )
    target_episode = models.PositiveIntegerField(
        verbose_name='目标训练回合数',
        help_text='目标训练回合数',
        null=False,
        blank=False
    )
    current_episode = models.PositiveIntegerField(
        verbose_name='当前训练回合数',
        help_text='当前训练回合数',
        default=0,
        null=False,
        blank=False
    )
    status = models.SmallIntegerField(
        verbose_name='训练状态',
        help_text='训练状态：0-训练中，1-训练完成',
        choices=STATUS_CHOICES,
        default=STATUS_TRAINING,
        null=False,
        blank=False
    )
    task_size_average = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name='任务平均大小',
        help_text='任务平均大小',
        null=True,
        blank=True
    )
    task_comsumption_average = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name='任务平均消耗',
        help_text='任务平均消耗',
        null=True,
        blank=True
    )
    task_time_average = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name='任务平均耗时',
        help_text='任务平均耗时',
        null=True,
        blank=True
    )
    task_arrival_rate = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        verbose_name='任务到达率',
        help_text='任务到达率',
        null=True,
        blank=True
    )
    n_UE = models.PositiveIntegerField(
        verbose_name='用户设备(UE)数量',
        help_text='用户设备(UE)数量',
        null=True,
        blank=True
    )
    UE_computation_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='UE计算能力',
        help_text='UE计算能力',
        null=True,
        blank=True
    )
    MEC_computation_capacity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='MEC服务器计算能力',
        help_text='MEC服务器计算能力',
        null=True,
        blank=True
    )
    seed = models.PositiveIntegerField(
        verbose_name='随机种子',
        help_text='随机种子',
        null=True,
        blank=True
    )
    learning_rate = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        verbose_name='学习率',
        help_text='学习率',
        null=True,
        blank=True
    )
    batch_size = models.PositiveIntegerField(
        verbose_name='批次大小',
        help_text='批次大小',
        null=True,
        blank=True
    )
    buffer_size = models.PositiveBigIntegerField(
        verbose_name='经验回放缓冲区大小',
        help_text='经验回放缓冲区大小',
        null=True,
        blank=True
    )
    gamma = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        verbose_name='折扣因子γ',
        help_text='折扣因子γ',
        null=True,
        blank=True
    )
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        help_text='创建时间',
        auto_now_add=True,  # 自动设为创建时的时间，不可修改
        null=False
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        help_text='更新时间',
        auto_now=True,  # 自动设为每次保存时的时间
        null=False
    )

    class Meta:
        db_table = 'rl_model'  # 对应数据库表名
        verbose_name = '强化学习模型参数'
        verbose_name_plural = '强化学习模型参数'
        db_comment = '强化学习模型参数表'  # Django 3.2+ 支持表注释
        ordering = ['-create_time']  # 默认按创建时间倒序