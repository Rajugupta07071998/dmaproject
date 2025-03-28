# Generated by Django 4.2.18 on 2025-03-28 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_chatroom_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='duration',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='extension',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
