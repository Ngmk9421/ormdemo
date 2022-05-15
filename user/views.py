import hashlib
import uuid

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template
from django.urls import reverse

from article.models import Article
from ormdemo.settings import EMAIL_FROM
from user.models import User, UserProfile, Message

# 注册
from user.utils import Sample


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        mail = request.POST.get('mail')
        phone = request.POST.get('phone')
        confirm = request.POST.get('confirm')

        print(username, password, mail, phone, confirm)

        # 密码一致，进行加密，存储到数据库，发送激活邮件
        if password == confirm:
            password = hashlib.sha256(password.encode('utf8')).hexdigest()
            user = User.objects.create(username=username, password=password)
            UserProfile.objects.create(mail=mail, user_id=user.id, phone=phone)
            user.is_active = False
            user.save()

            # 生成 token 发送激活邮件
            token = str(uuid.uuid4()).replace('-', '')
            # 将生成的 token 和用户建立联系
            request.session[token] = user.id

            # 拼成激活链接
            path = 'http://100.100.6.186/user/user_active?token={}'.format(token)

            email_msg = get_template('mail.html').render({'username': username, 'path': path})
            send_mail(subject='激活邮件', message='', from_email=EMAIL_FROM, recipient_list=[mail], html_message=email_msg)

            return HttpResponse('账号激活邮件已发送，激活之后即可登录')
        else:
            return render(request, 'user/register.html', {'msg': '两次密码不一致！'})
    return render(request, 'user/register.html')


# 登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        rem_name = request.POST.get('rem_name')

        # 查找该用户
        user = User.objects.filter(username=username).first()
        # 判断 账号是否激活
        if not user.is_active:
            return HttpResponse('账号未激活')
        # 用户存在判断密码是否一致
        if user:
            password = hashlib.sha256(password.encode('utf8')).hexdigest()
            if user.password == password:
                # 使用session记录用户登录状态
                request.session['username'] = username

                # 登录 记住我
                response = redirect(reverse('index'))
                if rem_name == 'on':
                    response.set_cookie('username', user.username)
                return response
            else:
                return render(request, 'user/login.html', {'msg': '用户名或密码错误！'})
        else:
            return render(request, 'user/login.html', {'msg': '该用户还未注册！'})
    else:
        username = request.COOKIES.get('username', '')

    return render(request, 'user/login.html', {'username': username})


# 首页
def index(request):
    # 喜欢量
    articles = Article.objects.filter(is_delete=False).order_by('-like_num').all()
    articles = articles[:5]

    # 首页展示访问量最高的文章
    hots = Article.objects.filter(is_delete=False).order_by('-visit_num').all()
    hots = hots[:6]
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    return render(request, 'user/index.html', {'articles': articles, 'user': user, 'hots': hots})


# 邮箱激活
def user_active(request):
    token = request.GET.get('token')
    id = request.session.get(token)
    user = User.objects.get(pk=id)
    user.is_active = True
    user.save()
    request.session.pop(token)
    return redirect(reverse('user:login'))


# 退出登录
def logout(request):
    request.session.delete()
    # request.session.clear()  # 不删除数据库里的内容
    return redirect(reverse('index'))


# 忘记密码 手机号
def forget_code_pwd(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        code = int(request.POST.get('code'))
        new_pwd = request.POST.get('new_pwd')
        session_code = request.session.get(phone)

        if session_code == code:
            new_password = hashlib.sha256(new_pwd.encode('utf8')).hexdigest()
            userprofile = UserProfile.objects.filter(phone=phone).first()
            userprofile.user.password = new_password
            userprofile.user.save()
            return render(request, 'user/login.html')
    return render(request, 'user/forget_code_pwd.html')


def send_phone_code(request):
    phone = request.GET.get('phone')
    if phone:
        import random
        # 生成随机验证码
        code = random.randint(100000, 999999)
        val = Sample.send(phone, code)

        if val.get('Code', '') == 'OK':
            request.session[phone] = code
            return JsonResponse({'msg': '发送成功'})

    return JsonResponse({'msg': '出错了'})


# 忘记密码 邮箱
def forget_mail_pwd(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        code = int(request.POST.get('code'))
        new_pwd = request.POST.get('new_pwd')
        session_code = request.session.get(mail)

        if session_code == code:
            new_password = hashlib.sha256(new_pwd.encode('utf8')).hexdigest()
            userprofile = UserProfile.objects.filter(mail=mail).first()
            userprofile.user.password = new_password
            userprofile.user.save()
            return render(request, 'user/login.html')
    return render(request, 'user/forget_mail_pwd.html')


def send_mail_code(request):
    mail = request.GET.get('mail')
    if mail:
        import random
        # 生成随机验证码
        code = random.randint(100000, 999999)

        msg = '【晨曦记录】您的验证码%d，该验证码5分钟内有效，请勿泄露于他人！' % code

        val = send_mail('重置密码', msg, EMAIL_FROM, [mail])
        if val == 1:
            request.session[mail] = code
            return JsonResponse({'msg': '发送成功'})

    return JsonResponse({'msg': '出错了'})


# 个人中心
def center(request):
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    articles = user.article_set.filter(is_delete=False).all()
    return render(request, 'user/center.html', {'user': user, 'articles': articles})


def profile(request):
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    if request.method == 'POST':
        icon = request.FILES.get('icon')
        # username = request.POST.get('username')
        phone = request.POST.get('phone')

        user.userprofile.icon = icon
        # user.username = username
        user.userprofile.phone = phone
        user.save()
        user.userprofile.save()
        return HttpResponse('成功')
    return render(request, 'user/profile.html', {'user': user})


def msg_center(request):
    receive_id = int(request.GET.get('receive_id'))
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    # print(receive_id, user.id)
    messages = Message.objects.filter(
        Q(send_id__in=[receive_id, user.id]) & Q(receive_id__in=[receive_id, user.id])).all()
    # print(messages)
    user1 = User.objects.get(pk=receive_id)
    return render(request, 'user/message_center.html',
                  {'receive_id': receive_id, 'user': user, 'user1': user1, 'messages': messages})


def msg(request):
    msg = request.POST.get('msg')
    send_id = request.POST.get('send_id')
    receive_id = request.POST.get('receive_id')

    Message(send_id=send_id, receive_id=receive_id, msg=msg).save()

    return JsonResponse({'msg': msg})


def msg_update(request):
    send_id = request.POST.get('send_id')
    receive_id = request.POST.get('receive_id')

    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    messages = Message.objects.filter(
        Q(send_id__in=[receive_id, user.id]) & Q(receive_id__in=[receive_id, user.id])).all()
    data = {'length': len(messages), 'data': []}
    for message in messages:

        data['data'].append({
            'send_username': User.objects.get(pk=message.send_id).username,
            'receive_username': User.objects.get(pk=message.receive_id).username,
            'msg': message.msg,
            'send_time': message.send_time
        })

    return JsonResponse(data)
