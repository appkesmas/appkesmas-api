# Generated by Django 3.2.3 on 2021-06-02 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20210602_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='image_name',
            field=models.CharField(default='default.img', max_length=200),
        ),
    ]
