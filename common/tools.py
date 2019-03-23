import datetime
import bcrypt
import jwt
from blog import settings


# 密码加密
def pwd_bcrypt(password):
    salt = bcrypt.gensalt()
    pwd = bcrypt.hashpw(password.encode(), salt)
    return pwd


# 获取jwt_token
def get_token(user_id):
    payload = {'user_id': user_id, 'exp': int(datetime.datetime.now().timestamp() + settings.token_expire)}
    token = jwt.encode(payload, settings.SECRET_KEY, 'HS256')
    return token.decode()

# 验证jwt token
def check_token(token):
    if jwt.decode(token, settings.SECRET_KEY):
        return True
    return False

# 获取header信息
def get_jwt_header(token):
    return jwt.decode(token, settings.SECRET_KEY)


# 验证密码
def check_password(auth_pwd, db_pwd):
    if bcrypt.checkpw(auth_pwd.encode(), db_pwd.encode()):
        return True
    return False

# 分页索引
def validate(d: dict, name, default, converse, validate_func):
    try:
        result = converse(d.get(name, default))
        result = validate_func(result, default)
    except:
        result = default
    return result
