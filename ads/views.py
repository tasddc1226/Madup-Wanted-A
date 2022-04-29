from django.db.models import Sum
from .models import result_data_set
from advertisers.models import advertiser_info

from datetime import datetime
from django.http import JsonResponse

# Create your views here.
def analysis_detail(request):

    # 조회할 광고주id의 존재여부 확인
    advertiser_id = request.GET.get('advertiser_id', None)
    advertiser = advertiser_info.objects.filter(advertiser_id=advertiser_id).first()
    if not advertiser:
        return JsonResponse({'message':f'{advertiser_id}로 검색된 광고주가 없습니다.'}, status=404)
    
    # 입력기간 예외 처리
    try:
        date_format = '%Y.%M.%d'
        start_date = datetime.strptime(request.GET.get('start_date', None), date_format)
        end_date = datetime.strptime(request.GET.get('end_date', None), date_format)
    except:
        return JsonResponse({'message':'조회 날짜가 비어있거나 입력 형식이 잘못되었습니다. 일자입력형식은 YYYY.MM.DD입니다.'}, status=404)

    if start_date > end_date:
        return JsonResponse({'message':'조회 시작 날짜보다 끝 날짜가 더 빠를 수 없습니다.'}, status=404)

    # 광고주id와 기간으로 검색
    datas = result_data_set.objects.filter(advertiser_id=advertiser_id, 
                                    date__gte=start_date, date__lte=end_date)

    # 검색된 결과에서 media(매체)의 종류를 뽑아내기
    media_kind = datas.values_list('media', flat=True).distinct()
    media_kind_list = []
    for i in range(media_kind.count()):
        media_kind_list.append(media_kind[i])

    # 매체별로 filtering하여 각각 계산된 분석자료를 사전에 입력
    analysis_datas_set = {}
    for kind in media_kind_list:
        data = datas.filter(media=kind)
        total = data.aggregate(
            total_click = Sum('click'),
            total_impression = Sum('impression'),
            total_cost = Sum('cost'),
            total_conversion = Sum('conversion'),
            total_cv = Sum('cv'),
        )
        analysis_datas = {
            'ctr': round(total['total_click'] * 100 / total['total_impression'], 2),
            'roas': round(total['total_cv'] * 100 / total['total_cost'], 2),
            'cpc': round(total['total_cost'] * 100 / total['total_click'], 2),
            'cvr': round(total['total_conversion'] * 100 / total['total_click'], 2),
            'cpa': round(total['total_cost'] * 100 / total['total_conversion'], 2),
        }
        analysis_datas_set[f'{kind}'] = analysis_datas

    return JsonResponse({'message':'SUCCESS', 'analysis_datas': analysis_datas_set}, status=200)
    
