import jwt
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model


@database_sync_to_async
def get_user(scope):
    token = scope["token"]
    model = get_user_model()    
    try:
        if token:
            print("jest token !!!!")
            # user_id = jwt.decode(token, settings.SECRET_KEY,
            #                      algorithms=["HS256"])["user_id"]            
            user_id = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])["user_id"]       
            
            print("user_id: ", user_id)
            return model.objects.get(id=user_id)
        else:
            return AnonymousUser()
    except Exception as e:
        print(e)
        return AnonymousUser()
    


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        headers_dict = dict(scope['headers'])
        print("headers_dict: ", headers_dict)
        cookies_str = headers_dict.get(b'cookie', b"").decode()
        print("cookies_str: ", cookies_str)        
        cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookies_str.split('; ')}
        print("cookies dict: ", cookies)
        access_token = cookies.get('access_token')
        scope["token"] = access_token
        scope["user"] = await get_user(scope)
        return await self.app(scope, receive, send)
