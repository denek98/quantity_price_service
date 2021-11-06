# Generated by Django 3.2.8 on 2021-11-04 13:51

from django.db import migrations, models
import suppliers.cmethods


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='price_list_link',
            field=models.CharField(blank=True, max_length=256, verbose_name='Ссылка на прайс-лист'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='price_list',
            field=models.FileField(blank=True, upload_to=suppliers.cmethods.UploadToPathAndRename('uploads'), verbose_name='Прайс-лист'),
        ),
    ]
