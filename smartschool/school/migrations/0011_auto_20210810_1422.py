# Generated by Django 3.2.6 on 2021-08-10 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0010_auto_20210810_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='SquadSubject',
            fields=[
                ('squad_subject', models.AutoField(primary_key=True, serialize=False)),
                ('squad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='squadsubject_class', to='school.squad')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='squadsubject_subject', to='school.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='squadsubject_teacher', to='school.teacher')),
            ],
            options={
                'db_table': 'squad_subject',
            },
        ),
        migrations.AlterField(
            model_name='timetable',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable_subject', to='school.squadsubject'),
        ),
        migrations.DeleteModel(
            name='SquadSubjects',
        ),
    ]
