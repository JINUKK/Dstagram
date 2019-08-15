# 모델 폼을 만드려면 2가지 필요하다.
# 제네릭 뷰: 제네릭 뷰, 모델
# 모델 폼 : 모델, 폼

from .models import User
from django import forms

class SignUpForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput) # 추가 필드

    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        # fields에는 해당 모델에 대해 입력받을 필드들을 나열한다.
        # + 추가 필드도 포함될 수 있다. -> 필드 목록과 추가 필드가 겹치면 오버라이드(추가 필드의 우선순위가 높다)
        # fields에 써준 순서대로 출력한다.
        fields = ['username','password','password2','first_name','last_name','email'] # 입력받을 필드명을 입력
        # fields = '__all__' # 전체 다 부르고 싶을 경우

        # Todo : 필드의 기본값, Placeholder 설정법, css Class 설정법법, validator 설정법법, help text 설정
        # Todo : 커스텀 필드 만드는 법

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        # 항상 해당 필드의 값을 리턴한다.
        return cd['password2']