# Generated by Django 5.0.2 on 2024-10-14 04:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0010_employee_total_sl_alter_employee_total_cl_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeleave',
            name='leave',
            field=models.CharField(choices=[('CL', 'Casual Leave'), ('EL', 'Earned Leave'), ('SL', 'Sick Leave')], default='CL', max_length=16),
        ),
        migrations.AlterField(
            model_name='employeeleave',
            name='total_days',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='EmployeeExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeTimesheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_date', models.DateField()),
                ('hours_worked', models.DecimalField(decimal_places=2, max_digits=5)),
                ('task_description', models.TextField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.employee')),
            ],
        ),
    ]
