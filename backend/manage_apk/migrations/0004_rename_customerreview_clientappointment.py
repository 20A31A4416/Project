# Generated by Django 4.1.7 on 2023-06-06 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_apk', '0003_remove_stream_event_remove_stream_time_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomerReview',
            new_name='ClientAppointment',
        ),
    ]
