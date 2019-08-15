from django.shortcuts import render

# 유저 목록이 출력되는 뷰
# + Follow라는 기능 추가
# 중간 테이블을 직접 생성 - 모델

# 유저 모델을 커스터마이징해야 한다. -> 1. 커스터마이징 하는 방법을 배운다.
# 확장하는 방법에 따라서
# 1) 새로운 유저 모델을 만드는 방법 - 기존 유저 데이터를 유지할 수가 없다.
# 2) 기존 모델을 확장하는 방법 - DB 다운 타임 alter table을 하면 table lock이 걸린다.
# -> 두 방법 다 운영하는 중간 입장에서는 위험한 방법이다.

# 유저 모델(나)
# 나를 팔로우한 사람 필드
# 내가 팔로우한 사람 필드

# 하지만 커스터마이징 할 수 없다면?
# 새로운 모델을 추가하는 방법

# 사진 모델
# 사진을 좋아요한 사람 필드
# 사진을 저장한 사람 필드


"""
팔로우 기능 구현
1. 유저 목록 혹은 유저 프로필에서 팔로우 버튼
1-1. 전체 유저 목록을 출력하는 뷰 - User 모델에 대한 ListView
2. 팔로우 정보를 저장하는 뷰
"""

from django.views.generic.list import ListView
from django.views.generic.base import View

from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.contrib import messages

from django.urls import reverse

from urllib.parse import urlparse

from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User, Follow

class UserList(ListView):
    model = User
    template_name = 'accounts/user_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:signin'))
        else:
            return super(UserList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.exclude(id=user.id)

        return queryset


class FollowerList(LoginRequiredMixin, ListView):
    Model = User
    template_name = 'accounts/follow_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = user.follower.all()
        user_list = []
        for idx in queryset:
            user_list.append(idx.me)
        return user_list

class FollowingList(LoginRequiredMixin, ListView):
    Model = User
    template_name = 'accounts/follow_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = user.following.all()
        user_list = []
        for idx in queryset:
            user_list.append(idx.you)
        return user_list

class FollowButton(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'user_id' in kwargs:
                user_id = kwargs['user_id']
                follow_user = User.objects.get(pk=user_id)
                login_user = request.user

                if not login_user == follow_user:
                    follow_filter = Follow.objects.filter(me=login_user, you=follow_user)

                    if follow_filter:
                        follow_filter[0].delete()
                    else:
                        Follow(me=login_user, you=follow_user).save()


            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)

# 기존에 입력받는 뷰 - CreateView 상속 받아서
# 상속받아서 만들면 커스텀이 힘들다.
# 회원가입 -> User 모델에 값을 입력받는다.-> CreateView
# 회원가입시 모델 필드 외에 추가 입력이 필요하다.
# 커스텀 뷰를 하려면 함수형 뷰가 적절하겠다.

from .forms import SignUpForm
def signup(request):
    # 함수형 뷰에서는 매개변수 request가 꼭 있어야 한다.
    # Class Based View였다면 dispatch -> get, post
    if request.method == "POST":
        # Todo : 입력 받은 내용을 이용해서 회원 객체 생성
        # 입력받은 내용 확인하기
        # 모델 폼을 이용해서 코드를 간결하게 바꾼다.
        # validation - 아이디가 중복되는지, 아이디가 한글은 아닌지

        signup_form = SignUpForm(request.POST) # 폼에 내용이 채워져 있는 형태로 출력됨

        # form validation이 진행되지 않은 채로 저장하게 되기 때문에...
        if signup_form.is_valid():
            # 1. 저장하고 인스턴스 생성
            user_instance = signup_form.save(commit=False) # 해당 입력받은 정보를 가지고 인스턴스를 만들어줌
            # commit=False 옵션을 통해 데이터베이스에는 저장이 안되도록 함
            # 2. 패스워드 암호화 -> 저장
            # 폼이 가지고 있는 cleaned_data는 무엇인가? : 유효한 문자만 남긴 상태로 처리 과정을 거친 데이터
            # request.POST.get('password') <- 이런 방법으로 받지 않는다.
            user_instance.set_password(signup_form.cleaned_data['password'])
            user_instance.save()

            return render(request, 'accounts/signup_complete.html', {'username':user_instance.username})
            # username을 던져줌. 'username'이 html에서 쓰일 이름/ 뒤에 user_instance.username이 html로 넘기는 값

        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        # email = request.POST.get('email')
        # print(username, password, first_name, last_name, email)
        # # 회원 객체 생성하기
        # user = User()
        # user.username = username
        # # user.password = password # set_password()를 쓰지 않고 저장하면 암호화되지 않은채 저장된다.
        # user.set_password(password) # 비밀번호를 비밀번호화 시켜주는 메서드
        # user.first_name = first_name
        # user.last_name = last_name
        # user.email = email
        # user.save()
    else:
        # Todo : form 객체를 만들어서 전달
        # form에는 username, password만 입력 받으면 된다.

        signup_form = SignUpForm()
        # 1. 템플릿 불러오기
        # 2. 템플릿 렌더링하기
        # 3. HTTP Response하기
    return render(request, 'accounts/signup.html', {'form':signup_form}) # 변수값 전달 방법
