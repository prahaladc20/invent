# Generated by Django 2.2.7 on 2019-12-02 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_remove_inventory_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryapproval',
            name='status',
            field=models.CharField(max_length=20),
        ),
    ]
