# from django.shortcuts import render_to_response,RequestContext
from django.shortcuts import render
from django.template import RequestContext
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from HZYentrytask.templates.html.commonPaginator import SelfPaginator
#from UserManage.views.permission import PermissionVerify
from django.contrib.auth import get_user_model
from UserManagementSystem.forms import LoginUserForm,ChangePasswordForm,AddUserForm,EditUserForm,RegisterForm,ShowProfileForm,ForgetForm,ResetForm
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.models import User
# from HZYentrytask.templates import
from django import forms
# from . import forms as fm
from django.views.decorators.csrf import csrf_exempt
import os


from random import Random
from django.core.mail import send_mail
# from users.models import EmailVerifyRecord
# from MxOnline.settings import EMAIL_FROM
# from .models import UserProfile
# from django.contrib.auth.hashers import make_password
# from apps.utils.email_send import send_register_email
# from .models import EmailVerifyRecord


# Create your views here.


'''    用户登录'''
def login(request):
    #还想实现先判断账户是否存在，如果不存在，则提示账号不存在，并加上注册功能
    # if request.user.is_authenticated():#验证是否已登陆的验证
        # return HttpResponseRedirect('/')

    # if request.method == 'GET' and request.GET.has_key('next'):
    # if request.method == 'GET' and 'next' in request.GET:
    #     next = request.GET['next']
    # else:
    #     next = '/'
    if request.method == "POST":
        # name = User.objects.get(username=request.user.username).username
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())

            # return render(request,'home.html')
            from UserManagementSystem.models import User
            user = User.objects.filter(username=request.user.username)[0]
            
            # return HttpResponseRedirect(reverse('homeurl'),{'user':user.headimg})
            return render(request,'home.html',{'user':user.headimg})
            # if request.POST['next'] !="":
            #     return HttpResponseRedirect(request.POST['next'])
            # else:
                # return render(request,'home.html')
                
    else:
        form = LoginUserForm(request)

    kwvars = {
        # 'request':request,
        'form':form
        # 'next':next,
    }

    # return render_to_response(,kwvars,RequestContext(request))
    # return render(request,'HZYentrytask/templates/html/login.html')
    return render(request,'login.html',kwvars)


'''    用户退出'''
# @login_required #登陆后才可以使用
def logout(request):    
    auth.logout(request)    
    # return redirect('login') #退出后，页面跳转至登录界面
    return HttpResponseRedirect(reverse('loginurl'))
    # return HttpResponseRedirect(reverse('logiurl'))


# @login_required
# @PermissionVerify()
# def DeleteUser(request,ID):
#     if ID == '1':
#         return HttpResponse(u'超级管理员不允许删除!!!')
#     else:
#         get_user_model().objects.filter(id = ID).delete()

#     return HttpResponseRedirect(reverse('listuserurl'))

'''    注销用户'''
# @login_required #登陆后才可以使用
# def DeleteUser(request,ID):
def DeleteUser(request):
    # get_user_model().objects.filter(id = ID).delete()
    # user = User.objects.get(username=request.user.username)
    get_user_model().objects.filter(username=request.user.username).delete()
    return HttpResponseRedirect(reverse('loginurl'))
# def DeleteUser(request):
#     get_user_model().objects.delete()
#     return HttpResponseRedirect(reverse('loginurl'))

'''    修改密码'''
# @login_required #登陆后才可以使用
def ChangePassword(request):
    if request.method=='POST':
        form = ChangePasswordForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect(reverse('logouturl'))
            return HttpResponseRedirect(reverse('loginurl'))
    else:
        form = ChangePasswordForm(user=request.user)

    kwvars = {
        'form':form
        # 'request':request,
    }

    # return render_to_response('HZYentrytask/templates/html/changePassword.html',kwvars,RequestContext(request))
    # return render(request,'HZYentrytask/templates/html/changePassword.html')
    return render(request,'changePassword.html',kwvars)


# @login_required
# @PermissionVerify()
# def ListUser(request):
#     mList = get_user_model().objects.all()

#     分页功能
#     lst = SelfPaginator(request,mList, 20)

#     kwvars = {
#         'lPage':lst,
#         'request':request,
#     }

#     return render_to_response('HZYentrytask/templates/html/listUser.html',kwvars,RequestContext(request))
#     return render(request,'HZYentrytask/templates/html/listUser.html')


'''    用户注册'''
def register(request):    
    if request.method == 'POST':        
        form = RegisterForm(user=request.user,data=request.POST)
         

        if form.is_valid():
            # form.save()
            username = request.POST.get('username') 
            # username = RegisterForm.cleaned_data.get('username')
            password = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            # password = request.POST.password
            # password = request.POST.get('password')
            # username = request.user.username
            # username = request.username
            user = User.objects.create_user(username=username,password=password,email=email)        
            user.save() 
            id = user.id
            from UserManagementSystem.models import User as myUser
            if len(myUser.objects.filter(username =username)) == 0:
                usr = myUser()
            else:
                usr = myUser.objects.filter(username =username)[0]
            usr.username = username
            # usr.user_id = id
            # usr.headimg = null
            usr.save()


            auth.login(request, user) 
            return HttpResponseRedirect(reverse('loginurl'))
    else:
        form = RegisterForm(user=request.user)
        # form = RegisterForm()

    kwvars = {
        'form':form
        # 'request':request,
    }
    
    return render(request,'register.html',kwvars)

     



# @login_required
#@PermissionVerify()
def AddUser(request):
    if request.method=='POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            # return HttpResponseRedirect(reverse('listuserurl'))
            return HttpResponseRedirect(reverse('loginurl'))
    else:
        form = AddUserForm()

    kwvars = {
        'form':form
        # 'request':request,
    }

    # return render_to_response('HZYentrytask/templates/html/addUser.html',kwvars,RequestContext(request))
    # return render(request,'HZYentrytask/templates/html/addUser.html')
    return render(request,'addUser.html',kwvars)


# @login_required
#@PermissionVerify()
# def EditUser(request,ID):
def EditUser(request):
    # user = get_user_model().objects.get(id = ID)
    user = User.objects.get(username=request.user.username)

    if request.method=='POST':
        form = EditUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect(reverse('listuserurl'))
            # return render(request,'home.html')#等查看信息调好了，回到showProfile.html
            return HttpResponseRedirect(reverse('showprofileurl'))
    else:
        form = EditUserForm(instance=user)
        # print('this is a test by hzy!!!')

    kwvars = {
        # 'ID':ID,
        'form':form
        # 'request':request,
    }

    # return render_to_response('HZYentrytask/templates/html/editUser.html',kwvars,RequestContext(request))
    # return render(request,'HZYentrytask/templates/html/editUser.html')
    return render(request,'editUser.html',kwvars)



# @login_required
# @PermissionVerify()
# def ResetPassword(request,ID):
def ResetPassword(request):
    user = User.objects.get(user=request.user)

    newpassword = get_user_model().objects.make_random_password(length=10,allowed_chars='abcdefghjklmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789')
    print ('====>ResetPassword:%s-->%s' %(user.username,newpassword))
    user.set_password(newpassword)
    user.save()

    kwvars = {
        'object':user,
        'newpassword':newpassword,
        # 'request':request,
    }

    # return render_to_response('HZYentrytask/templates/html/resetPassword.html',kwvars,RequestContext(request))
    # return render(request,'HZYentrytask/templates/html/resetPassword.html')
    return render(request,'resetPassword.html',kwvars)

# @login_required
def showProfile(request):
    # user = get_object_or_404(User, pk=pk)
    # user = get_user_model().objects.get(id = ID)
    userinfo = User.objects.get(username=request.user.username)

    # from UserManagementSystem.models import User
    # usr = User.objects.filter(user_id=request.user.id)
    # return render(request,"showProfile.html",{'userinfo':userinfo, 'extra_info':usr})

    return render(request,"showProfile.html",{'userinfo':userinfo})
    # return render(request, 'HZYentrytask/templates/html/profile.html', {'user': user})


def showProfiles(request):
    userinfo = User.objects.get(username=request.user.username)

    if request.method=='GET':
        # form = ShowProfileForm(request.GET,instance=user)
        form = ShowProfileForm(request.GET)
        if form.is_valid():
            form.save()
            return render(request,"showProfile.html",{'userinfo':userinfo})
    else:
        # form = ShowProfileForm(instance=user)
        form = ShowProfileForm()

    kwvars = {
        # 'ID':ID,
        'form':form
        # 'request':request,
    }

    # return render_to_response('HZYentrytask/templates/html/editUser.html',kwvars,RequestContext(request))
    # return render(request,'HZYentrytask/templates/html/editUser.html')
    return render(request,'showProfile.html',kwvars)

# @login_required
# @csrf_exempt
def upload(request):
    if request.method == 'POST':
        name = request.user.username
        user_id = request.user.id
        avatar = request.FILES.get('avatar')
        # from UserManagementSystem.models import FormalUser
        from UserManagementSystem.models import User
        if len(User.objects.filter(username=name)) == 0:
            user = User()
        else:
            user = User.objects.filter(username=name)[0]
        # user.username = name
        user.user_id = user_id
        user.headimg = avatar
        user.save()
        
        # return HttpResponse('上传成功')
        # return render_to_response('index.html', {'images':'1.jpg'})
        # return render(request,'home.html',{'user':user.headimg})
        return HttpResponseRedirect(reverse('homeurl'),{'user':user.headimg})
        # return render(request,'home.html')
        
 
    return render(request,'upload.html')


# @login_required
def home(request):
    if request.method == 'GET':
        # imgPath = request.User.headimg
        # IMG.objects.filter(name=imgPath)
        # img = IMG.objects.all()
        # return render(request,'home.html',{'img':img})
        # return render(request,'home.html',{'img':imgPath})
        print("--------")
        print(request.user)
        # user = User.objects.filter(username=request.user)[0]
        from UserManagementSystem.models import User
        user = User.objects.filter(username=request.user.username)[0]
        print(user)
        return render(request,'home.html',{'user':user.headimg})


#随机生成验证码
def random_str(randomlength=8):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    random = Random()
    # random = random.Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

#发送邮件找回密码 
def findpwdView(request):
    if request.method=="GET":
        email_title = "找回密码"
        code=random_str()#随机生成的验证码
        request.session["code"]=code #将验证码保存到session
        email_body = "验证码为：{0}".format(code)
        send_status = send_mail(email_title, email_body,"xxxx@shopee.com",["xxxx@qq.com",])
        msg="验证码已发送，请查收邮件"
    else:
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=User.objects.get(username=username)
        code=request.POST.get("code") #获取传递过来的验证码
        if code==request.session["code"]:
            user.set_password(password)
            user.save()
            del request.session["code"] #删除session
            msg="密码已重置"
    return render(request,"findpwd.html",locals())






# class ForgetPwdView(View):
#   '''忘记密码'''
#   def get(self,request):
#     forget_form=ForgetForm()
#     return render(request,'forget.html',{'forget_form':forget_form})
#   def post(self,request):
#     forget_form = ForgetForm(request.POST)
#     if forget_form.is_valid():
#       email=request.POST.get('email','')
#       send_register_email(email,'forget')
#       return render(request,'send_success.html')
#     else:
#       return render(request,'forget.html',{'forget_form':forget_form})


# # class ResetView(View):
#   '''重置密码'''
#   def get(self,request,active_code):
#     record=EmailVerifyRecord.objects.filter(code=active_code)
#     print(record)
#     if record:
#       for i in record:
#         email=i.email
#         is_register=UserProfile.objects.filter(email=email)
#         if is_register:
#           return render(request,'pwd_reset.html',{'email':email})
#     return redirect('home')


# #因为<form>表单中的路径要是确定的，所以post函数另外定义一个类来完成
# # class ModifyView(View):
# class ModifyView():
#   """重置密码post部分"""
#   def post(self,request):
#     reset_form=ResetForm(request.POST)
#     if reset_form.is_valid():
#       pwd1=request.POST.get('newpwd1','')
#       pwd2=request.POST.get('newpwd2','')
#       email=request.POST.get('email','')
#       if pwd1!=pwd2:
#         return render(request,'pwd_reset.html',{'msg':'密码不一致！'})
#       else:
#         user=UserProfile.objects.get(email=email)
#         user.password=make_password(pwd2)
#         user.save()
#         return redirect('home')
#     else:
#       email=request.POST.get('email','')
#       return render(request,'pwd_reset.html',{'msg':reset_form.errors})







