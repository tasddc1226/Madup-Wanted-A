import json

from django.test import TestCase, Client
from datetime import datetime

from ads.models import result_data_set, ad_info
from advertisers.models import advertiser_info

TestCase.maxDiff = None
# 양수영
# 광고 효율 데이터 테스트
class GetAdsResultTest(TestCase):
    def setUp(self):
        advertiser_info.objects.create(
            advertiser_id = '37443400',
            name = '양수영',
            email = 'tasddc@namver.com',
            phone = '010-1234-1234'
        )
        ad_info.objects.create(
            uid = 'ad_cmp-a001-04-000000000684573',
            advertiser_id = '37443400',
            media = 'naver'
        )
        # 37443400	ad_cmp-a001-04-000000000684573	naver	2022.1.1	49900	244	47	0	0
        result_data_set.objects.create(
            advertiser_id = '37443400',
            uid_id = 'ad_cmp-a001-04-000000000684573',
            media = 'naver',
            date = datetime.strptime('2022.01.01','%Y.%M.%d'),
            cost = '49900',
            impression = 244,
            click = '47',
            conversion = '0',
            cv = '0'
        )
        # 37443400	ad_cmp-a001-04-000000000684573	naver	2022.1.2	49900	434	68	4	162800
        result_data_set.objects.create(
            advertiser_id = '37443400',
            uid_id = 'ad_cmp-a001-04-000000000684573',
            media = 'naver',
            date = datetime.strptime('2022.01.02', '%Y.%M.%d'),
            cost = '49900',
            impression = 434,
            click = '68',
            conversion = '4',
            cv = '162800'
        )
    def tearDown(self):
        result_data_set.objects.all().delete()
    
    # 효율 분석 데이터 가져오기 성공
    def test_analysis_get_success(self):
        client = Client()
        response = client.get('/api/v1/ads/analysis-detail?advertiser_id=37443400&start_date=2022.01.01&end_date=2022.01.02')
        self.assertEqual(response.json(),
            {
                "message": "SUCCESS",
                "analysis_datas": {
                    "naver": {
                        "ctr": 18.89,
                        "roas": 403.89,
                        "cpc": 72109.83,
                        "cvr": 6.94,
                        "cpa": 1039583.33
                    }
                }
            }
        )
        self.assertEqual(response.status_code, 200)


