import datetime

import simplejson
from django.shortcuts import render
from post import models
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse
from common import tools
from django.db import transaction


# token的过期以及放篡改验证
def auth_token(view_func):
    def wrapper(request: HttpRequest):
        try:
            tools.check_token(request.META.get('HTTP_JWT', 0))
        except Exception:
            return HttpResponseBadRequest('token Error')
        res = view_func(request)
        return res

    return wrapper


@auth_token
# Create your views here.
def pub(request: HttpRequest):
    if request.method == 'POST':
        try:
            payload = simplejson.loads(request.body)
            title = payload['title']
            content = payload['content']

            # 通过jwt header拿出用户的id
            header = tools.get_jwt_header(request.META.get('HTTP_JWT'))
            user_id = header.get('user_id')
            user = models.User.objects.get(pk=user_id)

            # 保存博文和内容信息
            with transaction.atomic():
                post = models.Post(title=title, postdate=datetime.datetime.now(), author=user)
                post.save()
                content = models.Content(post=post, content=content)
                content.save()

        except Exception as e:
            print(e)
            return HttpResponseBadRequest('Error')

        return JsonResponse(
            {
                "post_id": post.id
            }
        )


def get(request):
    pass


def getall(request):
    pass
