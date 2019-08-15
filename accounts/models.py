from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    message = models.TextField(blank=True)
    profile = models.ImageField(upload_to='user_images/profile/%Y/%m/%d', blank=True)

    class Meta:
        ordering = ['id']


class Follow(models.Model):
    # 2개 필드 = ForeignKey
    # A가 B를 팔로우 하고 있다.
    # on_delete = 연관된 객체가 삭제된다면 어떻게 할 것인가?
    # related_name은 참조 객체의 입장에서 필드명, 속성값
    me = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')  # 내가 팔로잉한 사람들
    you = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')  # 나를 팔로워한 사람들

    def __str__(self):
        return self.me.username + " follow " + self.you.username
