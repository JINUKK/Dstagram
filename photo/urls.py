from django.urls import path

from .views import *

app_name = 'photo'

urlpatterns = [
    path('like/<int:photo_id>/', PhotoLike.as_view(), name='like'),
    path('save/<int:photo_id>/', PhotoSave.as_view(), name='save'),
    path('like/', PhotoLikeList.as_view(), name='like_list'),
    path('save/', PhotoSaveList.as_view(), name='save_list'),

    path('mypage/', PhotoMyPageList.as_view(), name='mypage_list'),

    path('', PhotoList.as_view(), name = 'index'),
    path('create/', PhotoCreate.as_view(), name = 'create'),
    path('update/<int:pk>', PhotoUpdate.as_view(), name = 'update'),
    path('delete/<int:pk>', PhotoDelete.as_view(), name = 'delete'),
    path('detail/<int:pk>', PhotoDetail.as_view(), name = 'detail'),

    # path('', PhotoListView.as_view()),
]