from typing import Any, Optional
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

from utility.pcloud import deleteFolder
from core.views import getAuth

from django.db.models import Count, When, F, Q, Case, Sum


# -------------------------------Client Admin--------------------------------------------------------------------------------------------
@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    icon_name = 'person_pin'
    list_display = ['name', 'phone', 'gender',
                    'pincode', 'appointments', 'mutual_appointments']
    list_per_page = 10
    list_filter = ['gender']
    ordering = ['name']
    search_fields = ['name__icontains', 'phone__icontains', 'pincode']
    actions_selection_counter = False

    fieldsets = [
        (None, {
            'fields': [('name', 'phone')]
        }),
        ('Other Options', {
            'fields': [('gender', 'pincode')],
            'description': 'these fields are optional, But Better to fill!'
        })]

    @admin.display(ordering='appointments')
    def appointments(self, client: models.Client):
        url = reverse('admin:patient_management_appointment_changelist') + '?' + \
            urlencode({'client__id': client.id})
        return format_html(f'<a href="{url}">{client.appointments}</a>')

    @admin.display(ordering='appointments')
    def mutual_appointments(self, client: models.Client):
        url = reverse('admin:patient_management_appointment_changelist') + '?' + \
            urlencode({'mutuals__id': client.id})
        return format_html(f'<a href="{url}">{client.mutual_appointments}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(appointments=Count('appointment', distinct=True)).annotate(mutual_appointments=Count('mutualAppointments', distinct=True))


# -------------------------------appointment Admin----------------------------------------------------------------------------------------------
class WorkStatusInline(admin.TabularInline):
    model = models.AppointmentWorkStatus
    min_num = 1
    max_num = 1
    extra = 0

    def has_delete_permission(self, request, obj):
        return False


class appointmentStaffInline(admin.StackedInline):
    model = models.appointmentStaff
    min_num = 1
    max_num = 1000
    extra = 1


class TransactionInline(admin.StackedInline):
    model = models.Transaction
    min_num = 0
    max_num = 1000
    extra = 1


@admin.register(models.Appointment)
class appointmentAdmin(admin.ModelAdmin):
    icon_name = 'airline_seat_flat_angled'
    list_display = ['Patient', 'reason', 'date',
                    'category', 'city', 'status', 'payment', 'staff', 'work_status']
    list_per_page = 10
    autocomplete_fields = ['patient', 'mutuals']
    ordering = ['-date']
    search_fields = ['reason__icontains',
                     'patient__name__icontains', 'patient__phone__icontains']
    list_filter = ['category', 'city', 'status']
    date_hierarchy = 'date'
    list_select_related = ['patient']
    inlines = [WorkStatusInline, appointmentStaffInline, TransactionInline]

    fieldsets = [
        (None, {
            'fields': ['status', ('reason', 'date', 'quotation'), ('patient', 'category', 'city')]
        }),
        ('Details', {
            'fields': [('address')],
            'description': 'this data is used in the APK, make sure to give properly!'
        }),
        ('Mutual Connections', {
            'fields': [('mutuals')],
        })]

    @admin.display(ordering='payment')
    def payment(self, appointment):
        if appointment.payment == None:
            return '0%'
        url = reverse('admin:patient_management_transaction_changelist') + \
            '?' + urlencode({'appointment__id': appointment.id})
        return format_html(f'<a href="{url}">{str(appointment.payment)}%</a>')

    @admin.display(ordering='staffCount')
    def staff(self, appointment):
        url = reverse('admin:patient_management_appointmentstaff_changelist') + \
            '?' + urlencode({'appointment__id': appointment.id})
        return format_html(f'<a href="{url}">{str(appointment.staffCount)}</a>')

    def work_status(self, appointment):
        url = reverse('admin:patient_management_appointmentworkstatus_changelist') + \
            '?' + urlencode({'appointment__id': appointment.id})
        return format_html(f'<a style="color:#000000;" href="{url}"><i class="material-icons large-icon">lassignment_turned_in keyboard_arrow_right</i></a>')

    @admin.display(ordering='patient__name')
    def Patient(self, appointment: models.Appointment):
        return appointment.patient.name + ' - ' + appointment.patient.phone

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(payment=(Sum('transaction__value', distinct=True)/F('quotation'))*100).annotate(staffCount=Count('staff', distinct=True))


# ---------------------appointment WorkStatus------------------------------------------------------------------------------------------------
@ admin.register(models.AppointmentWorkStatus)
class appointmentWorkStatusAdmin(admin.ModelAdmin):
    icon_name = 'assignment_turned_in'
    list_display = ['appointment', 'Phsthpy', 'temp', 'Weight',
                    'Xray', 'Scanning', 'Platelet', 'bp', 'urin_Chk', 'oper_Req', 'Dialysis']
    list_per_page = 10
    list_select_related = ['appointment']

    fieldsets = [
        (None, {
            'fields': ['appointment']
        }),
        ('Works', {
            'fields': [('temperatureCheckup', 'weightMeasurement', 'xray', 'scanning'), ('physiotherapy', 'plateletsCheckup', 'bpCheckup'), ('dialysis', 'urinalysis', 'operationRequired')],
            'description': 'NOTE: Please Keep None if the service is not providing to this appointment. '
        })]

    # *****************************************************
    # @admin.display(ordering='appointment')
    def appointment(self, appointmentWorkStatus: models.AppointmentWorkStatus):
        return appointmentWorkStatus.appointment.reason + ' - ' + str(appointmentWorkStatus.appointment.client.phone)

    def temp(self, appointmentWorkStatus: models.AppointmentWorkStatus):
        if appointmentWorkStatus.temperatureCheckup == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif appointmentWorkStatus.temperatureCheckup == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def Phsthpy(self, appointmentWorkStatus: models.AppointmentWorkStatus):
        if appointmentWorkStatus.physiotherapy == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif appointmentWorkStatus.physiotherapy == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def Weight(self, appointmentWorkStatus: models.AppointmentWorkStatus):
        if appointmentWorkStatus.weightMeasurement == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif appointmentWorkStatus.weightMeasurement == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def Xray(self, appointmentWorkStatus: models.AppointmentWorkStatus):
        if appointmentWorkStatus.xray == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif appointmentWorkStatus.xray == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def Scanning(self, appointmentWorkStatus: models.AppointmentWorkStatus):
        if appointmentWorkStatus.scanning == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif appointmentWorkStatus.scanning == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def Platelet(self, appointmentWorkStatus: models.AppointmentWorkStatus):
        if appointmentWorkStatus.plateletsCheckup == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif appointmentWorkStatus.plateletsCheckup == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def bp(self, appointmentWorkStatus: models.AppointmentWorkStatus):
        if appointmentWorkStatus.bpCheckup == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif appointmentWorkStatus.bpCheckup == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def oper_Req(self, appointmentWorkStatus: models.AppointmentWorkStatus):
        if appointmentWorkStatus.operationRequired == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif appointmentWorkStatus.operationRequired == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def urin_Chk(self, appointmentWorkStatus: models.AppointmentWorkStatus):
        if appointmentWorkStatus.urinalysis == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif appointmentWorkStatus.urinalysis == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def Dialysis(self, appointmentWorkStatus: models.AppointmentWorkStatus):
        if appointmentWorkStatus.dialysis == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif appointmentWorkStatus.dialysis == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')
    # -------------------------------------------------------------


    def get_queryset(self, request):
        query = super().get_queryset(request).select_related(
            'appointment').exclude(appointment__status='C')
        return query.annotate(payment=(Sum('appointment__transaction__value', distinct=True)/F('appointment__quotation'))*100).order_by('appointment__date')


# ---------------------Quotation Transaction---------------------------------------------------------------------------------------------
@ admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    icon_name = 'attach_money'
    list_display = ['appointment', 'date', 'paymode', 'value']
    list_per_page = 10
    ordering = ['-date']
    search_fields = ['appointment__icontains', 'client__icontains']
    date_hierarchy = 'date'
    list_filter = ['paymode']
    autocomplete_fields = ['appointment', 'paymode']

    fieldsets = [
        (None, {
            'fields': [('appointment', 'paymode', 'value')]
        })]


# ---------------------appointment Staff-----------------------------------------------------------------------------------------------------
@ admin.register(models.appointmentStaff)
class appointmentStaffAdmin(admin.ModelAdmin):
    icon_name = 'all_inclusive'
    list_display = ['appointment', 'user', 'role']
    list_per_page = 10


# ---------------------Staff account Ledger-----------------------------------------------------------------------------------------------------
@ admin.register(models.staffPaymentLedger)
class StaffPaymentLedgerAdmin(admin.ModelAdmin):
    icon_name = 'chrome_reader_mode'
    list_display = ['user', 'date', 'narration',
                    'creditValue', 'debtValue', 'accountBalance']
    list_per_page = 10

    fieldsets = [
        (None, {
            'fields': [('user'), ('date', 'creditValue', 'debtValue'), 'narration']
        })]

    def has_delete_permission(self, *args) -> bool:
        return False
