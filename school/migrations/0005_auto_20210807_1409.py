# Generated by Django 3.2.6 on 2021-08-07 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_studentparent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentparent',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentparent_parent', to='school.parent'),
        ),
        migrations.AlterField(
            model_name='studentparent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentparent_student', to='school.student'),
        ),
    ]
