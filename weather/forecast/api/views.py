import datetime

from rest_framework.viewsets import ModelViewSet
from .serializers import  DuLieu_ThoiTiet_Serializer
from forecast.models import DuLieu_ThoiTiet
from forecast.MoHinhDuDoan_all import chaymai,aloalo
# from forecast.MoHinhDuDoan_all import chaymai,aloalo
from datetime import date

class Forecast_HN(ModelViewSet):
    serializer_class = DuLieu_ThoiTiet_Serializer
    def get_queryset(self):
        chaymai()
        date_hientai = date.today()
        print(date_hientai)
        queryset = DuLieu_ThoiTiet.objects.filter(thoigian=date_hientai, id_thanhpho =1)
        for i in range(6):
            date_hientai = date_hientai + datetime.timedelta(days=1)
            queryset = queryset | DuLieu_ThoiTiet.objects.filter(thoigian=date_hientai, id_thanhpho =1)
        return queryset
class Forecast_DN(ModelViewSet):
    serializer_class = DuLieu_ThoiTiet_Serializer
    def get_queryset(self):
        chaymai()
        date_hientai = date.today()
        print(date_hientai)
        queryset = DuLieu_ThoiTiet.objects.filter(thoigian=date_hientai, id_thanhpho =2)
        for i in range(6):
            date_hientai = date_hientai + datetime.timedelta(days=1)
            queryset = queryset | DuLieu_ThoiTiet.objects.filter(thoigian=date_hientai, id_thanhpho =2)
        return queryset
class Forecast_HCM(ModelViewSet):
    serializer_class = DuLieu_ThoiTiet_Serializer
    def get_queryset(self):
        chaymai()
        date_hientai = date.today()
        print(date_hientai)
        queryset = DuLieu_ThoiTiet.objects.filter(thoigian=date_hientai, id_thanhpho =3)
        for i in range(6):
            date_hientai = date_hientai + datetime.timedelta(days=1)
            queryset = queryset | DuLieu_ThoiTiet.objects.filter(thoigian=date_hientai, id_thanhpho =3)
        return queryset

class DataWeather_HN(ModelViewSet):
    serializer_class = DuLieu_ThoiTiet_Serializer
    def get_queryset(self):
        chaymai()
        date_hientai = date.today()

        queryset =  DuLieu_ThoiTiet.objects.filter(thoigian=date_hientai,id_thanhpho=1)
        for i in range(20):
            date_hientai = date_hientai - datetime.timedelta(days=1)
            queryset = queryset | DuLieu_ThoiTiet.objects.filter(thoigian = date_hientai,id_thanhpho=1)
        return queryset
class DataWeather_DN(ModelViewSet):
    serializer_class = DuLieu_ThoiTiet_Serializer
    def get_queryset(self):
        date_hientai = date.today()
        chaymai()
        queryset =  DuLieu_ThoiTiet.objects.filter(thoigian=date_hientai,id_thanhpho=2)
        for i in range(20):
            date_hientai = date_hientai - datetime.timedelta(days=1)
            queryset = queryset | DuLieu_ThoiTiet.objects.filter(thoigian = date_hientai,id_thanhpho=2)
        return queryset
class DataWeather_HCM(ModelViewSet):
    serializer_class = DuLieu_ThoiTiet_Serializer
    def get_queryset(self):
        date_hientai = date.today()
        chaymai()
        queryset =  DuLieu_ThoiTiet.objects.filter(thoigian=date_hientai,id_thanhpho=3)
        for i in range(20):
            date_hientai = date_hientai - datetime.timedelta(days=1)
            queryset = queryset | DuLieu_ThoiTiet.objects.filter(thoigian = date_hientai,id_thanhpho=3)
        return queryset
