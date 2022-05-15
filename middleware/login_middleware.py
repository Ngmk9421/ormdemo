from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

loginRequired_list = ['/article/article', '/article/leave']


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path in loginRequired_list:
            if request.session.get('username'):
                return
            return redirect(reverse('user:login'))

    def process_exception(self, request, exception):
        return render(request, 'error.html')

