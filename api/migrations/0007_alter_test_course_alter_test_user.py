# Generated by Django 4.1.6 on 2023-07-01 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_test_course_test_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course', to='api.course'),
        ),
        migrations.AlterField(
            model_name='test',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test', to=settings.AUTH_USER_MODEL),
        ),
    ]
