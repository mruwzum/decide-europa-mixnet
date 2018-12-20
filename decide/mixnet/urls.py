from django.urls import path, include
from rest_framework import routers
from . import views
from .views import zkpView

router = routers.DefaultRouter()
router.register(r'', views.MixnetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('shuffle/<int:voting_id>/', views.Shuffle.as_view(), name='shuffle'),
    path('decrypt/<int:voting_id>/', views.Decrypt.as_view(), name='decrypt'),
    #path('zkp/', views.zkpView, name='zkp'),
    path('zkp', zkpView.as_view(), name='zkp'),
    path('zkp/test', views.vistaZkp, name='zkp'),
    path('menu', views.menu, name='menu'),
    path('prueba/simetrica', views.vistaSimetrica, name='simetrica'),
    path('cargarpk', views.cargarpk, name='cargarpk'),
]
