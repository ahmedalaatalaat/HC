# Generated by Django 2.2.13 on 2020-06-09 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpanel', '0008_auto_20200609_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientinsurance',
            name='insurance_type',
            field=models.ForeignKey(db_column='Insurance_Type', on_delete=django.db.models.deletion.CASCADE, to='cpanel.InsuranceTypes'),
        ),
    ]