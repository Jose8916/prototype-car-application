from django.urls import path
from .views import *

app_name = "guests"

urlpatterns = [
    path('transfer',TransferView.as_view(),name='transfer'),
    path('recharge',RechargeView.as_view(),name='recharge'),
    path('balance',BalanceList.as_view(),name='balance'),
    path('bonus',BonusesList.as_view(),name='balance_bonus'),
] 