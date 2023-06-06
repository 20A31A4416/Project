from . import models
from patient_management.models import staffPaymentLedger
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count, Sum
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.utils.translation import gettext_lazy as _

from utility.pcloud import getPubSmallThumb, deleteFile

from core.views import getAuth


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ("phoneNumber", "username", "email",
                    "last_login", 'is_active', 'total_payoffs', 'account_balance')
    search_fields = ("username", "phoneNumber", "email")
    list_filter = ("is_staff", "is_superuser",
                   "is_active", "groups", "isCustomer")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phoneNumber", "password1", "password2",),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("phoneNumber", "password")}),
        (_("Personal info"), {"fields": ("username", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    @admin.display(ordering='payoff')
    def total_payoffs(self, user):
        url = reverse('admin:patient_management_staffpaymentledger_changelist') + \
            '?' + urlencode({'user__id': user.id})
        if user.payoff:
            return format_html(f'<a href="{url}" target="_blank">{str(user.payoff)}</a>')
        return 0

    def account_balance(self, user):
        record = staffPaymentLedger.objects.filter(user=user.id).last()
        if record:
            return record.accountBalance
        else:
            return 0

    def get_queryset(self, request):
        return models.User.objects.filter(is_staff=1).annotate(payoff=Sum('accountLedger__creditValue'))


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    icon_name = "dashboard"
    list_display = ['title', 'appointments', 'Thumbnail']
    search_fields = ['title']

    @admin.display(ordering='appointmentCount')
    def appointments(self, category):
        url = reverse('admin:patient_management_appointment_changelist') + \
            '?' + urlencode({'category__id': category.id})
        return format_html(f'<a href={url}>{category.appointmentCount}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(appointmentCount=Count('appointment'))

    def Thumbnail(self, category):
        component = f"""
            <a href="{category.link}" target="_blank">
                <div style="width: 10rem;
                    height: 5.5rem;
                    background-image: url({getPubSmallThumb(category.pubCode, 300)});
                    background-size: cover;
                    display: inline-block;
                    transition: all 0.3s ease;
                    box-shadow: 0 0px 10px 0 #0000006e;
                    border-radius: 0.5rem;">
                </div>
	        </a>
        """
        return format_html(component)

    fieldsets = (
        (None, {
            "fields": ('title', 'description', 'thumbnail'),
        }),
    )

    def delete_queryset(self, request, queryset):
        for object in queryset:
            response = deleteFile(
                getAuth(), object.pcloudFileId)
            if response == 200:
                continue
            else:
                break
        else:
            return super().delete_queryset(request, queryset)


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    icon_name = "pin_drop"
    list_display = ['title', 'appointments']
    search_fields = ['title']

    @admin.display(ordering='appointmentCount')
    def appointments(self, city):
        url = reverse('admin:patient_management_appointment_changelist') + \
            '?' + urlencode({'city__id': city.id})
        return format_html(f'<a href={url}>{city.appointmentCount}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(appointmentCount=Count('appointment'))


@admin.register(models.PayMode)
class PayModeAdmin(admin.ModelAdmin):
    icon_name = "payment"
    list_display = ['title', 'transaction']
    search_fields = ['title']

    @admin.display(ordering='transactionCount')
    def transaction(self, paymode):
        url = reverse('admin:patient_management_transaction_changelist') + \
            '?' + urlencode({'paymode__id': paymode.id})
        return format_html(f'<a href={url}>{paymode.transactionCount}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(transactionCount=Count('transaction'))


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    icon_name = "assignment_ind"
    list_display = ['title']
    search_fields = ['title']
