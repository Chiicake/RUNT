from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        # 保存密码时进行加密
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
    
    def check_password(self, raw_password):
        # 验证密码
        return check_password(raw_password, self.password)
