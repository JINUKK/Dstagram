from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import UserList, FollowerList, FollowingList, FollowButton, signup

app_name = 'accounts'

urlpatterns = [
    path('user/list/', UserList.as_view(), name='user_list'),
    path('follower/list/', FollowerList.as_view(), name='follower_list'),
    path('following/list/', FollowingList.as_view(), name='following_list'),

    path('follow/<int:user_id>/', FollowButton.as_view(), name='follow_button'),
    path('singin/', LoginView.as_view(template_name='accounts/signin.html'), name='signin'),
    path('signout/', LogoutView.as_view(template_name='accounts/signout.html'), name='signout'),
    path('signup/', signup, name='signup'), # 함수형 뷰는 이름만 쓴다.
]