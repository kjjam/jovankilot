from django.contrib import admin
from jalali_date import datetime2jalali

from installation.models import Customer, Craftsman, Request, SMSPanelPattern


@admin.register(SMSPanelPattern)
class SMSPanelPattern(admin.ModelAdmin):
    list_display = ["stage", "pattern_code", "panel_number"]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["fullname", "number"]


@admin.register(Craftsman)
class CraftsmanAdmin(admin.ModelAdmin):
    list_display = ["fullname", "number"]


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ["customer", "get_number", "installer", "get_timing_jalali", "status", "web_id"]
    fieldsets = [("شناسه درخواست", {"fields": ["web_id"]}), ("مشتری", {"fields": ["customer", "request"]}),
                 ("استادکار", {"fields": ["installer", "descriptions", "status", "timing"]}),
                 ]
    readonly_fields = ["web_id"]

    @admin.display(ordering='book__author', description='شماره مشتری')
    def get_number(self, obj):
        return obj.customer.number

    @admin.display(description='تاریخ برای مراجعه')
    def get_timing_jalali(self, obj):
        return datetime2jalali(obj.timing).strftime('%Y/%m/%d  %H:%M')
