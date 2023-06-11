from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth import get_user_model

from users.models import CustomUser

from PIL import Image

def user_directory_path(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


UserModel = get_user_model() # получение всей модели пользователей

class Follower(models.Model):
    user = models.OneToOneField(UserModel,related_name="followers", verbose_name=("User"), on_delete=models.CASCADE)
    follower_user = models.ManyToManyField(UserModel, verbose_name=("Follower"),related_name='follower_user')


class Following(models.Model):
    user = models.OneToOneField(UserModel, related_name="following",unique=False, verbose_name=("User"), on_delete=models.CASCADE)
    following_user = models.ManyToManyField(UserModel, verbose_name=("Following"), related_name='following_user')


class Posts(models.Model):
    text = models.TextField(default='') # комментарий
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # пользователь
    date = models.DateTimeField() 
    image = models.ImageField(upload_to=user_directory_path)
    likes = models.ManyToManyField(UserModel, blank=True, related_name="likes")
    dislikes = models.ManyToManyField(UserModel, blank=True, related_name="dislikes")

    product = models.BooleanField(default=False)
    price = models.FloatField(default=0)
    count = models.IntegerField(default=0)
    
    def save(self):
        super().save()  # saving image first

        max_size = 800
        img = Image.open(self.image.path)
        if img.size[1] > img.size[0]:
            height = max_size
            ratio = (height / float(img.size[1]))
            width = int((float(img.size[0]) * float(ratio)))
            img = img.resize((width, height), Image.ANTIALIAS)
        else:
            width = max_size
            ratio = (width / float(img.size[0]))
            height = int((float(img.size[1]) * float(ratio)))
            img = img.resize((width, height), Image.ANTIALIAS)

        white_img = Image.new('RGB', (800, 800), color = (255,255,255))
        x = int((white_img.size[0] - img.size[0])/2)
        y = int((white_img.size[1] - img.size[1])/2)

        white_img.paste(img,(x,y))
        white_img.save(self.image.path)


class Comments(models.Model):
    text = models.CharField(max_length=150)
    image = models.ForeignKey('Posts', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField() 
