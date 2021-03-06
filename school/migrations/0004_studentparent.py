# Generated by Django 3.2.6 on 2021-08-06 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_squad_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentParent',
            fields=[
                ('student_parent', models.AutoField(primary_key=True, serialize=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='studentparent_parent', to='school.parent')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='studentparent_student', to='school.student')),
            ],
            options={
                'db_table': 'student_parent',
            },
        ),
    ]
