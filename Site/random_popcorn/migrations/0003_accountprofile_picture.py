# Generated by Django 3.0 on 2020-01-02 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('random_popcorn', '0002_remove_accountprofile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountprofile',
            name='picture',
            field=models.ImageField(blank=True, upload_to='account_image'),
        ),
    ]
