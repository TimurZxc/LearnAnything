# Generated by Django 4.1.6 on 2023-07-02 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_body_question_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]