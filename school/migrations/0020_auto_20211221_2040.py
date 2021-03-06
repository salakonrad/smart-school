# Generated by Django 3.2.6 on 2021-12-21 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0019_auto_20210831_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='is_final',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='event',
            field=models.CharField(choices=[('OB', 'Obecność'), ('SP', 'Spóźnienie'), ('NB', 'Nieobecność'), ('NU', 'Nieobecność usprawiedliwiona')], max_length=2),
        ),
        migrations.AlterField(
            model_name='squad',
            name='year_end',
            field=models.IntegerField(default=2025),
        ),
    ]
