# Generated by Django 4.1 on 2022-11-16 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0015_applicant_grad_year_applicant_job_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('staff', 'staff'), ('applicant', 'applicant')], max_length=20),
        ),
    ]