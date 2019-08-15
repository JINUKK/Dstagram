from django.contrib import admin

from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id','author','image','created','updated']

    list_filter = ['created','updated']

    search_fields = ['created','updated','text']

    # model에서 하는 ordering은 사용자가 list 화면을 처음볼 때부터 적용됨
    ordering = ['-updated','-created']

    # 스크롤 방식이 아닌 번호로 찾을 수 있음
    raw_id_fields = ['author']

admin.site.register(Photo, PhotoAdmin)

