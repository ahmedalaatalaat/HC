# Generated by Django 2.2.13 on 2020-06-09 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpanel', '0007_auto_20200609_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientinsurance',
            name='insurance_type',
            field=models.ForeignKey(db_column='Insurance_Type', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='cpanel.InsuranceTypes'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='patientinsurance',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='patientinsurance',
            name='insurance_type_id',
        ),
    ]
