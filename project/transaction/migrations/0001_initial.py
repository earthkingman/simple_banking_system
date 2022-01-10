# Generated by Django 4.0 on 2022-01-10 04:18

from django.db import migrations, models
import django.db.models.deletion
import transaction.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.PositiveBigIntegerField(validators=[transaction.validators.validate_balance])),
                ('amount', models.PositiveBigIntegerField(validators=[transaction.validators.validate_amount])),
                ('transaction_type', models.CharField(max_length=2, validators=[transaction.validators.validate_t_type])),
                ('description', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
            ],
            options={
                'db_table': 'transaction_history',
            },
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['account_id', 'transaction_type'], name='transaction_account_b0155b_idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['account_id', 'created_at'], name='transaction_account_ebbee2_idx'),
        ),
    ]
