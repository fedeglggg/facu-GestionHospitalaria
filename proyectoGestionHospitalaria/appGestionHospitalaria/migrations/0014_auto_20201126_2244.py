# Generated by Django 3.1 on 2020-11-27 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appGestionHospitalaria', '0013_auto_20201023_0045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='especialidad',
        ),
        migrations.AddField(
            model_name='doctor',
            name='especialidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appGestionHospitalaria.especialidad'),
        ),
    ]