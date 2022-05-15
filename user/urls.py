from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    # 注册
    path('register', views.register, name='register'),
    # 登录
    path('login', views.login, name='login'),
    # 账号激活
    path('user_active', views.user_active, name='user_active'),
    path('logout', views.logout, name='logout'),
    path('forget_code_pwd', views.forget_code_pwd, name='forget_code_pwd'),
    path('code_phone_pwd', views.send_phone_code, name='code_phone_pwd'),
    path('forget_mail_pwd', views.forget_mail_pwd, name='forget_mail_pwd'),
    path('code_mail_pwd', views.send_mail_code, name='code_mail_pwd'),
    path('center', views.center, name='center'),
    path('profile', views.profile, name='profile'),

    path('msg_center', views.msg_center, name='msg_center'),
    path('msg', views.msg, name='msg'),
    path('msg_update', views.msg_update, name='msg_update')
]
