from django.contrib import admin
from .models import User, Follow
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):

    # fieldsets - 상세 화면에서 출력될 수정 폼 설정
    # add_fieldsets - 추가 화면에 출력될 입력 폼의 설정
    UserAdmin.fieldsets[1][1]['fields']+=('profile','message')

    UserAdmin.add_fieldsets += (
        (('Additional Info'), {'fields':('profile','message')}),
    )

class FollowOption(admin.ModelAdmin):
    list_display = ['id', 'me', 'you']
    raw_id_fields = ['me', 'you']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Follow, FollowOption)
