# Generated by Django 4.0 on 2021-12-16 15:49

from django.db import migrations, models
import django.db.models.deletion
import storage_management.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DetailPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(default='Book Shelf 1', max_length=1024)),
                ('description', models.TextField(blank=True, null=True)),
                ('uuid', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', help_text='Please Enter your item name', max_length=1024, verbose_name='Item Name')),
                ('description', models.TextField(blank=True, help_text='Please enter your item description', null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('price', models.FloatField(default=0.0)),
                ('qr_code', models.CharField(blank=True, max_length=10008, null=True, unique=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('installed', 'Installed'), ('delivered', 'Delivered'), ('out', 'Out'), ('error', 'Error')], default='pending', help_text='Current storage status', max_length=128)),
                ('column', models.IntegerField(default=1)),
                ('row', models.IntegerField(default=1)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('detail_position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='storage_management.detailposition')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(default='China', max_length=128)),
                ('city', models.CharField(default='Shenzhen', max_length=128)),
                ('street', models.CharField(blank=True, default='Some Street', max_length=128, null=True)),
                ('building', models.CharField(blank=True, default='Some Building', max_length=128, null=True)),
                ('unit', models.CharField(blank=True, default='Some Unit', max_length=128, null=True)),
                ('room_number', models.CharField(default='Some RM Number', max_length=128)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MachineType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Raspberry Pi', max_length=128, unique=True)),
                ('hashRate', models.FloatField(default=0, help_text="Machine's base hash rate")),
                ('disk_storage', models.FloatField(default=0, help_text='Storage in MB.')),
                ('memory_size', models.FloatField(default=0, help_text='Size in MB')),
                ('os_version', models.CharField(default='Ubuntu 20.04', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('user_name', models.CharField(blank=True, max_length=128, null=True)),
                ('user_id', models.CharField(default='', max_length=128, unique=True)),
                ('coinbase', models.TextField(blank=True, default='No content here', help_text="User's coinbase", null=True)),
                ('uuid', models.UUIDField(default=uuid.UUID('ab1e6e42-ddd5-48ae-82d3-42943e251c96'), primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='Face', max_length=128, null=True)),
                ('image', models.ImageField(upload_to=storage_management.models.upload_location, verbose_name='Item Image')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='storage_management.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='storage_management.location'),
        ),
        migrations.AddField(
            model_name='item',
            name='machine_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='storage_management.machinetype'),
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='storage_management.owner'),
        ),
    ]
