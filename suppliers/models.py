from django.db import models
from django.conf import settings
from . import cmethods

# Model to load Excel file from admin
class ProductList(models.Model):
    class Meta:  # name in admin panel
        verbose_name = 'Список товаров'
        verbose_name_plural = "Список товаров"

    product_list_source = models.CharField('Источник',max_length=30, primary_key = True) # Must be Forest
    product_list_file = models.FileField('Список товаров',upload_to = cmethods.UploadToPathAndRename(settings.SUPPLIERS_FOLDER)) # Excel file with product list (custom function to rename and replace)

    def __str__(self):
        return self.pk
# ---------------------------------------------------------------------------------
# Supplier model to fill dict with supplier info from admin
class Supplier(models.Model):
    class Meta:  # name in admin panel
        verbose_name_plural = "Поставщики"
        verbose_name = "Поставщиков"

    types = models.CharField("Тип загрузочного файла",max_length=32, choices=cmethods.filetypes, default = 'XLS')
    supplier_name = models.CharField("Поставщик",max_length=30, primary_key=True)
    offer_column_name = models.CharField("Название товарного блока (для XML)",max_length=30,blank = True)
    sku_colunmn_number = models.CharField("Колонка артикула",max_length=30)
    quantity_colunmn_number = models.CharField("Колонка количества",max_length=30)
    quantity_specific = models.CharField("Специфика колонки количества (прим. больше5=6,>10=6)",max_length=60,blank = True)
    price_type = models.CharField("Тип обновления цены",max_length=32, choices=cmethods.pricetypes, default = 'pure_price')
    price_colunmn_number = models.CharField("Колонка итоговой цены",max_length=30)
    old_price_colunmn_number = models.CharField("Колонка цены до применения скидки",max_length=30,blank = True)
    update_price = models.BooleanField("Обновлять цену?",default = True)
    price_list = models.FileField("Прайс-лист",upload_to = cmethods.UploadToPathAndRename(settings.SUPPLIERS_FOLDER),blank=True) # Excel file with product list (custom function to rename and replace)
    price_list_link = models.CharField("Ссылка на прайс-лист",max_length = 256,blank=True)
    def __str__(self):
        return self.pk
# ---------------------------------------------------------------------------------
# Model to initialize and keep list with all products from site
class ProductTable(models.Model):
    sku = models.CharField("Артикул",max_length=50,primary_key = True)
    name = models.CharField("Название",max_length=60)

    def __str__(self):
        return self.name
# ---------------------------------------------------------------------------------


