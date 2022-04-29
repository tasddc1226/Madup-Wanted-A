import json

from django.http      import JsonResponse, request
from django.views     import View

from advertisers.models import advertiser_info
from .utils  import validate_email, validate_phone, validate_id

# 권은경
class AdvertiserSignIn(View):
    def post(self, request):
        try : 
            data = json.loads(request.body)
            advertiser_id = data['advertiser_id']
            name = data['name']
            email = data['email']
            phone = data['phone']

            if not validate_id(advertiser_id):
                return JsonResponse({'message':'USER_ID_VALIDATION_ERROR'}, status=400)
                
            if not validate_email(email):
                return JsonResponse({'message':'EMAIL_VALIDATION_ERROR'}, status=400)
            
            if not validate_phone(phone):
                return JsonResponse({'message':'PHONE_NUMBER_VALIDATION_ERROR'}, status=400)

            if advertiser_info.objects.filter(advertiser_id=advertiser_id).exists():
                return JsonResponse({'message':'ALREADY_EXISTS_ID'}, status=409)
    
            if advertiser_info.objects.filter(email=email).exists():
                return JsonResponse({'message':'ALREADY_EXISTS_EMAIL'}, status=409)

            advertiser_info.objects.create(
                advertiser_id = advertiser_id,
                name = name,
                email = email,
                phone = phone,
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class AdvertiserView(View):
    def get(self, request, advertiser_id):
        try:
            if not advertiser_info.objects.filter(advertiser_id=advertiser_id).exists():
                return JsonResponse({'message':'DOES_NOT_EXISTS'}, status=404)

            advertisers = advertiser_info.objects.get(advertiser_id=advertiser_id)

            result = {
                'advertiser_id' : advertisers.advertiser_id,
                'name' : advertisers.name,
                'email' : advertisers.email,
                'phone' : advertisers.phone,
            }

            return JsonResponse({'result':result}, status = 200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400) 

    def patch(self, request, advertiser_id):
        try:
            data = json.loads(request.body)
            advertisers = advertiser_info.objects.get(advertiser_id=advertiser_id)

            name = data['name']
            email = data['email']
            phone = data['phone']

            advertisers.name = name
            advertisers.email = email
            advertisers.phone = phone
            advertisers.save()

            return JsonResponse({'message':'SUCCESS'}, status = 200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except advertiser_info.DoesNotExist:
            return JsonResponse({'message':'ADVERTISER_DOES_NOT_EXIST'}, status=404)

    def delete(self, request, advertiser_id):
        try:
            advertisers =advertiser_info.objects.get(advertiser_id=advertiser_id)
            
            if not advertiser_info.objects.filter(advertiser_id=advertiser_id).exists():
                return JsonResponse({'message':'DOES_NOT_EXISTS'}, status=404)

            advertisers.delete()

            return JsonResponse({'message':'SUCCESS'}, status=204)
        except advertiser_info.DoesNotExist:
            return JsonResponse({'message':'ADVERTISER_DOES_NOT_EXIST'}, status=404)
