# Generated by Django 3.0.1 on 2019-12-25 03:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('storage_management', '0014_auto_20190921_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailposition',
            name='uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True),
        ),
    ]
