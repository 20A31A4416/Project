# Generated by Django 4.1.7 on 2023-06-06 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedbackBy', models.CharField(max_length=30)),
                ('feedback', models.TextField()),
                ('isVisible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlanAddon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PlanQuerie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'enquire',
                'verbose_name_plural': 'enquiries',
            },
        ),
        migrations.CreateModel(
            name='PortfolioImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastUpdate', models.DateField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='portfolio/')),
                ('link', models.URLField(blank=True, unique=True)),
                ('pcloudFileId', models.CharField(blank=True, max_length=300)),
                ('pubCode', models.CharField(max_length=1000)),
                ('isHeroBackground', models.BooleanField(default=False)),
                ('isHeroPic', models.BooleanField(default=False)),
                ('isScrollPic', models.BooleanField(default=False)),
                ('isPortfolioDisplay', models.BooleanField(default=True)),
                ('isEmotionalCapture', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('streamLink', models.URLField(unique=True)),
                ('link', models.URLField(unique=True)),
                ('time', models.TimeField()),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnail/')),
                ('pcloudFileId', models.CharField(blank=True, max_length=300)),
                ('pubCode', models.CharField(max_length=1000)),
            ],
        ),
    ]
