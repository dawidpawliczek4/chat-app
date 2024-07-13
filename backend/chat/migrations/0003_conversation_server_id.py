# Generated by Django 5.0.6 on 2024-07-06 14:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_rename_conversation_message_conversation'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='server_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]