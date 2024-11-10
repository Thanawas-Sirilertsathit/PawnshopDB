from django.urls import path
from .views import RecordIndex, RecordDetail, PawnshopListView, CreatePawnshopView

urlpatterns = [
    path('create/', CreatePawnshopView.as_view(), name='create_pawnshop'),
    path('', PawnshopListView.as_view(), name='index'),
    path('<int:pawnshop_id>/', RecordIndex.as_view(), name='record_index'),
    path('<int:pawnshop_id>/record/<int:record_id>/', RecordDetail.as_view(), name='record_detail'),
]
