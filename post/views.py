import datetime

import math
import simplejson
from django.shortcuts import render
from post import models
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse, HttpResponseNotFound
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


def get(request, post_id):
    if request.method == 'GET':
        post = models.Post.objects.filter(pk=post_id).first()

        if post:
            return JsonResponse(
                {
                    "id": post.id,
                    "title": post.title,
                    "author": post.author.name,
                    'content': post.content.content
                }
            )
        return HttpResponseNotFound('post is not exists')


def getall(request):
    if request.method == 'GET':
        # try:
        #     page = int(request.GET.get('page', 1))
        #     page = page if page > 0 else 1
        # except Exception:
        #     page = 1
        #
        # try:
        #     size = int(request.GET.get('size', 20))
        #     size = size if size > 0 and size < 100 else 20
        # except Exception:
        #     size = 20

        page = tools.validate(request.GET, 'page', 1, int, lambda result, default: result if result > 0 else default)
        size = tools.validate(request.GET, 'size', 3, int,
                              lambda result, default: result if result > 0 and size < 100 else default)
        start = (page - 1) * size
        all_posts = models.Post.objects.order_by('id')
        count = all_posts.count()
        posts = all_posts[start:start + size]
        return JsonResponse(
            {'posts': [
                {"id": post.id,
                 "title": post.title,
                 "author": post.author.name,
                 'content': post.content.content
                 } for post in posts
            ],
                'page': page,
                'total': math.ceil(count / size)
            }
        )

    return HttpResponse('OK')
