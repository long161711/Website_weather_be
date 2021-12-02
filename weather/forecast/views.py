# import datetime
#
# from django.shortcuts import render
#
# # Create your views here.
# from django.views import View
# from rest_framework.response import Response
# from django.http import HttpResponse
# from .models import thoitiet
# from .MoHinhDuDoan import RNN,CapnhatDulieu,chaymai
# from tensorflow import keras
# from datetime import date
# import numpy as np
# def KiemTraDB(today_daco):
#     Data_daco = thoitiet.objects.all()
#     today = today_daco
#     for data in Data_daco:
#         if data.thoigian == today_daco:
#             today_daco = today_daco + datetime.timedelta(days=1)
#     if today_daco == today:
#         today_daco = today_daco - datetime.timedelta(days=1)
#         return KiemTraDB(today_daco)
#     else:
#         # print(today_daco)
#         return today_daco
# class CapNhatDB(View):
#     def get(self, request):
#         Data_thoitiet = thoitiet.objects.all()
#         if len(Data_thoitiet) == 0:
#             CapnhatDulieu()
#         # Data_daco = thoitiet.objects.all()
#         today = date.today()
#         today_daco = date.today()
#         today_daco = KiemTraDB(today_daco)
#         songaydudoan =today - today_daco
#         songaycandudoan = 7 + songaydudoan.days
#
#
#         model_nhietdocaonhat = keras.Sequential()
#         RNN("T2M_MAX", model_nhietdocaonhat, 15)
#         # dudoan_nhietdocaonhat = model_nhietdocaonhat.predict(nhietdocaonhat)
#         model_nhietdothapnhat = keras.Sequential()
#         RNN("T2M_MIN", model_nhietdothapnhat, 15)
#         # dudoan_nhietdothapnhat = model_nhietdothapnhat.predict(nhietdothapnhat)
#         # if dudoan_nhietdothapnhat < dudoan_nhietdocaonhat:
#         #     row_thoitiet.nhietdothapnhat = dudoan_nhietdothapnhat
#         #     row_thoitiet.nhietdocaonhat = dudoan_nhietdocaonhat
#         # else:
#         #     row_thoitiet.nhietdocaonhat = dudoan_nhietdothapnhat
#         #     row_thoitiet.nhietdothapnhat = dudoan_nhietdocaonhat
#         model_doam = keras.Sequential()
#         RNN("RH2M", model_doam, 15)
#         # dudoan_doam = model_doam.predict(doam)
#         # row_thoitiet.doam = dudoan_doam
#         model_luongmua = keras.Sequential()
#         RNN("PRECTOTCORR", model_luongmua, 15)
#         # dudoan_luongmua = model_luongmua.predict(luongmua)
#         # row_thoitiet.luongmua = dudoan_luongmua
#         model_tocdogio = keras.Sequential()
#         RNN("WS50M_RANGE", model_tocdogio, 15)
#         # dudoan_tocdogio = model_tocdogio.predict(tocdogio)
#         # row_thoitiet.tocdogio = dudoan_tocdogio
#
#         for i in range(songaycandudoan):
#             nhietdocaonhat, nhietdothapnhat, doam, luongmua, tocdogio = [],[],[],[],[]
#             for k in range(30):
#                 tg_gannhat = today_daco - datetime.timedelta(days=k+1)
#                 # print(tg_gannhat)
#                 data = thoitiet.objects.filter(thoigian=tg_gannhat)
#                 for dulieu in data:
#                     nhietdocaonhat.insert(0, dulieu.nhietdocaonhat)
#                     nhietdothapnhat.insert(0,dulieu.nhietdothapnhat)
#                     doam.insert(0, dulieu.doam)
#                     luongmua.insert(0, dulieu.luongmua)
#                     tocdogio.insert(0, dulieu.tocdogio)
#             # print(nhietdocaonhat, nhietdothapnhat, doam, luongmua, tocdogio)
#             nhietdocaonhat = [nhietdocaonhat]
#             nhietdocaonhat = np.expand_dims(nhietdocaonhat, axis=2)
#             # print(nhietdocaonhat)
#             nhietdothapnhat = [nhietdothapnhat]
#             nhietdothapnhat = np.expand_dims(nhietdothapnhat, axis=2)
#             # print(nhietdothapnhat)
#             doam = [doam]
#             doam = np.expand_dims(doam, axis=2)
#             # print(doam)
#             luongmua =[luongmua]
#             luongmua = np.expand_dims(luongmua, axis=2)
#             # print(luongmua)
#             tocdogio = [tocdogio]
#             tocdogio = np.expand_dims(tocdogio, axis=2)
#             # print(tocdogio)
#             row_thoitiet = thoitiet()
#             row_thoitiet.thoigian = today_daco
#             print("alo")
#             print(today_daco)
#             today_daco = today_daco + datetime.timedelta(days=1)
#             dudoan_nhietdocaonhat = model_nhietdocaonhat.predict(nhietdocaonhat)
#             dudoan_nhietdothapnhat = model_nhietdothapnhat.predict(nhietdothapnhat)
#             if dudoan_nhietdothapnhat < dudoan_nhietdocaonhat:
#                 row_thoitiet.nhietdothapnhat = dudoan_nhietdothapnhat[0][0]
#                 row_thoitiet.nhietdocaonhat = dudoan_nhietdocaonhat[0][0]
#                 # print(dudoan_nhietdocaonhat[0][0])
#                 # print(dudoan_nhietdothapnhat[0][0])
#             else:
#                 row_thoitiet.nhietdocaonhat = dudoan_nhietdothapnhat[0][0]
#                 row_thoitiet.nhietdothapnhat = dudoan_nhietdocaonhat[0][0]
#                 # print(dudoan_nhietdothapnhat[0][0])
#                 # print(dudoan_nhietdocaonhat[0][0])
#             dudoan_doam = model_doam.predict(doam)
#             row_thoitiet.doam = dudoan_doam[0][0]
#             # print(dudoan_doam[0][0])
#             dudoan_luongmua = model_luongmua.predict(luongmua)
#             if dudoan_luongmua[0][0] < 0 :
#                 row_thoitiet.luongmua = 0
#                 # print(0)
#             else :
#                 row_thoitiet.luongmua = dudoan_luongmua[0][0]
#                 # print(dudoan_luongmua[0][0])
#             dudoan_tocdogio = model_tocdogio.predict(tocdogio)
#             if dudoan_tocdogio[0][0] < 0:
#                 row_thoitiet.tocdogio = 0
#                 # print(0)
#             else:
#                 # print(dudoan_tocdogio[0][0])
#                 row_thoitiet.tocdogio = dudoan_tocdogio[0][0]
#             row_thoitiet.save()
#         # print(songaydudoan.days)
#         # HamKiemTra(nam,thang,ngay)
#         # dudoandulieu(nam,thang,ngay)
#
#
#
#         # nd_max, nd_min, doam , luongmua, tocdogio = [], [], [] , [], []
#         # Data = thoitiet.object.all()
#         # for i in (0,30):
#
#
#         # for item in Data:
#         #     if Data.nam == nam and Data.thang == thang and Data.ngay == ngay:
#         #         data_thoigian_tien(nam,thang,ngay)
#         #         ngaydudoan = ngaydudoan+1
#         #     else :
#         #         data_thoigian_lui(nam,thang,ngay)
#
#
#
#         # model = keras.Sequential()
#         # RNN("T2M",model,13)
#         return HttpResponse("hay nhi")