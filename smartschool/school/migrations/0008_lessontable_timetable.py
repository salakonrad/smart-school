# Generated by Django 3.2.6 on 2021-08-10 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonTable',
            fields=[
                ('lesson_table', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.IntegerField()),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
            ],
            options={
                'db_table': 'lesson_time_table',
            },
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('time_table', models.AutoField(primary_key=True, serialize=False)),
                ('day', models.CharField(choices=[('M', 'Poniedziałek'), ('T', 'Wtorek'), ('W', 'Środa'), ('C', 'Czwartek'), ('F', 'Piątek'), ('S', 'Sobota')], max_length=1)),
                ('lesson_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable_lesson_number', to='school.lessontable')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable_subject', to='school.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable_teacher', to='school.teacher')),
            ],
            options={
                'db_table': 'time_table',
            },
        ),
    ]
