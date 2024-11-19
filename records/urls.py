from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreatePawnshopView.as_view(), name='create_pawnshop'),
    path('<int:pawnshop_id>/create/', CreateRecordView.as_view(), name='create_record'),
    path('', PawnshopListView.as_view(), name='index'),
    path('<int:pawnshop_id>/', RecordIndex.as_view(), name='record_index'),
    path('<int:pawnshop_id>/record/<int:record_id>/', RecordDetail.as_view(), name='record_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
