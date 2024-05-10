# Generated by Django 5.0.4 on 2024-05-10 13:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_product_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_items',
            field=models.ManyToManyField(related_name='orders', to='home.orderitem'),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_amount', models.IntegerField()),
                ('transaction_gateway', models.CharField(max_length=100)),
                ('related_order', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='home.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_record',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='home.transaction'),
            preserve_default=False,
        ),
    ]
