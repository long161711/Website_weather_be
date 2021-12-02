from django.db import models

# Create your models here.

class ThanhPho(models.Model):
    name = models.CharField(max_length=255)

class DuLieu_ThoiTiet(models.Model):
    id_thanhpho = models.ForeignKey(ThanhPho, on_delete=models.CASCADE)
    thoigian = models.DateField()
    nhietdocaonhat = models.FloatField()
    nhietdothapnhat = models.FloatField()
    doam = models.FloatField()
    luongmua = models.FloatField()
    tocdogio = models.FloatField()

