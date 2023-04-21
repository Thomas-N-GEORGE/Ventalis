# Generated by Django 4.2 on 2023-04-20 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventashop', '0003_conversation_customeraccount_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conversation',
            options={},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['date_created']},
        ),
        migrations.AddField(
            model_name='order',
            name='incl_vat_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='vat_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]