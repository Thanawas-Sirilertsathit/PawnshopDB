from django.urls import path
from . import views

urlpatterns = [
    path('', views.PawnshopList.as_view(), name='pawnshop_index'),
    path('record/', views.RecordList.as_view(), name='record_index'),
    path('record/<int:pk>/', views.RecordDetail.as_view(), name='record_detail'),

    path('get-csrf-token/', views.util.csrf_token_view, name='get_csrf_token'),
]
