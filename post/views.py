from django.shortcuts import render
from post import models
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from common import tools


def auth_token(view_func):
    def wrapper(request:HttpRequest):
        token = request.META.get('HTTP_JWT',0)
        print(token)
        res = view_func(request)
        return res
    return wrapper




@auth_token
# Create your views here.
def pub(request):  # 需要过期验证，登录验证

    return HttpResponse('OK')



def get(request):
    pass



def getall(request):
    pass
