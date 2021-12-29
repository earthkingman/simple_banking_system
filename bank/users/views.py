import json, re, bcrypt, jwt
from datetime import datetime, timedelta
from django.http  import JsonResponse
from users.models import User
from django.shortcuts import render
import my_settings
SECRET_KEY = my_settings.SECRET
# Create your views here.

def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            hash_password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            if User.objects.filter(email=data['email']).exists(): 
                return JsonResponse({'Message':'USER_ALREADY_EXISTS'},status=400)
            User.objects.create(
                    email        = data['email'],
                    password     = hash_password
            )
            return JsonResponse({'Message':'SUCCESS'},status=201)
        except KeyError:
            return JsonResponse({'Message':'ERROR'},status=400)
    else :
        return JsonResponse({'Message':'ERROR'},status=400)

def login(request):
    if request.method == 'POST':
        try :
            data = json.loads(request.body)
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'Message':'USER_DOES_NOT_EXIST'},status=401)

            user = User.objects.get(email= data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id': user.id
                , "exp": datetime.utcnow() + timedelta(minutes=900000000)}
                , SECRET_KEY
                , algorithm="HS256")

                return JsonResponse({'TOKEN': access_token},status=200)

            return JsonResponse({'Message':'INVALID_PASSWORD'},status=401)
        except KeyError:
            return JsonResponse({'Message':'KEY_ERROR'},status=400)
    else :
        return JsonResponse({'Message':'ERROR'},status=400)
