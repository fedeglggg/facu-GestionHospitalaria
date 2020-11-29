
# Generated by Django 3.1 on 2020-11-28 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appGestionHospitalaria', '0015_auto_20201126_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiaJornada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='TurnoJornada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario_inicio', models.TimeField()),
                ('horario_fin', models.TimeField(blank=True, null=True)),
                ('dia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appGestionHospitalaria.diajornada')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appGestionHospitalaria.doctor')),
            ],
        ),
    ]
