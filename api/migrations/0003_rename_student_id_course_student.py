# Generated by Django 4.1.6 on 2023-07-01 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_course_question_quiz_source_student_video_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='student_id',
            new_name='student',
        ),
    ]
