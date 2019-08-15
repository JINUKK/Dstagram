from django.shortcuts import render

from .models import Photo

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView

from django.views.generic.base import View
from django.http import HttpResponseForbidden

from django.http import HttpResponseRedirect
from django.contrib import messages

from django.urls import reverse

from urllib.parse import urlparse

# 뷰를 실행하기 전에 특정한 로직을 추가로 실행하고 싶다면?
# 로그인 여부, csrf 체크를 수행할 것인가?
# 믹스인 : 클래스형 뷰
# 데코레이터 : 함수형 뷰
from django.contrib.auth.mixins import LoginRequiredMixin
# LoginRequiredMixin : 로그인을 해야만 실행할 수 있게 해준다.

# Create your views here.
# CRUDL - 이미지를 띄우는 방법
# 제네릭 뷰 활용
# 쿼리셋 변경하기, context_data 추가하기, 권한 체크
# 함수형 뷰 <-> 클래스형 뷰

class PhotoList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'  # 파일 이름 전체를 지정

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return HttpResponseRedirect(reverse('accounts:signin'))
    #     else:
    #         return super(PhotoList, self).dispatch(request, *args, **kwargs)

class PhotoLikeList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         messages.warning(request, "접근 권한이 없습니다.")
    #         return HttpResponseRedirect('/')
    #     else:
    #         return super(PhotoLikeList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # 로그인한 유저가 좋아요를 클릭한 글을 찾아서 반환
        user = self.request.user
        queryset = user.like_post.all()
        return queryset

class PhotoSaveList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         messages.warning(request, "접근 권한이 없습니다.")
    #         return HttpResponseRedirect('/')
    #     else:
    #         return super(PhotoSaveList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = user.save_post.all()
        return queryset

class PhotoMyPageList(LoginRequiredMixin, ListView):
    Model = Photo
    template_name = 'photo/photo_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = user.photos.all()
        return queryset

from django.shortcuts import redirect

class PhotoCreate(CreateView):
    model = Photo

    fields = ['text', 'image']
    template_name = 'photo/photo_create.html'
    # template_name_suffix = '_create' # 뒤에 붙는 이름만 바꿈
    success_url = '/'

    def form_valid(self, form):
        # 입력된 자료가 올바른지 체크
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            # 올바르다면
            # form : 모델 폼
            # form.instance는 model의 객체
            form.instance.save()
            return redirect('/')
        else:
            # 올바르지 않다면
            return self.render_to_response({'form':form})

class PhotoUpdate(UpdateView):
    model = Photo

    fields = ['text', 'image']
    template_name = 'photo/photo_update.html'
    # success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author !=request.user:
            # 삭제 페이지에서 권한이 없다!
            # 원래 디테일 페이지로 돌아가서 삭제에 실패했다!
            # 사용자가 선택할 수 없는 기능들은 눈에 안보이게 하는 것이 좋다.
            messages.warning(request, "수정할 권한이 없습니다.")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)

class PhotoDelete(DeleteView):
    model = Photo
    template_name = 'photo/photo_delete.html'
    success_url = '/'

    # Life Cycle - iOS, Android, Vue, React, Django, Rails
    # Framework는 라이프 사이클이 존재 : 어떤 순서로 구동이 되느냐?
    # URLConf -> View -> Model 순으로
    # 어떤 뷰를 구동할 때 그 안에서 동작하는 순서

    # 사용자가 접속했을 때, get? post? 등을 결정하고 분기하는 부분
    # 로직을 수행하고, 템플릿을 랜더링한다.
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author !=request.user:
            # 삭제 페이지에서 권한이 없다!
            # 원래 디테일 페이지로 돌아가서 삭제에 실패했다!
            # 사용자가 선택할 수 없는 기능들은 눈에 안보이게 하는 것이 좋다.
            messages.warning(request, "삭제할 권한이 없습니다.")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

    # get과 post는 세트
    # get과 post는 로직을 수행하고, 템플릿을 렌더링한다.
    # def get(self, request, *args, **kwargs):
    #     object = self.get_object()
    #     if object.author != request.user:
    #
    #         messages.warning(request, "삭제할 권한이 없습니다.")
    #
    #         return HttpResponseRedirect(object.get_absolute_url())
    #     else:
    #         return super(PhotoDelete, self).get(request, *args, **kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     object = self.get_object()
    #
    #     if object.author != request.user:
    #         messages.warning(request, "삭제할 권한이 없습니다.")
    #
    #         return HttpResponseRedirect(object.get_absolute_url())
    #     else:
    #         return super(PhotoDelete, self).get(request, *args, **kwargs)

    # def get_object(self, queryset=None):
        # 해당 쿼리셋을 이용해서 현재 페이지에 필요한 object를 인스턴스화 한다.
        # pass

    # def get_queryset(self):
        # 어떻게 데이터를 가져올 것인가?
        # pass

class PhotoDetail(DetailView):
    model = Photo
    template_name = 'photo/photo_detail.html'

class PhotoLike(View):
    def get(self, request, *args, **kwargs):
        # like를 할 정보가 있다면 진행, 없다면 증단
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            # 1. 어떤 포스팅?
            # url : www.naver.com/blog/like/?photo_id=1
            # request.GET.get('photo_id')
            # url : www.naver.com/blog/like/1/
            # path('blog/like/<int:photo_id>')
            # kwargs['photo_id']
            # 2. 누가?
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user

                if user not in photo.like.all():
                    photo.like.add(user)
                else:
                    photo.like.remove(user)

            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path) # 도메인 주소 필요없이 경로만 필요하다.

class PhotoSave(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user

                if user not in photo.favorite.all():
                    photo.favorite.add(user)
                else:
                    photo.favorite.remove(user)

            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)

# signal
# ~하기 전에, ~한 후에 발생하는 일들을 말함
# 후속 조치를 하는 것
# 대표적인 signal 종류
# pre_save : 저장하기 전
# post_save : 저장한 후
# pre_delete : 지우기 전
# post_delete : 지운 후
# 1. 어떤 시그널이 발생했을 때 반응할 것인가?
# 2. 그 시그널이 발생한 것을 어떻게 알았나?
from django.db.models.signals import post_delete
from django.dispatch import receiver

import boto3
from django.conf import settings

# @receiver(어떤 시그널이 발생했는가?, 누가 발생시켰는가?)
# sender가 없다면 모든 경우에 post_delete가 발생
# sender=Photo를 해줌으로써 Photo가 있는 경우에만 발생
@receiver(post_delete, sender=Photo)
def post_delete(sender, instance, **kwargs):
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    # s3.Objects는 s3에 업로드된 파일 객체를 얻어오는 클래스
    # arg1 = 버킷네임
    # arg2 = 파일 경로 - Key
    s3 = session.resource('s3') # s3 권한 가져오기
    image = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, "media/"+str(instance.image))
    image.delete()
