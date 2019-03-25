from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse
import datetime
import simplejson
from common import tools
from user import models


# Create your views here.

# def index(request: HttpRequest, year=1):
#     my_dict = {
#         'a': 100,
#         'b': ['{}x{}={}'.format(i, j, i * j) for i in range(1, 10) for j in range(1, 10)],
#         'c': list(range(10, 20)),
#         'd': 'abc',
#         'e': list(range(1, 10)),
#         'date': datetime.datetime.now()
#     }
#
#     print(year)
#
#     return render(request, 'index.html', my_dict)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        try:
            payload = simplejson.loads(request.body)
            email = payload['email']
            user = models.User.objects.get(email=email)
            print(user)
            # 验证密码
            if tools.check_password(payload['password'], user.password):
                return JsonResponse({
                    'user': user.id,
                    'name': user.name,
                    'email': user.email,
                    'token': tools.get_token(user.id)
                })
            else:
                return HttpResponseBadRequest('Error')
        except Exception as e:
            print(e)
            return HttpResponseBadRequest('Error')


def register(request: HttpRequest):
    if request.method == 'POST':
        content_type = request.META.get('CONTENT_TYPE')  # CONTENT_TYPE:application/json
        try:
            if 'json' in content_type:
                payload = simplejson.loads(request.body)
                username = payload['name']
                password = payload['password']
                email = payload['email']
            if 'form-data' in content_type:
                username = request.POST.get('name')
                password = request.POST.get('password')
                email = request.POST.get('email')
        except Exception as e:
            print(e)
            return HttpResponseBadRequest('Error')
        password = tools.pwd_bcrypt(password)
        res = models.User.objects.filter(email=email).first()

        if res:
            return HttpResponseBadRequest('email is exists')
        user = models.User(name=username, password=password, email=email)
        try:
            user.save()
            token = tools.get_token(user.id)
            return JsonResponse({
                'user': user.id,
                'name': user.name,
                'email': user.email,
                'token': token
            })
        except:
            raise
