from django.db import models
from .rl_model import RLModel

class TrainData(models.Model):
    id = models.BigAutoField(
        primary_key=True,
        verbose_name='主键ID',
        help_text='主键ID，自增'
    )

    model = models.ForeignKey(
        RLModel,
        on_delete=models.CASCADE,
        verbose_name='关联模型',
        help_text='关联的RL模型',
        null=False
    )

    episode = models.PositiveIntegerField(
        verbose_name='训练回合数',
        help_text='训练回合数',
        null=False,
        blank=False
    )
    reward = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name='当前回合奖励值',
        help_text='当前回合奖励值',
        null=True,
        blank=True
    )
    smoothed_reward = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name='平滑奖励值',
        help_text='平滑奖励值（如滑动平均）',
        null=True,
        blank=True
    )
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        help_text='创建时间',
        auto_now_add=True,
        null=False
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        help_text='更新时间',
        auto_now=True,
        null=False
    )

    class Meta:
        db_table = 'train_data'  # 对应数据库表名
        verbose_name = '训练数据'
        verbose_name_plural = '训练数据'
        # 索引：提升模型ID查询效率
        indexes = [
            models.Index(
                fields=['model'],
                name='idx_model_id'
            )
        ]
        # 默认排序：按模型ID和回合数升序
        ordering = ['model', 'episode']