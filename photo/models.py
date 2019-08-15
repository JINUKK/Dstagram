from django.db import models

# Create your models here.
# 기본 모델
"""

작성자 : author
본문글 : text
사진 : image
작성일 : created
수정일 : updated

+ tag, like
--> comment
"""
# User 모델은 확장 가능
# settings.AUTH_USER_MODEL
from django.contrib.auth import get_user_model

# url pattern 이름을 가지고 주소를 만들어주는 함수
from django.urls import reverse

User = get_user_model()

# models.Model이 ORM 가능을 가지고 있어서 상속받아서 그 기능을 이용
class Photo(models.Model):
    # ForeignKey(연결되는 모델, 삭제 시 동작, 연관 이름)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')

    # User 모델을 커스텀했을 시에 models.ForeignKey(get_user_model(),)를 쓰는 것이 좋다.

    # CASCADE : 연속해서 지운다. = 탈퇴하면 사진도 싹 지운다.
    # PROTECT : 사진을 다 지우지 않으면 탈퇴할 수 없다. = 탈퇴 프로세스에 사진을 우선 삭제하고 탈퇴 시킨다는 메시지를 띄움
    # 특정값으로 셋팅하는 방법도 있음

    # related_name으로 연관 데이터를 얻을 수 없다면 쿼리를 별도로 실행해야 한다,
    # 내 프로필 페이지에서 내가 올린 사진만 뜬다. -> related_name을 이용하여 별도의 퀴리없이도 불러올 수 있다.

    text = models.TextField(blank=True) # 필수 필드가 아닐 수 있기 때문에 blank = True
    image = models.ImageField(upload_to='timeline_photo/%Y/%m/%d')
    # %Y = 2019로 표시
    # %y = 19로 표시
    # upload_to는 함수를 사용해서 폴더를 동적으로 설정할 수 있다.
    # pip install pillow 설치

    created = models.DateTimeField(auto_now_add= True) # 생성 당시에 날짜를 저장
    updated = models.DateTimeField(auto_now=True) # 다시 생성할 때마다 날짜 갱신

    like = models.ManyToManyField(User, related_name='like_post', blank=True)

    # save라는 변수를 사용하면 안되는 이유
    # 예약어를 필드명을 사용하면 안된다.
    favorite = models.ManyToManyField(User, related_name='save_post', blank=True)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        # detail/<int:pk>/
        # <int:pk>에 들어갈 값을 아래와 같이 args=[self.id] 방법으로 넣어준다.
        return reverse('photo:detail', args=[self.id])

    # save를 실행하고 나면 DB에 레코드 생성
    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     pass
        # save를 하기전에 어떠한 것을 하고 싶다면 여기에 입력
        # super(Photo,self).save()
        # save를 하고나서 어떠한 것을 하고 싶다면 여기에 입력

    # delete를 실행하고 나면 DB에서 레코드 제거
    # def delete(self, using=None, keep_parents=False):
    #     pass
    #     delete를 하기전에 어떠한 것을 하고 싶다면 여기에 입력
        # super(Photo,self).delete()
        # delete를 하고나서 어떠한 것을 하고 싶다면 여기에 입력