# Generated by Django 4.1.7 on 2023-06-06 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('oneset', '0001_initial'),
        ('patient_management', '0001_initial'),
        ('manage_apk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_management.appointment'),
        ),
        migrations.AddField(
            model_name='portfolioimage',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oneset.category'),
        ),
        migrations.AddField(
            model_name='planquerie',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_management.client'),
        ),
        migrations.AddField(
            model_name='planquerie',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='manage_apk.plan'),
        ),
        migrations.AddField(
            model_name='planaddon',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addons', to='manage_apk.plan'),
        ),
    ]
