from django.test import TestCase

# Create your tests here.

#
# import jwt
#
# key = '123456'
# pyload = {"name": "daxin"}
#
# x = jwt.encode(pyload, key, 'HS256')  # json能够转换的数据，密码字符串，算法 => bytes
# header, payload, sig = x.split(b'.')
#
# import base64
# print(base64.urlsafe_b64decode(header))
# print(base64.urlsafe_b64decode(payload + b'=='))
# print(base64.urlsafe_b64decode(sig + b'=='))

import bcrypt
import datetime

password = b'123456'

# 获取一个盐，用于对密码进行Mix(每次获取的salt都不同)
print(1, bcrypt.gensalt())
print(2, bcrypt.gensalt())

salt = bcrypt.gensalt()  # 拿到的盐相同，计算得到的密文就相同
print(salt)
# 通过盐来加密
x = bcrypt.hashpw(password, salt)
print(x)
y = bcrypt.hashpw(password, salt)
print(y)

# 校验
z = bcrypt.checkpw(password, x)
print(z)
