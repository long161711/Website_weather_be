import pandas as pd
import numpy as np
from datetime import date
import datetime
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [20, 5]
import datetime as dt
from sklearn import metrics
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from .models import DuLieu_ThoiTiet,ThanhPho
import datetime
import requests

DuLieu_ThoiTiet.objects.all().delete()
DL_input = 30
df_HaNoi = pd.read_csv('forecast\HANOI.csv', header=14)
df_DaNang = pd.read_csv('forecast\DANANG.csv', header=14)
df_HCM = pd.read_csv('forecast\HOCHIMINH.csv', header=14)

# loại bỏ dữ liệu không đầy đủ
df_HaNoi = df_HaNoi.dropna(axis=0, how='any')
df_DaNang = df_DaNang.dropna(axis=0, how='any')
df_HCM = df_HCM.dropna(axis=0, how='any')

def CapNhatData_Weather(Diadiem, df):
    data = df[['YEAR', 'MO', 'DY', 'T2M_MAX', 'T2M_MIN', 'RH2M', 'PRECTOTCORR', 'WS10M_RANGE']].values
    dulieu = []
    for i in range((len(data)-DL_input) , (len(data))):
        dulieu.append(data[i])
    id_TP = 0
    if Diadiem == 'HaNoi':
        id_TP = 1
    if Diadiem == 'DaNang':
        id_TP = 2
    if Diadiem == 'HCM':
        id_TP = 3
    for j in range(len(dulieu)):
        # row_thoitiet = DuLieu_ThoiTiet()
        # row_thoitiet.id_thanhpho = id_TP
        thanhpho_object = ThanhPho.objects.get(pk=id_TP)
        print("!")
        print(thanhpho_object)
        # row_thoitiet = Data_thoitiet.objects.create(id_thanhpho=1)
        todayss = datetime.datetime(int(dulieu[j][0]), int(dulieu[j][1]), int(dulieu[j][2]))
        # row_thoitiet.thoigian = todayss.date()
        # row_thoitiet.nhietdocaonhat = dulieu[j][3]
        # row_thoitiet.nhietdothapnhat = dulieu[j][4]
        # row_thoitiet.doam = dulieu[j][5]
        # row_thoitiet.luongmua = dulieu[j][6]
        # row_thoitiet.tocdogio = dulieu[j][7]
        # row_thoitiet.save()

        DuLieu_ThoiTiet.objects.create(thoigian=todayss.date(),nhietdocaonhat = dulieu[j][3], nhietdothapnhat = dulieu[j][4],doam = dulieu[j][5],luongmua = dulieu[j][6],tocdogio = dulieu[j][7],id_thanhpho = thanhpho_object)

        print(j)



Data_thoitiet = DuLieu_ThoiTiet.objects.all()
if len(Data_thoitiet) == 0:
    CapNhatData_Weather("HaNoi", df_HaNoi)
    CapNhatData_Weather("DaNang", df_DaNang)
    CapNhatData_Weather("HCM", df_HCM)

def KiemTraDB(today_daco):
    Data_daco = DuLieu_ThoiTiet.objects.filter(id_thanhpho = 1)
    today = today_daco
    for data in Data_daco:
        if data.thoigian == today_daco:
            today_daco = today_daco + datetime.timedelta(days=1)
    if today_daco == today:
        today_daco = today_daco - datetime.timedelta(days=1)
        return KiemTraDB(today_daco)
    else:
        # print(today_daco)
        return today_daco


def ThemPhanConThieu(date_dau,date_cuoi,thanhpho):
    id_TP = 0
    if thanhpho == 'HaNoi':
        id_TP = 1
    if thanhpho == 'DaNang':
        id_TP = 2
    if thanhpho == 'HoChiMinh':
        id_TP = 3
    url = "https://visual-crossing-weather.p.rapidapi.com/history"

    querystring = {"startDateTime": date_dau, "aggregateHours": "24", "location": thanhpho,
                   "endDateTime": date_cuoi, "unitGroup": "metric", "contentType": "json", "shortColumnNames": "0"}

    headers = {
        'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com",
        'x-rapidapi-key': "5cb76fd66emsh144331b62e1243ap10c9f0jsnac19f58b74ed"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    # print(response.text)
    alo = response.json()
    songaycanthem = date_cuoi-date_dau
    for i in range(songaycanthem.days+1):
        print(alo['locations'][thanhpho]['values'][i]['datetimeStr'])
        date_str = alo['locations'][thanhpho]['values'][i]['datetimeStr']
        date_format = "%Y-%m-%dT%H:%M:%S+07:%f"
        dt = datetime.datetime.strptime(date_str, date_format)
        print(dt.date())
        print(alo['locations'][thanhpho]['values'][i]['maxt'])
        print(alo['locations'][thanhpho]['values'][i]['mint'])
        print(alo['locations'][thanhpho]['values'][i]['humidity'])
        print(alo['locations'][thanhpho]['values'][i]['precip'])
        print(alo['locations'][thanhpho]['values'][i]['wspd'])
        thanhpho_object = ThanhPho.objects.get(id=id_TP)

        d1 = dt.date()
        ndmax = alo['locations'][thanhpho]['values'][i]['maxt']
        ndmin = alo['locations'][thanhpho]['values'][i]['mint']
        da = alo['locations'][thanhpho]['values'][i]['humidity']
        lm = alo['locations'][thanhpho]['values'][i]['precip']
        tdg= alo['locations'][thanhpho]['values'][i]['wspd']
        DuLieu_ThoiTiet.objects.create(id_thanhpho=thanhpho_object,thoigian = d1,nhietdocaonhat = ndmax,nhietdothapnhat=ndmin,luongmua =lm,doam = da,tocdogio=tdg)

today = date.today()
today_daco = date.today()
today_daco = KiemTraDB(today_daco)
songaycapnhat =today - today_daco
if(songaycapnhat.days>1):
    print(songaycapnhat.days)
    today_dau = today - datetime.timedelta(days=songaycapnhat.days)
    print(today_dau)
    today_cuoi = today-datetime.timedelta(days=1)
    print(today_cuoi)
    ThemPhanConThieu(today_dau,today_cuoi,"HaNoi")
    ThemPhanConThieu(today_dau, today_cuoi, "DaNang")
    ThemPhanConThieu(today_dau, today_cuoi, "HoChiMinh")


solanchayAI = 1
def RNN(thongso , model, epoch, df):
    data = df[thongso].values
    X, Y = [], []
    seq_len = DL_input
    num_records = len(data) - seq_len
    for i in range(num_records):
        X.append(data[i:i + seq_len])
        Y.append(data[i + seq_len])
    X = np.array(X)
    X = np.expand_dims(X, axis=2)
    Y = np.array(Y)
    Y = np.expand_dims(Y, axis=1)
    # Tách dataset để giữ lại bộ test: Là bộ ta đánh giá cuối cùng sau khi train
    X, X_test, Y, Y_test = train_test_split(X, Y, test_size=0.15, shuffle=False)

    # tách dataset thành train và val: Đánh giá trong lúc train
    X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2, shuffle=False)
    # model = keras.Sequential()
    model.add(layers.InputLayer(input_shape=(seq_len, 1)))  # 1 chuỗi (sample) có seq_len số, 1-dimension
    model.add(layers.SimpleRNN(256))  # number of hidden state
    model.add(layers.Dense(512))
    model.add(layers.Dropout(0.01))
    model.add(layers.Dense(128))
    model.add(layers.Dense(1))  # 1 value - output dự đoán
    model.summary()
    model.compile(optimizer="Adam", loss="mse")  # Mean-squared Error
    hist = model.fit(X_train, Y_train, validation_data=(X_val, Y_val),
                     epochs=epoch, verbose=1, shuffle=False)
    print("solanchay AI")

model_nhietdocaonhat_HaNoi = keras.Sequential()
RNN("T2M_MAX", model_nhietdocaonhat_HaNoi, 15 , df_HaNoi)
model_nhietdocaonhat_DaNang = keras.Sequential()
RNN("T2M_MAX", model_nhietdocaonhat_DaNang, 15 , df_DaNang)
model_nhietdocaonhat_HCM = keras.Sequential()
RNN("T2M_MAX", model_nhietdocaonhat_HCM, 15 , df_HCM)
#
model_nhietdothapnhat_HaNoi = keras.Sequential()
RNN("T2M_MIN", model_nhietdothapnhat_HaNoi, 15, df_HaNoi)
model_nhietdothapnhat_DaNang = keras.Sequential()
RNN("T2M_MIN", model_nhietdothapnhat_DaNang, 15 , df_DaNang)
model_nhietdothapnhat_HCM = keras.Sequential()
RNN("T2M_MIN", model_nhietdothapnhat_HCM, 15 , df_HCM)
#
model_doam_HaNoi = keras.Sequential()
RNN("RH2M", model_doam_HaNoi, 15 ,df_HaNoi)
model_doam_DaNang = keras.Sequential()
RNN("RH2M", model_doam_DaNang, 15 ,df_DaNang)
model_doam_HCM = keras.Sequential()
RNN("RH2M", model_doam_HCM, 15 ,df_HCM)
#
model_luongmua_HaNoi = keras.Sequential()
RNN("PRECTOTCORR", model_luongmua_HaNoi, 15 , df_HaNoi)
model_luongmua_DaNang = keras.Sequential()
RNN("PRECTOTCORR", model_luongmua_DaNang, 15 , df_DaNang)
model_luongmua_HCM = keras.Sequential()
RNN("PRECTOTCORR", model_luongmua_HCM, 15 , df_HCM)

model_tocdogio_HaNoi = keras.Sequential()
RNN("WS10M_RANGE", model_tocdogio_HaNoi, 15 , df_HaNoi)
model_tocdogio_DaNang = keras.Sequential()
RNN("WS10M_RANGE", model_tocdogio_DaNang, 15 , df_DaNang)
model_tocdogio_HCM = keras.Sequential()
RNN("WS10M_RANGE", model_tocdogio_HCM, 15 , df_HCM)

today_khongthaydoi = date.today()
today = date.today()
Data_thoitiethientai= DuLieu_ThoiTiet.objects.filter(thoigian=today , id =1)

if len(Data_thoitiethientai) == 0:
    id_ThanhPho = 0
    for j in range(3):
        print("alo jjjjjjjjjjjjjjjjjjjjjjjjj")
        print(j)
        id_ThanhPho = id_ThanhPho + 1
        today = today_khongthaydoi

        model_nhietdocaonhat = keras.Sequential()
        model_nhietdothapnhat = keras.Sequential()
        model_doam = keras.Sequential()
        model_luongmua = keras.Sequential()
        model_tocdogio = keras.Sequential()

        if id_ThanhPho == 1 :
            model_nhietdocaonhat = model_nhietdocaonhat_HaNoi
            model_nhietdothapnhat = model_nhietdothapnhat_HaNoi
            model_doam = model_doam_HaNoi
            model_tocdogio = model_tocdogio_HaNoi
            model_luongmua = model_luongmua_HaNoi
        if id_ThanhPho == 2 :
            model_nhietdocaonhat = model_nhietdocaonhat_DaNang
            model_nhietdothapnhat = model_nhietdothapnhat_DaNang
            model_doam = model_doam_DaNang
            model_tocdogio = model_tocdogio_DaNang
            model_luongmua = model_luongmua_DaNang
        if id_ThanhPho == 3 :
            model_nhietdocaonhat = model_nhietdocaonhat_HCM
            model_nhietdothapnhat = model_nhietdothapnhat_HCM
            model_doam = model_doam_HCM
            model_tocdogio = model_tocdogio_HCM
            model_luongmua = model_luongmua_HCM
        Data_thanhpho = ThanhPho.objects.get(pk = id_ThanhPho)

        for i in range(7):
            nhietdocaonhat, nhietdothapnhat, doam, luongmua, tocdogio = [], [], [], [], []
            for k in range(30):
                tg_gannhat = today - datetime.timedelta(days=k + 1)
                # print(tg_gannhat)
                data = DuLieu_ThoiTiet.objects.filter(thoigian=tg_gannhat, id_thanhpho = id_ThanhPho)
                for dulieu in data:
                    nhietdocaonhat.insert(0, dulieu.nhietdocaonhat)
                    nhietdothapnhat.insert(0, dulieu.nhietdothapnhat)
                    doam.insert(0, dulieu.doam)
                    luongmua.insert(0, dulieu.luongmua)
                    tocdogio.insert(0, dulieu.tocdogio)
            # print(nhietdocaonhat, nhietdothapnhat, doam, luongmua, tocdogio)
            nhietdocaonhat = [nhietdocaonhat]
            nhietdocaonhat = np.expand_dims(nhietdocaonhat, axis=2)
            # print(nhietdocaonhat)
            nhietdothapnhat = [nhietdothapnhat]
            nhietdothapnhat = np.expand_dims(nhietdothapnhat, axis=2)
            # print(nhietdothapnhat)
            doam = [doam]
            doam = np.expand_dims(doam, axis=2)
            # print(doam)
            luongmua = [luongmua]
            luongmua = np.expand_dims(luongmua, axis=2)
            # print(luongmua)
            tocdogio = [tocdogio]
            tocdogio = np.expand_dims(tocdogio, axis=2)
            # print(tocdogio)

            row_thoitiet = DuLieu_ThoiTiet()

            row_thoitiet.id_thanhpho = Data_thanhpho
            row_thoitiet.thoigian = today
            today = today + datetime.timedelta(days=1)
            dudoan_nhietdocaonhat = model_nhietdocaonhat.predict(nhietdocaonhat)
            dudoan_nhietdothapnhat = model_nhietdothapnhat.predict(nhietdothapnhat)
            if dudoan_nhietdothapnhat < dudoan_nhietdocaonhat:
                a = float("{:.2f}".format(dudoan_nhietdothapnhat[0][0]))
                b = float("{:.2f}".format(dudoan_nhietdocaonhat[0][0]))
                row_thoitiet.nhietdothapnhat = a
                row_thoitiet.nhietdocaonhat = b
                # print(dudoan_nhietdocaonhat[0][0])
                # print(dudoan_nhietdothapnhat[0][0])
            else:
                a = float("{:.2f}".format(dudoan_nhietdothapnhat[0][0]))
                b = float("{:.2f}".format(dudoan_nhietdocaonhat[0][0]))
                row_thoitiet.nhietdocaonhat =a
                row_thoitiet.nhietdothapnhat = b
                # print(dudoan_nhietdothapnhat[0][0])
                # print(dudoan_nhietdocaonhat[0][0])
            dudoan_doam = model_doam.predict(doam)
            c = float("{:.2f}".format(dudoan_doam[0][0]))
            row_thoitiet.doam = c
            # print(dudoan_doam[0][0])
            dudoan_luongmua = model_luongmua.predict(luongmua)
            if dudoan_luongmua[0][0] < 0:
                row_thoitiet.luongmua = 0
                # print(0)
            else:
                d = float("{:.2f}".format(dudoan_luongmua[0][0]))
                row_thoitiet.luongmua = d
                # print(dudoan_luongmua[0][0])
            dudoan_tocdogio = model_tocdogio.predict(tocdogio)
            if dudoan_tocdogio[0][0] < 0:
                row_thoitiet.tocdogio = 0
                # print(0)
            else:
                # print(dudoan_tocdogio[0][0])
                e = float("{:.2f}".format(dudoan_tocdogio[0][0]))
                row_thoitiet.tocdogio = e
            row_thoitiet.save()

def update_data_weather(chinhxac,today,thanhpho, id_thanhpho):

    url = "https://visual-crossing-weather.p.rapidapi.com/history"

    querystring = {"startDateTime": chinhxac, "aggregateHours": "24", "location": thanhpho,
                   "endDateTime": today, "unitGroup": "metric", "contentType": "json", "shortColumnNames": "0"}
    headers = {
        'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com",
        'x-rapidapi-key': "5cb76fd66emsh144331b62e1243ap10c9f0jsnac19f58b74ed"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    # print(response.text)
    alo = response.json()
    songaycanthem = today - chinhxac
    for i in range(songaycanthem.days):
        date_str = alo['locations'][thanhpho]['values'][i]['datetimeStr']
        date_format = "%Y-%m-%dT%H:%M:%S+07:%f"
        dt = datetime.datetime.strptime(date_str, date_format)
        # row_thoitiet = thoitiet.objects.filter(thoigian=dt.date())
        DuLieu_ThoiTiet.objects.filter(thoigian=dt.date(),id_thanhpho= id_thanhpho).update(
            nhietdocaonhat=alo['locations'][thanhpho]['values'][i]['maxt'])
        DuLieu_ThoiTiet.objects.filter(thoigian=dt.date(),id_thanhpho= id_thanhpho).update(
            nhietdothapnhat=alo['locations'][thanhpho]['values'][i]['mint'])
        DuLieu_ThoiTiet.objects.filter(thoigian=dt.date(),id_thanhpho= id_thanhpho).update(
            doam=alo['locations'][thanhpho]['values'][i]['humidity'])
        DuLieu_ThoiTiet.objects.filter(thoigian=dt.date(),id_thanhpho= id_thanhpho).update(
            luongmua=alo['locations'][thanhpho]['values'][i]['precip'])
        DuLieu_ThoiTiet.objects.filter(thoigian=dt.date(),id_thanhpho= id_thanhpho).update(
            tocdogio=alo['locations'][thanhpho]['values'][i]['wspd'])

        # row_thoitiet.nhietdocaonhat = alo['locations']['Danang']['values'][i]['maxt']
        # row_thoitiet.nhietdothapnhat = alo['locations']['Danang']['values'][i]['mint']
        # row_thoitiet.doam = alo['locations']['Danang']['values'][i]['humidity']
        # row_thoitiet.luongmua = alo['locations']['Danang']['values'][i]['precip']
        # row_thoitiet.tocdogio = alo['locations']['Danang']['values'][i]['wspd']
        # row_thoitiet.save()
        for i in range(7):
            nhietdocaonhat, nhietdothapnhat, doam, luongmua, tocdogio = [], [], [], [], []
            for k in range(30):
                tg_gannhat = today - datetime.timedelta(days=k + 1)
                # print(tg_gannhat)
                data = DuLieu_ThoiTiet.objects.filter(thoigian=tg_gannhat,id_thanhpho=id_thanhpho)
                for dulieu in data:
                    nhietdocaonhat.insert(0, dulieu.nhietdocaonhat)
                    nhietdothapnhat.insert(0, dulieu.nhietdothapnhat)
                    doam.insert(0, dulieu.doam)
                    luongmua.insert(0, dulieu.luongmua)
                    tocdogio.insert(0, dulieu.tocdogio)
            # print(nhietdocaonhat, nhietdothapnhat, doam, luongmua, tocdogio)
            nhietdocaonhat = [nhietdocaonhat]
            nhietdocaonhat = np.expand_dims(nhietdocaonhat, axis=2)
            # print(nhietdocaonhat)
            nhietdothapnhat = [nhietdothapnhat]
            nhietdothapnhat = np.expand_dims(nhietdothapnhat, axis=2)
            # print(nhietdothapnhat)
            doam = [doam]
            doam = np.expand_dims(doam, axis=2)
            # print(doam)
            luongmua = [luongmua]
            luongmua = np.expand_dims(luongmua, axis=2)
            # print(luongmua)
            tocdogio = [tocdogio]
            tocdogio = np.expand_dims(tocdogio, axis=2)
            # print(tocdogio)

            dudoan_nhietdocaonhat = model_nhietdocaonhat.predict(nhietdocaonhat)
            dudoan_nhietdothapnhat = model_nhietdothapnhat.predict(nhietdothapnhat)
            dudoan_doam = model_doam.predict(doam)
            # row_thoitiet.doam = dudoan_doam[0][0]
            # print(dudoan_doam[0][0])
            dudoan_luongmua = model_luongmua.predict(luongmua)
            dudoan_tocdogio = model_tocdogio.predict(tocdogio)
            row_thoitiet = DuLieu_ThoiTiet.objects.filter(thoigian=today,id_thanhpho=id_thanhpho)
            if len(row_thoitiet) == 1:
                if dudoan_nhietdothapnhat < dudoan_nhietdocaonhat:
                    a = float("{:.2f}".format(dudoan_nhietdothapnhat[0][0]))
                    b = float("{:.2f}".format(dudoan_nhietdocaonhat[0][0]))
                    DuLieu_ThoiTiet.objects.filter(thoigian=today, id_thanhpho = id_thanhpho).update(
                        nhietdothapnhat=a)
                    DuLieu_ThoiTiet.objects.filter(thoigian=today, id_thanhpho = id_thanhpho).update(
                        nhietdocaonhat=b)
                    # print(dudoan_nhietdocaonhat[0][0])
                    # print(dudoan_nhietdothapnhat[0][0])
                else:
                    a = float("{:.2f}".format(dudoan_nhietdothapnhat[0][0]))
                    b = float("{:.2f}".format(dudoan_nhietdocaonhat[0][0]))
                    DuLieu_ThoiTiet.objects.filter(thoigian=today, id_thanhpho = id_thanhpho).update(
                        nhietdocaonhat=a)
                    DuLieu_ThoiTiet.objects.filter(thoigian=today, id_thanhpho = id_thanhpho).update(
                        nhietdothapnhat=b)
                    # print(dudoan_nhietdothapnhat[0][0])
                    # print(dudoan_nhietdocaonhat[0][0])
                e = float("{:.2f}".format(dudoan_doam[0][0]))
                DuLieu_ThoiTiet.objects.filter(thoigian=today, id_thanhpho = id_thanhpho).update(
                    doam=e)
                if dudoan_luongmua[0][0] < 0:
                    DuLieu_ThoiTiet.objects.filter(thoigian=today, id_thanhpho = id_thanhpho).update(
                        luongmua=0)
                    # print(0)
                else:
                    c = float("{:.2f}".format(dudoan_luongmua[0][0]))
                    DuLieu_ThoiTiet.objects.filter(thoigian=today, id_thanhpho = id_thanhpho).update(
                        luongmua=c)
                    # print(dudoan_luongmua[0][0])
                if dudoan_tocdogio[0][0] < 0:
                    DuLieu_ThoiTiet.objects.filter(thoigian=today, id_thanhpho = id_thanhpho).update(
                        tocdogio=0)
                    # print(0)
                else:
                    # print(dudoan_tocdogio[0][0])
                    d = float("{:.2f}".format(dudoan_tocdogio[0][0]))
                    DuLieu_ThoiTiet.objects.filter(thoigian=today, id_thanhpho = id_thanhpho).update(
                        tocdogio=d)
            else :
                data_ThanhPho = ThanhPho.objects.get(pk = id_thanhpho)
                row_thoitiet = DuLieu_ThoiTiet()
                row_thoitiet.thoigian = data_ThanhPho
                # today = today + datetime.timedelta(days=1)
                # dudoan_nhietdocaonhat = model_nhietdocaonhat.predict(nhietdocaonhat)
                # dudoan_nhietdothapnhat = model_nhietdothapnhat.predict(nhietdothapnhat)
                if dudoan_nhietdothapnhat < dudoan_nhietdocaonhat:
                    a = float("{:.2f}".format(dudoan_nhietdothapnhat[0][0]))
                    b =float("{:.2f}".format(dudoan_nhietdocaonhat[0][0]))
                    row_thoitiet.nhietdothapnhat = a
                    row_thoitiet.nhietdocaonhat = b
                    # print(dudoan_nhietdocaonhat[0][0])
                    # print(dudoan_nhietdothapnhat[0][0])
                else:
                    a = float("{:.2f}".format(dudoan_nhietdothapnhat[0][0]))
                    b = float("{:.2f}".format(dudoan_nhietdocaonhat[0][0]))
                    row_thoitiet.nhietdocaonhat = a
                    row_thoitiet.nhietdothapnhat = b
                    # print(dudoan_nhietdothapnhat[0][0])
                    # print(dudoan_nhietdocaonhat[0][0])
                # dudoan_doam = model_doam.predict(doam)
                c = float("{:.2f}".format(dudoan_doam[0][0]))
                row_thoitiet.doam = c
                # # print(dudoan_doam[0][0])
                # dudoan_luongmua = model_luongmua.predict(luongmua)
                if dudoan_luongmua[0][0] < 0:
                    row_thoitiet.luongmua = 0
                    # print(0)
                else:
                    d= float("{:.2f}".format(dudoan_luongmua[0][0]))
                    row_thoitiet.luongmua = d
                    # print(dudoan_luongmua[0][0])
                # dudoan_tocdogio = model_tocdogio.predict(tocdogio)
                if dudoan_tocdogio[0][0] < 0:
                    row_thoitiet.tocdogio = 0
                    # print(0)
                else:
                    # print(dudoan_tocdogio[0][0])
                    e = float("{:.2f}".format(dudoan_tocdogio[0][0]))
                    row_thoitiet.tocdogio = e
                row_thoitiet.save()
            today = today + datetime.timedelta(days=1)
def chaymai():
    today = date.today()
    print(today)
    today_candudoanden = today + datetime.timedelta(days=6)
    today_daco = KiemTraDB(today_candudoanden)
    dulieuthieu = today_candudoanden - today_daco
    if(dulieuthieu.days == 0):
        print(today_daco)
        chinhxac = today - datetime.timedelta(days=1)
        id_thanhPho = 0
        for i in range(3):
            id_thanhPho = id_thanhPho +1
            if id_thanhPho == 1:
                update_data_weather(chinhxac,today,"HaNoi",id_thanhPho)
            if id_thanhPho == 2:
                update_data_weather(chinhxac, today, "DaNang", id_thanhPho)
            if id_thanhPho == 3:
                update_data_weather(chinhxac, today, "HoChiMinh", id_thanhPho)

def aloalo():
    print("aloalo")