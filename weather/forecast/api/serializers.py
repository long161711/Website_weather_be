from rest_framework.serializers import ModelSerializer
from forecast.models import DuLieu_ThoiTiet


class DuLieu_ThoiTiet_Serializer(ModelSerializer):
    class Meta:
        model = DuLieu_ThoiTiet
        fields = "__all__"