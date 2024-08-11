# Generated by Django 3.2.5 on 2023-08-29 23:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('states', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate', models.CharField(max_length=6, null=True)),
                ('brand', models.CharField(max_length=30, null=True)),
                ('line', models.CharField(max_length=30, null=True)),
                ('model', models.IntegerField()),
                ('photo', models.ImageField(null=True, upload_to='vehiculos/', verbose_name='foto')),
                ('technomechanical', models.FileField(default='', null=True, upload_to='technomechanical/')),
                ('technomechanical_date', models.DateField(null=True)),
                ('soat', models.FileField(default='', null=True, upload_to='soat/')),
                ('soat_date', models.DateField(null=True)),
                # ('is_active', models.BooleanField(default=False)),
                # ('use_condition', models.CharField(default='Libre', max_length=100)),
                ('editing_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='editing_user', to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='states.state')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.extended_user')),
            ],
        ),
    ]