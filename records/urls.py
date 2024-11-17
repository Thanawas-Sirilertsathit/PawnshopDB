from django.urls import path
from .views import *
from .payment_views import *

urlpatterns = [
    # Views for creation
    path('<int:pawnshop_id>/record/<int:record_id>/create-payment/', CreatePaymentView.as_view(), name='create_payment'),
    path('create/', CreatePawnshopView.as_view(), name='create_pawnshop'),
    path('<int:pawnshop_id>/create/', CreateRecordView.as_view(), name='create_record'),
    # Views for detail
    path('', PawnshopListView.as_view(), name='index'),
    path('<int:pawnshop_id>/', RecordIndex.as_view(), name='record_index'),
    path('<int:pawnshop_id>/record/<int:record_id>/', RecordDetail.as_view(), name='record_detail'),
]

