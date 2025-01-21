from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import connect_mt5, get_eurusd_data, detect_flag_pattern

class FlagDetectionView(APIView):
    def get(self, request, *args, **kwargs):
        connect_mt5()
        data = get_eurusd_data()
        result = detect_flag_pattern(data)
        if result:
            return Response({"flag_detected": True, "details": result})
        return Response({"flag_detected": False, "details": None})