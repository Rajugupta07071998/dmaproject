# Generated by Django 4.2.18 on 2025-02-11 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_businessinfo_business_logo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessinfo',
            name='business_logo',
            field=models.ImageField(blank=True, null=True, upload_to='business_logos/'),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
