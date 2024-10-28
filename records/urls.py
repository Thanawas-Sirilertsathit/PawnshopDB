from django.urls import path
from .views import RecordIndex, RecordDetail

urlpatterns = [
    path('', RecordIndex.as_view(), name='index'),
    path('<int:pk>/', RecordDetail.as_view(), name='record_detail'),
]
