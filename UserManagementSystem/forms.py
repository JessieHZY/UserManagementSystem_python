
from django import forms
from django.contrib import auth
from django.contrib.auth import get_user_model
# from UserManagementSystem.models import User,RoleList,PermissionList
from UserManagementSystem.models import User
from django.utils.safestring import mark_safe
from  django.forms import fields
from  django.core.validators import RegexValidator
# from .base import Base
# from repository import models
from django.core.exceptions import  ValidationError
from django.forms import widgets
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField
class LoginUserForm(forms.Form):
    username = forms.CharField(label=u'账 号',error_messages={'required':u'账号不能为空'},
        widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=u'密 码',error_messages={'required':u'密码不能为空'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None

        super(LoginUserForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]
        is_user_existed=User.objects.filter(username=username)
        if is_user_existed is None:
            raise forms.ValidationError(u'账户不存在，请先注册')
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username,password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'账号不存在或账号密码不匹配')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'此账号已被禁用')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=u'原始密码',error_messages={'required':'请输入原始密码'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(label=u'新密码',error_messages={'required':'请输入新密码'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label=u'确认密码',error_messages={'required':'请重复新输入密码'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        
    # def __init__(self, *args, **kwargs):
    #     super(ChangePasswordForm, self).__init__(*args, **kwargs)
    #     # self.user = 
    #     self.fields['username'].widget = widgets.TextInput

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(u'原密码错误')
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if len(password1)<6:
            raise forms.ValidationError(u'密码必须大于6位')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u'两次密码输入不一致')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
            # from UserManagementSystem.models import User
            # self.Uer.save()
        return self.user

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = ('username','password','email','nickname','sex','role','is_active')
        fields = ('username','first_name','last_name','email','is_active')
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'password' : forms.PasswordInput(attrs={'class':'form-control'}),
            'email' : forms.TextInput(attrs={'class':'form-control'}),
            # 'email' : forms.EmailInput(attrs={'class':'form-control'}),
            # 'nickname' : forms.TextInput(attrs={'class':'form-control'}),
            # 'sex' : forms.RadioSelect(choices=((u'男', u'男'),(u'女', u'女')),attrs={'class':'list-inline'}),
            # 'role' : forms.Select(attrs={'class':'form-control'}),
            'is_active' : forms.Select(choices=((True, u'启用'),(False, u'禁用')),attrs={'class':'form-control'}),
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
        }
        

    def __init__(self,*args,**kwargs):
        super(AddUserForm,self).__init__(*args,**kwargs)
        self.fields['username'].label=u'账 号'
        self.fields['username'].error_messages={'required':u'请输入账号'}
        self.fields['password'].label=u'密 码'
        self.fields['password'].error_messages={'required':u'请输入密码'}
        self.fields['email'].label=u'邮 箱'
        self.fields['email'].error_messages={'required':u'请输入邮箱','invalid':u'请输入有效邮箱'}
        # self.fields['nickname'].label=u'姓 名'
        # self.fields['nickname'].error_messages={'required':u'请输入姓名'}
        # self.fields['sex'].label=u'性 别'
        # self.fields['sex'].error_messages={'required':u'请选择性别'}
        self.fields['first_name'].label=u'名 字'
        self.fields['first_name'].error_messages={'required':u'请输入名字'}
        self.fields['last_name'].label=u'姓 氏'
        self.fields['last_name'].error_messages={'required':u'请输入姓氏'}
        # self.fields['role'].label=u'角 色'
        self.fields['is_active'].label=u'状 态'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError(u'密码必须大于6位')
        return password

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = ('username','email','nickname','sex','role','is_active')
        fields = ('username','first_name','last_name','email','is_active')
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            # 'username' : forms.CharField(label='username',max_length=50,required=False),
            #'password': forms.HiddenInput,
            # 'nickname' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.TextInput(attrs={'class':'form-control'}),
            # 'email' : forms.EmailInput(attrs={'class':'form-control'}),
            # 'sex' : forms.RadioSelect(choices=((u'男', u'男'),(u'女', u'女')),attrs={'class':'list-inline'}),
            # 'role' : forms.Select(choices=[(x.name,x.name) for x in RoleList.objects.all()],attrs={'class':'form-control'}),
            'is_active' : forms.Select(choices=((True, u'启用'),(False, u'禁用')),attrs={'class':'form-control'}),
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self,*args,**kwargs):
        super(EditUserForm,self).__init__(*args,**kwargs)
        self.fields['username'].label=u'账 号'
        self.fields['username'].error_messages={'required':u'请输入账号'}
        # self.fields['nickname'].label=u'姓 名'
        # self.fields['nickname'].error_messages={'required':u'请输入姓名'}
        self.fields['first_name'].label=u'名 字'
        self.fields['first_name'].error_messages={'required':u'请输入名字'}
        self.fields['last_name'].label=u'姓 氏'
        self.fields['last_name'].error_messages={'required':u'请输入姓氏'}
        self.fields['email'].label=u'邮 箱'
        self.fields['email'].error_messages={'required':u'请输入邮箱','invalid':u'请输入有效邮箱'}
        #有效邮箱是指邮箱必须带有@和.com且二者之间有符号
        # self.fields['sex'].label=u'性 别'
        # self.fields['sex'].error_messages={'required':u'请选择性别'}
        # self.fields['role'].label=u'角 色'
        self.fields['is_active'].label=u'状 态'

    def clean_password(self):
        return self.cleaned_data['password']


# class PermissionListForm(forms.ModelForm):
#     class Meta:
#         model = PermissionList
#         widgets = {
#             'name' : forms.TextInput(attrs={'class':'form-control'}),
#             'url' : forms.TextInput(attrs={'class':'form-control'}),
#         }

#     def __init__(self,*args,**kwargs):
#         super(PermissionListForm,self).__init__(*args,**kwargs)
#         self.fields['name'].label=u'名 称'
#         self.fields['name'].error_messages={'required':u'请输入名称'}
#         self.fields['url'].label=u'URL'
#         self.fields['url'].error_messages={'required':u'请输入URL'}

# class RoleListForm(forms.ModelForm):
#     class Meta:
#         model = RoleList
#         widgets = {
#             'name' : forms.TextInput(attrs={'class':'form-control'}),
#             'permission' : forms.SelectMultiple(attrs={'class':'form-control','size':'10','multiple':'multiple'}),
#             #'permission' : forms.CheckboxSelectMultiple(choices=[(x.id,x.name) for x in PermissionList.objects.all()]),
#         }

#     def __init__(self,*args,**kwargs):
#         super(RoleListForm,self).__init__(*args,**kwargs)
#         self.fields['name'].label=u'名 称'
#         self.fields['name'].error_messages={'required':u'请输入名称'}
#         self.fields['permission'].label=u'URL'
#         self.fields['permission'].required=False

# class RegisterForm(forms.Form):
#     username = forms.CharField(label=u'账号',error_messages={'required':'请输入账号'},
#     widget=forms.TextInput(attrs={'class':'form-control'}))
#     password1 = forms.CharField(label=u'密码',error_messages={'required':'请输入密码'},
#     widget=forms.PasswordInput(attrs={'class':'form-control'}))
#     password2 = forms.CharField(label=u'确认密码',error_messages={'required':'请重复输入密码'},
#     widget=forms.PasswordInput(attrs={'class':'form-control'}))

#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super(RegisterForm, self).__init__(*args, **kwargs)

#     def clean_username(self):
#         username = self.cleaned_data["username"]
#         is_user_existed=User.objects.filter(username=username)
#         if is_user_existed:
#             raise forms.ValidationError(u'账户名已被占用')
#         return username

#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if len(password1)<6:
#             raise forms.ValidationError(u'密码必须大于6位')

#         if password1 and password2:
#             if password1 != password2:
#                 raise forms.ValidationError(u'两次密码输入不一致')
#         return password2

#     def save(self, commit=True):
#         self.user.set_password(self.cleaned_data['password1'])
#         if commit:
#             self.user.save()
#             # from UserManagementSystem.models import User
#             # self.Uer.save()
#         return self.user


class RegisterForm(forms.Form):
    username = forms.CharField(label=u'账号',error_messages={'required':'请输入账号'},
    widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label=u'密码',error_messages={'required':'请输入密码'},
    widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label=u'确认密码',error_messages={'required':'请重复输入密码'},
    widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(label=u'邮箱',error_messages={'required':u'请输入邮箱','invalid':u'请输入有效邮箱'},
    widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]
        is_user_existed=User.objects.filter(username=username)
        if is_user_existed:
            raise forms.ValidationError(u'账户名已被占用')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if len(password1)<6:
            raise forms.ValidationError(u'密码必须大于6位')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u'两次密码输入不一致')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password1'])
        if commit:
            self.user.save()
            # from UserManagementSystem.models import User
            # self.Uer.save()
        return self.user




# class accountform(models.Model):
class accountform(forms.ModelForm):
    username = fields.CharField(
        label= "账号",
        widget= widgets.TextInput(attrs={'class':'form-control'}),
        validators=[RegexValidator(r'^[a-zA-Z0-9_-]{4,16}$','4到16位（字母，数字，下划线，减号）')],
        error_messages = {'required':'不能为空',}
    )

    # nickname = fields.CharField(
    #     label="昵称",

    #     widget=widgets.TextInput(attrs={'class': 'form-control'}),
    #     validators=[RegexValidator(r'^[a-zA-Z0-9_-]{4,16}$', '4到16位（字母，数字，下划线，减号）')],
    #     error_messages={'required': '不能为空', }
    # )
    password = fields.CharField(
        label="密码",
        widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
        validators=[RegexValidator(r'^[a-zA-Z]([-_a-zA-Z0-9]{5,19})+$','以字母开头，字母，数字，减号，下划线')]
        ,error_messages = {'required': '不能为空', }
    )

    confirm_password = fields.CharField(
        label="密码",
        widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
        validators=[RegexValidator(r'^[a-zA-Z]([a-zA-Z0-9]{5,19})+$', '以字母开头，字母，数字，减号，下划线')]
        ,error_messages = {'required':'不能为空',}
     )

    email = fields.EmailField(
        label="邮箱",
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        error_messages={'inisvalid':'请输入正确的邮箱','required':'邮箱不能为空'})

    check_code = fields.CharField(
        label="验码",
        error_messages={'required':'验证码不能为空'}
    )

    # avatar_img = fields.ImageField(
    #     label="头像",
    #     error_messages={'invalid_image':"请上传图片类型",'required':'不能为空'}
    # )

    def clean_username(self):
        v = self.cleaned_data['username']
        # have_name = models.UserInfo.objects.filter(username=v).count()
        have_name = get_user_model().objects.filter(username=v).count()
        if have_name:
            raise ValidationError('用户名存在')
        return v

    def clean_email(self):
        v = self.cleaned_data['email']
        # has_email = models.UserInfo.objects.filter(email=v).count()
        has_email = get_user_model().objects.filter(email=v).count()
        if has_email:
            raise ValidationError('邮箱存在')
        return v

    def clean_check_code(self):
        v = self.cleaned_data['check_code']
        # if self.request.session.get('CheckCode').upper() != v.upper():
        #     raise ValidationError('验证码错误')
        return v
    def clean(self):
        value_dict = self.cleaned_data
        paw = value_dict.get('password')
        con_pax = value_dict.get('confirm_password')
        print(paw)
        if paw != con_pax:
            raise ValidationError('密码不一致')
        return  value_dict

class ShowProfileFormBAK(forms.Form):
# class ShowProfileFormBAK(forms.ModelForm):
    class Meta:
        model = User
        # fields = ('username','email','nickname','sex','role','is_active')
        fields = ('username','nickname','email','sex','is_active')
        widgets = {
            'username':forms.CharField(label='username',max_length=50,required=False),
            'email':forms.CharField(label='email',max_length=50,required=False),
            # email=forms.EmailInput(label='email',max_length=50,required=False),这个不是widgets里form格式
            'nickname':forms.CharField(label='nickname',max_length=50,required=False),
            'sex':forms.CharField(label='sex',max_length=50,required=False),
            # 'role' : forms.Select(choices=[(x.name,x.name) for x in RoleList.objects.all()],attrs={'class':'form-control'}),
            'is_active':forms.CharField(label='is_active',max_length=50,required=False),
        }

    def __init__(self,*args,**kwargs):
    # def __init__(self):
        # super(EditUserForm,self).__init__(*args,**kwargs)
        self.fields['username'].label=u'账 号'
        # self.fields['username'].error_messages={'required':u'请输入账号'}
        self.fields['email'].label=u'邮 箱'
        # self.fields['email'].error_messages={'required':u'请输入邮箱','invalid':u'请输入有效邮箱'}
        self.fields['nickname'].label=u'姓 名'
        # self.fields['nickname'].error_messages={'required':u'请输入姓名'}
        self.fields['sex'].label=u'性 别'
        # self.fields['sex'].error_messages={'required':u'请选择性别'}
        # self.fields['role'].label=u'角 色'
        self.fields['is_active'].label=u'状 态'


class ShowProfileForm(forms.Form):

    class Meta:
        model = User
   
    username=forms.CharField(label='username',max_length=50,required=False),
    email=forms.CharField(label='email',max_length=50,required=False),
    is_active=forms.CharField(label='is_active',max_length=50,required=False),
    # nickname=forms.CharField(label='nickname',max_length=50,required=False),
    # nickname = User.nickname,
    # sex = forms.CharField(label='sex',max_length=50,required=False),
    # from UserManagementSystem.models import User
    # nickname = User.nickname
    # sex = User.sex
    last_name = forms.CharField(label='last_name',max_length=50,required=False)
    first_name = forms.CharField(label='first_name',max_length=50,required=False)






#forget.html中，用于验证邮箱格式和验证码
class ForgetForm(forms.Form):
  email=forms.EmailField(required=True)
  captcha=CaptchaField(error_messages={'invalid':'验证码错误'})

#reset.html中，用于验证新设的密码长度是否达标
class ResetForm(forms.Form):
  newpwd1=forms.CharField(required=True,min_length=6,error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})
  newpwd2 = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})
