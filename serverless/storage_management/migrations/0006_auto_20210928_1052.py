# Generated by Django 3.2.7 on 2021-09-28 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage_management', '0005_auto_20210928_0713'),
    ]

    operations = [
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(blank=True, max_length=128, null=True)),
                ('user_id', models.CharField(default='', max_length=128, unique=True)),
                ('coinbase', models.TextField(blank=True, default='No content here', help_text="User's coinbase", null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='item',
            name='author',
        ),
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='item',
            name='series',
        ),
        migrations.RemoveField(
            model_name='item',
            name='unit',
        ),
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('installed', 'Installed'), ('delivered', 'Delivered'), ('out', 'Out')], default='pending', help_text='Current storage status', max_length=128),
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Series',
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