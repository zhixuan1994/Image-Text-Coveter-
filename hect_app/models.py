from django.db import models

class User(models.Model):
    gender = (
        ('male','M'),
        ('female','Fe')
    )
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='male')
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering= ['c_time']
        verbose_name = 'user'
        verbose_name_plural = 'user'

class Img(models.Model):
    user_name = models.CharField(max_length=128)
    img_name = models.CharField(max_length=128)
    img_url = models.ImageField(upload_to='img')

class Text(models.Model):
    img_name = models.CharField(max_length=128)
    img_url = models.CharField(max_length=128)
    user_name = models.CharField(max_length=128)
    text_content = models.CharField(max_length=512)



