import json

from django.test import TestCase, Client
from django.conf import settings

from advertisers.models import advertiser_info
#########
# 권은경 #
######## 
# 광고주 생성 테스트
class AdvertiserPostTest(TestCase):
    def setUp(self):
        advertiser_info.objects.create(
            advertiser_id = '19950919',
            name = '권은경',
            email = 'fore0919@velog.io',
            phone = '010-3331-1826'
        )
    def tearDown(self):
        advertiser_info.objects.all().delete()

# 생성 성공 
    def test_SigninView_post_success(self):
        client = Client()
        advertiser_info = {
            'advertiser_id' : '09950818',
            'name' : '은경',
            'email' : 'fore0818@velog.io',
            'phone' : '010-3331-1826'
        }
        response = client.post('/api/v1/advertisers/signin', json.dumps(advertiser_info), content_type='application/json')
        self.assertEqual(response.json(), {'message':'SUCCESS'})
        self.assertEqual(response.status_code,201)

# 아이디 조건 미 충족
    def test_SigninView_post_id_validation_failed(self):
        client = Client()
        advertiser_info = {
            'advertiser_id' : '0995081811s',
            'name' : '은경',
            'email' : 'fore0818@velog.io',
            'phone' : '010-3331-1826'
        }
        response = client.post('/api/v1/advertisers/signin', json.dumps(advertiser_info), content_type='application/json')
        self.assertEqual(response.json(), {'message':'USER_ID_VALIDATION_ERROR'})
        self.assertEqual(response.status_code,400)

# 이메일 조건 미 충족
    def test_SigninView_post_email_validation_failed(self):
        client = Client()
        advertiser_info = {
            'advertiser_id' : '09950818',
            'name' : '은경',
            'email' : 'fore0818velog.io',
            'phone' : '010-3331-1826'
        }
        response = client.post('/api/v1/advertisers/signin', json.dumps(advertiser_info), content_type='application/json')
        self.assertEqual(response.json(), {'message':'EMAIL_VALIDATION_ERROR'})
        self.assertEqual(response.status_code,400)

# 전화번호 조건 미 충족 
    def test_SigninView_post_phone_validation_failed(self):
        client = Client()
        advertiser_info = {
            'advertiser_id' : '09950818',
            'name' : '은경',
            'email' : 'fore0818@velog.io',
            'phone' : '0103331-1826s'
        }
        response = client.post('/api/v1/advertisers/signin', json.dumps(advertiser_info), content_type='application/json')
        self.assertEqual(response.json(), {'message':'PHONE_NUMBER_VALIDATION_ERROR'})
        self.assertEqual(response.status_code,400)

# 중복 아이디 
    def test_SigninView_post_id_already_exists_failed(self):
        client = Client()
        advertiser_info = {
            'advertiser_id' : '19950919',
            'name' : '권은경',
            'email' : 'fore0818@velog.io',
            'phone' : '010-3331-1826'
        }
        response = client.post('/api/v1/advertisers/signin', json.dumps(advertiser_info), content_type='application/json')
        self.assertEqual(response.json(), {'message':'ALREADY_EXISTS_ID'})
        self.assertEqual(response.status_code,409)

# 중복 이메일
    def test_SigninView_post_email_already_exists_failed(self):
        client = Client()
        advertiser_info = {
            'advertiser_id' : '19950818',
            'name' : '권은경',
            'email' : 'fore0919@velog.io',
            'phone' : '010-3331-1826'
        }
        response = client.post('/api/v1/advertisers/signin', json.dumps(advertiser_info), content_type='application/json')
        self.assertEqual(response.json(), {'message':'ALREADY_EXISTS_EMAIL'})
        self.assertEqual(response.status_code,409)

# 정보 하나라도 미입력시 에러 반환
    def test_SigninView_post_keyerror_failed(self):
        client = Client()
        advertiser_info = {
            'name' : '권은경',
            'email' : 'fore0919@velog.io',
            'phone' : '010-3331-1826'
        }
        response = client.post('/api/v1/advertisers/signin', json.dumps(advertiser_info), content_type='application/json')
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})
        self.assertEqual(response.status_code,400)

# 광고주 불러오기 테스트 
class AdvertiserGetTest(TestCase):
    def setUp(self):
        advertiser_info.objects.create(
            advertiser_id = '19950919',
            name = '권은경',
            email = 'fore0919@velog.io',
            phone = '010-3331-1826'
        )
    def tearDown(self):
        advertiser_info.objects.all().delete()
# 불러오기 성공
    def test_advertiser_get_success(self):
        client   = Client()
        response = client.get('/api/v1/advertisers/19950919')
        self.assertEqual(response.json(),
            {
                "result" : {
                    "advertiser_id": "19950919",
                    "name": "권은경",
                    "email": "fore0919@velog.io",
                    "phone": "010-3331-1826"
                }
            }
        )
        self.assertEqual(response.status_code, 200) 

# 불러오기 실패 - 존재하지 않는 광고주 
    def test_advertiser_get_failed(self):
        client   = Client()
        response = client.get('/api/v1/advertisers/19950918')
        self.assertEqual(response.json(),{'message':'DOES_NOT_EXISTS'})
        self.assertEqual(response.status_code, 404) 

