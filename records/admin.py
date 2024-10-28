from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Record

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'loan_amount')
    search_fields = ('name',)
