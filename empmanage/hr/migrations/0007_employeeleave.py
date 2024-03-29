# Generated by Django 4.2.6 on 2023-11-03 06:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0006_alter_employeeattendance_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave', models.CharField(blank=True, choices=[('CL', 'Casual Leave'), ('EL', 'Earned Leave')], default='CL', max_length=16)),
                ('leave_reason', models.TextField(blank=True, null=True)),
                ('leave_from', models.DateTimeField(blank=True, null=True)),
                ('leave_to', models.DateTimeField(blank=True, null=True)),
                ('total_days', models.PositiveIntegerField(blank=True, null=True)),
                ('total_cl', models.PositiveIntegerField(default=13, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(13)])),
                ('total_el', models.IntegerField(default=13, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(13)])),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.employee')),
            ],
        ),
    ]
