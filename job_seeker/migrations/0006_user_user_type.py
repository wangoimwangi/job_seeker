# Generated by Django 4.1 on 2022-09-23 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0005_appliedjobs_profile_savedjobs_skill_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('staff', 'staff'), ('staff', 'applicant')], default=0, max_length=20),
            preserve_default=False,
        ),
    ]
