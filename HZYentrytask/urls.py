"""HZYentrytask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#refrence: https://www.jb51.net/article/165662.htm

from django.urls import path
from UserManagementSystem import views

from django.views.static import serve
# from UserManagementSystem.views import ForgetPwdView,ResetView,ModifyView
# from upload import settings                #upload是站点名

# from django.conf.urls import url
# from django.contrib import admin
# from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

 
urlpatterns = [ 
    # path('register', views.register, name='register'), #第一个参数表示正则匹配   

    # url(r'^login/$', 'user.LoginUser', name='loginurl'),#第一个参数表示正则匹配
    # url(r'^logout/$', 'user.LogoutUser', name='logouturl'),
    path('login', views.login, name='loginurl'),
    # path('logout', 'views.logout', name='logouturl'),
    path('logout', views.logout, name='logouturl'),
    path('addUser', views.AddUser, name='adduserurl'),
    # url(r'^user/list/$', 'user.ListUser', name='listuserurl'),
    # path('user/edit/<int:ID>/', views.EditUser, name='edituserurl'),
    path('edit', views.EditUser, name='edituserurl'),
    path('showProfile', views.showProfile, name='showprofileurl'),
    path('user/delete', views.DeleteUser, name='deleteuserurl'),
    # url(r'^user/delete/$', 'user.DeleteUser', name='deleteuserurl'),
    path('user/changepwd', views.ChangePassword, name='changepasswordurl'),
    path('user/resetpwd', views.ResetPassword, name='resetpasswordurl'),

    path('register', views.register, name='register'), 
    path('upload', views.upload, name='uploadurl'), 
    path('home', views.home, name='homeurl'), 
    
    path('media/<str:path>', serve, {'document_root': settings.MEDIA_ROOT}),


    # #忘记密码
    # path('forget/',ForgetPwdView.as_view(),name='forget_pwd'),
    # #重置密码
    # path('reset/<str:active_code>',ResetView.as_view(),name='reset'),
    # path('modify/',ModifyView.as_view(),name='modify'),
   


#      path('admin/', admin.site.urls),
# ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

    # url(r'^admin/', admin.site.urls),
    # url(r'^regsiter/', views.regsiter),
    # url(r'', TemplateView.as_view(template_name="app01/index.html")),
    # path('UserManagementSystem/', include('UserManagementSystem.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ]
