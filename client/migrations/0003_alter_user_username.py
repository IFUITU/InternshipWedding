# Generated by Django 4.1 on 2022-08-17 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
