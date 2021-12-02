from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('forecast_HN', Forecast_HN , basename='HN')
router.register('forecast_DN', Forecast_DN , basename='DN')
router.register('forecast_DCM', Forecast_HCM , basename='HCM')

router.register('data_weather_HN', DataWeather_HN , basename='Data_HN')
router.register('data_weather_DN', DataWeather_DN , basename='Data_DN')
router.register('data_weather_HCM', DataWeather_HCM , basename='Data_HCM')

urlpatterns = router.urls