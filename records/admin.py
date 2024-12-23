from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Record, Pawnshop, Profile


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'loan_amount')
    search_fields = ('name',)


@admin.register(Pawnshop)
class PawnshopAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user', 'role')
