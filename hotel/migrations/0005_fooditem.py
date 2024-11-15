# Generated by Django 5.1.3 on 2024-11-11 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_remove_order_total_price_order_ordered_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('image', models.ImageField(upload_to='menu_images/')),
            ],
        ),
    ]
