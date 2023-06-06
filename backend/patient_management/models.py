from typing import Any, Dict, Iterable, Optional, Tuple
from oneset.models import Category, Location, PayMode, Role

from django.db import models

from django.db.models import F

from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

from django.conf import settings

class Client(models.Model):
    name = models.CharField(max_length=225)
    phone = models.CharField(max_length=10, unique=True)
    pincode = models.CharField(max_length=7, blank=True, null=True, validators=[
        MinLengthValidator(5), MaxLengthValidator(7)])

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_OPTIONS = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other')
    ]
    gender = models.CharField(
        max_length=1, choices=GENDER_OPTIONS, blank=True, null=True)
    
    BLOOD_GROUPS = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )

    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)

    def __str__(self) -> str:
        return self.name


# --------------------------------------appointment-----------------------------------------------------
class Appointment(models.Model):
    reason = models.CharField(max_length=225)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    patient = models.ForeignKey(Client, on_delete=models.PROTECT)
    mutuals = models.ManyToManyField(Client, related_name='mutualAppointments')

    PENDING = 'P'
    FIRSTAID = 'F'
    OBSERVATION = 'O'
    EMERGENCY = 'I'
    DISCHARGED = 'D'
    DEAD = 'E'
    STATUS = [
        (PENDING, 'Pending'),
        (FIRSTAID, 'First Aid'),
        (OBSERVATION, 'Observation'),
        (EMERGENCY, 'Emergency'),
        (EMERGENCY, 'Discharge'),
        (DEAD, 'Dead'),
    ]
    status = models.CharField(
        max_length=1, choices=STATUS, default=PENDING)

    address = models.CharField(max_length=225)
    city = models.ForeignKey(Location, on_delete=models.PROTECT)

    quotation = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.reason


# -----------------------------appointment Work Status--------------------------------------------------
class AppointmentWorkStatus(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.PROTECT)

    DONE = 'D'
    PENDING = 'P'
    NONE = 'N'
    OPTIONS = [
        (DONE, 'Done'),
        (PENDING, 'Pending'),
        (NONE, 'None')
    ]

    temperatureCheckup = models.CharField(max_length=1, choices=OPTIONS, default=NONE)
    weightMeasurement = models.CharField(max_length=1, choices=OPTIONS, default=NONE)
    xray = models.CharField(max_length=1, choices=OPTIONS, default=NONE)
    scanning = models.CharField(
        max_length=1, choices=OPTIONS, default=NONE)
    physiotherapy = models.CharField(
        max_length=1, choices=OPTIONS, default=NONE)
    plateletsCheckup = models.CharField(max_length=1, choices=OPTIONS, default=NONE)
    bpCheckup = models.CharField(max_length=1, choices=OPTIONS, default=NONE)
    dialysis = models.CharField(max_length=1, choices=OPTIONS, default=NONE)
    urinalysis  = models.CharField(max_length=1, choices=OPTIONS, default=NONE)
    operationRequired = models.CharField(max_length=1, choices=OPTIONS, default=NONE)

    def __str__(self) -> str:
        return self.appointment.patient.name + ', ' + self.appointment.patient.phone + ' - ' + ' Work Status'

    class Meta:
        verbose_name = 'appointment Work Status'
        verbose_name_plural = 'appointment Work Status'


# -----------------------------appointment quotation Transaction----------------------------------------
class Transaction(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    paymode = models.ForeignKey(PayMode, on_delete=models.PROTECT)
    value = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.appointment.patient.name + ' - ' + str(self.value) + '₹' + ' - ' + self.paymode.title + ' - ' + str(self.date)

# -----------------------------Staff Account Ledger----------------------------------------


class staffPaymentLedger(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT, related_name='accountLedger')
    date = models.DateField()
    creditValue = models.DecimalField(
        max_digits=9, decimal_places=2, default=0)
    debtValue = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    narration = models.CharField(max_length=700)
    accountBalance = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self) -> str:
        return self.user.username + ' Account Balance - ' + str(self.accountBalance)

    def save(self, *args, **kwargs) -> None:
        if self.id == None:
            lastRecord = staffPaymentLedger.objects.filter(
                user=self.user).last()
            if lastRecord != None:
                accountBalance = lastRecord.accountBalance
            else:
                accountBalance = 0

            self.accountBalance = accountBalance

            if self.creditValue != None:
                self.accountBalance = self.accountBalance + self.creditValue

            if self.debtValue != None:
                self.accountBalance = self.accountBalance - self.debtValue

        else:
            oldData = staffPaymentLedger.objects.get(pk=self.id)

            if self.creditValue != oldData.creditValue:
                creditDifference = self.creditValue - oldData.creditValue
                self.accountBalance = self.accountBalance + creditDifference

                staffPaymentLedger.objects.filter(user=self.user).filter(
                    pk__gt=self.id).update(accountBalance=F('accountBalance') + creditDifference)

            if self.debtValue != oldData.debtValue:
                debtDifference = self.debtValue - oldData.debtValue
                self.accountBalance = self.accountBalance - debtDifference

                staffPaymentLedger.objects.filter(user=self.user).filter(
                    pk__gt=self.id).update(accountBalance=F('accountBalance') - debtDifference)

        return super(staffPaymentLedger, self).save(*args, **kwargs)


# -----------------------------appointment Staff----------------------------------------
class appointmentStaff(models.Model):
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, related_name='staff')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, limit_choices_to={
                             'is_staff__iexact': 1, 'is_active__iexact': 1}, related_name='appointmentPays')
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
