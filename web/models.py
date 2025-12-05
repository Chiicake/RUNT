from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        # 直接保存原始密码，不进行加密
        super(User, self).save(*args, **kwargs)
    
    def check_password(self, raw_password):
        # 直接比较原始密码
        return raw_password == self.password
