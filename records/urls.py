from django.urls import path
from .views import *
from .payment_views import *

urlpatterns = [
    # Views for creation
    path('<int:pawnshop_id>/record/<int:record_id>/create-payment/',
         CreatePaymentView.as_view(), name='create_payment'),
    path('<int:pawnshop_id>/record/<int:record_id>/resell/',
         CreateResellView.as_view(), name='create_resell'),
    path('<int:pawnshop_id>/record/<int:record_id>/retrieve/',
         retrieveItem, name='retrieve'),
    path('create/', CreatePawnshopView.as_view(), name='create_pawnshop'),
    path('<int:pawnshop_id>/create/',
         CreateRecordView.as_view(), name='create_record'),
    # Views for detail
    path('', PawnshopListView.as_view(), name='index'),
    path('<int:pawnshop_id>/', RecordIndex.as_view(), name='record_index'),
    path('<int:pawnshop_id>/record/<int:record_id>/',
         RecordDetail.as_view(), name='record_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('pawnshop/<int:pawnshop_id>/record/<int:record_id>/edit/',
         EditRecordView.as_view(), name='edit_record'),

]
