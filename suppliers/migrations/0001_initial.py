# Generated by Django 3.2.8 on 2021-11-04 13:50

from django.db import migrations, models
import suppliers.cmethods


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductList',
            fields=[
                ('product_list_source', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='Источник')),
                ('product_list_file', models.FileField(upload_to=suppliers.cmethods.UploadToPathAndRename('uploads'), verbose_name='Список товаров')),
            ],
            options={
                'verbose_name': 'Список товаров',
                'verbose_name_plural': 'Список товаров',
            },
        ),
        migrations.CreateModel(
            name='ProductTable',
            fields=[
                ('sku', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Артикул')),
                ('name', models.CharField(max_length=60, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('types', models.CharField(blank=True, choices=[('XML', 'XML'), ('XLS', 'Excel')], max_length=32, verbose_name='Тип загрузочного файла')),
                ('supplier_name', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='Поставщик')),
                ('offer_column_name', models.CharField(max_length=30, verbose_name='Название товарного блока (для XML)')),
                ('sku_colunmn_number', models.PositiveSmallIntegerField(verbose_name='Колонка артикула')),
                ('quantity_colunmn_number', models.PositiveSmallIntegerField(verbose_name='Колонка количества')),
                ('price_colunmn_number', models.PositiveSmallIntegerField(verbose_name='Колонка цены')),
                ('update_price', models.BooleanField(default=True, verbose_name='Обновлять цену?')),
                ('price_list', models.CharField(blank=True, max_length=256, verbose_name='Ссылка на прайс-лист')),
            ],
            options={
                'verbose_name': 'Поставщиков',
                'verbose_name_plural': 'Поставщики',
            },
        ),
    ]
