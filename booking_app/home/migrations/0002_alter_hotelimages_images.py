# Generated by Django 4.2.1 on 2023-06-14 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelimages',
            name='images',
            field=models.ImageField(upload_to='hotels_img'),
        ),
    ]
