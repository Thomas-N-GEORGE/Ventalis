# Generated by Django 4.2 on 2023-04-13 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventashop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_img/%Y/%m/%d/'),
        ),
    ]
