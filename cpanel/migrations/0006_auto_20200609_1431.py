# Generated by Django 2.2.13 on 2020-06-09 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpanel', '0005_auto_20200609_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='physicianrating',
            name='rate',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1),
        ),
    ]