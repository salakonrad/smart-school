# Generated by Django 3.2.6 on 2021-08-15 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0014_remove_grade_squad'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grade',
            old_name='date',
            new_name='issue_date',
        ),
        migrations.AddField(
            model_name='grade',
            name='edit_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='grade',
            name='edited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grade_edited_by', to='school.teacher'),
        ),
        migrations.AddField(
            model_name='grade',
            name='issued_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='grade_issued_by', to='school.teacher'),
            preserve_default=False,
        ),
    ]
