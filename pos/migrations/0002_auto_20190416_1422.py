# Generated by Django 2.1.7 on 2019-04-16 19:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('depositID', models.AutoField(primary_key=True, serialize=False)),
                ('depositDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('depositAmount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('camperID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.Customer')),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transactionDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]