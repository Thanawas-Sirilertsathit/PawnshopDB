from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecordIndex.as_view(), name='index'),
    path('<int:pk>/', views.RecordDetail.as_view(), name='record_detail'),

    path('get-csrf-token/', views.util.csrf_token_view, name='get_csrf_token'),
]
