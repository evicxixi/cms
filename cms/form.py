from django import forms
from django.forms import widgets
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from cms.models import UserInfo


class UserForm(forms.Form):
    wid = widgets.PasswordInput(
        attrs={'class': 'form-control form-control-sm'})
    attrs = {'class': 'form-control form-control-sm'}
    username = forms.CharField(  # CharField为渲染此标签时
        max_length=150,
        label='用户名',  # 类似标注 前端渲染时供用户辨别
        widget=widgets.TextInput(attrs=dict(
            attrs, **{'placeholder': 'UserName'}))
    )
    password = forms.CharField(
        max_length=16,
        label='密码',
        widget=widgets.TextInput(attrs=dict(
            attrs, **{'placeholder': 'Password'})),
    )
    re_password = forms.CharField(
        max_length=16,
        label='再次输入密码',
        widget=widgets.TextInput(attrs=dict(
            attrs, **{'placeholder': 'Re Password'})),
    )
    first_name = forms.CharField(
        max_length=30,
        widget=widgets.TextInput(attrs=dict(
            attrs, **{'placeholder': 'First Name'}))
    )
    last_name = forms.CharField(
        max_length=150,
        widget=widgets.TextInput(attrs=dict(
            attrs, **{'placeholder': 'Last Name'}))
    )
    email = forms.EmailField(
        max_length=254,
        widget=widgets.EmailInput(attrs=dict(
            attrs, **{'placeholder': 'Email'}))
    )

    # 自定义校验规则(局部钩子)
    def clean_username(self):  # 方法名称格式必须为cleand_FieldName
        username = self.cleaned_data.get('username')
        user_obj = UserInfo.objects.filter(username=username)
        if username.isdigit():
            raise ValidationError('用户名不能为纯数字')
        elif user_obj:
            raise ValidationError('用户名已存在')
        else:
            return username

    # 自定义校验规则(全局钩子)
    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password == re_password:
            return self.cleaned_data
        else:
            raise ValidationError('密码不一致')
