# Generated by Django 2.2.7 on 2020-06-07 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpanel', '0003_auto_20200525_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurancecompanies',
            name='image',
            field=models.ImageField(default='ic.png', upload_to='IC/images'),
        ),
    ]