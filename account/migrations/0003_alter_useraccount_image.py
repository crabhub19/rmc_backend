# Generated by Django 5.1.5 on 2025-01-28 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_useraccount_contract_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_image'),
        ),
    ]
