# Generated by Django 2.2.7 on 2019-12-02 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_inventoryapproval_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryapproval',
            name='master_id',
            field=models.IntegerField(null=True),
        ),
    ]
