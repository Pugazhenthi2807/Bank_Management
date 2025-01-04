from django.urls import path
from .views import (
    account_list, account_create, account_update, account_delete,
    transfer_view, transfer_success, transfer_history
)

urlpatterns = [
    path('', account_list, name='account_list'),
    path('accounts/create/', account_create, name='account_create'),
    path('accounts/update/<int:pk>/', account_update, name='account_update'),
    path('accounts/delete/<int:pk>/', account_delete, name='account_delete'),
    path('transfer/', transfer_view, name='transfer'),
    path('transfer/success/', transfer_success, name='transfer_success'),
    path('transfer/history/', transfer_history, name='transfer_history'),
]
