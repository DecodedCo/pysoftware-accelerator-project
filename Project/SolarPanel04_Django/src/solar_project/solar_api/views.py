from solar_lib import estimators as est

from rest_framework.decorators import api_view
from .models import SolarResult, SolarResultSerializer
from rest_framework.response import Response
from .apimodel import solarapi_est_response  

@api_view(['GET'])
def test_django_api(request):
    return Response({'error': False, 'data': 'hello!'})

@api_view(['GET'])
def test_request_data(request):
    return Response(solarapi_est_response(est.run_estimators(
        est.PvwattsParameters(),
        est.EnergyPriceParameters([f"2024/{m}/01" for m in range(1, 12)])
    )))

@api_view(['GET'])
def test_submit_data(request):
    return Response({
        "error": False, 
        "resultID": 1
    })

@api_view(['POST'])
def submit_data(request):
    serializer = SolarResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def request_data(request, result_id):
    try:
        result = SolarResult.objects.get(id=result_id)
    except SolarResult.DoesNotExist:
        return Response({'error': 'Result not found'}, status=404)
    serializer = SolarResultSerializer(result)
    return Response(serializer.data)
