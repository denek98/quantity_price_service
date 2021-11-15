from django.shortcuts import render,redirect
from . import models,cmethods
from django.conf import settings
import pandas as pd
from datetime import datetime



# Function to take info from model with Excel file and transfer it to another model with product list info
def initialize(request):
    engine = cmethods.init_db_connection()
    product_link_path = models.ProductList.objects.get().product_list_file.path # Get path for Excel file
    df = pd.read_excel(product_link_path,names = ['sku','name'],header = None) # provide Excel file with sku on the first position and name on the second
    df['quantity'] = 0 # setting default values
    df['price'] = 0 # setting default values
    df['price_old'] = 0 # setting default values
    df.to_sql(models.ProductTable._meta.db_table,con = engine,if_exists = 'replace',index = False)
    return redirect('index')
# --------------------------------------------------------------------------------------------------
def index(request):
      return render(request, 'suppliers/suppliers.html')
# --------------------------------------------------------------------------------------------------
def generate_price_list(request):
    report_name = (f'ostatki_to_upload-{datetime.today().strftime("%m-%d")}.xls')
    filepath = f'{settings.REPORTS_FOLDER}/generate_price_list.xls'
    engine = cmethods.init_db_connection()
    current_df_product = cmethods.get_current_df_product(models.ProductTable._meta.db_table) # get current products from ProductTable model
    dframe = cmethods.process_files_to_dataframe(models.Supplier.objects.values(),current_df_product) # get dataframe with all supliers 
    resulted_df_product = cmethods.update_product_table_model_from_dframe(dframe,current_df_product) # get resulted dataframe based on previous and new info
    resulted_df_product.to_sql(models.ProductTable._meta.db_table,con = engine,if_exists = 'replace',index = False,dtype = cmethods.datatypes)
    resulted_df_product.to_excel(filepath,index = False)
    return cmethods.donwload_report(filepath,report_name)
# --------------------------------------------------------------------------------------------------
def generate_suppliers_file(request):
    report_name = (f'ostatki-{datetime.today().strftime("%m-%d")}.xls')
    filepath = f'{settings.REPORTS_FOLDER}/generate_suppliers_file.xls'
    engine = cmethods.init_db_connection()
    current_df_product = cmethods.get_current_df_product(models.ProductTable._meta.db_table) # get current products from ProductTable model
    dframe = cmethods.process_files_to_pricelist(models.Supplier.objects.values(),current_df_product) # get dataframe with all supliers 
    resulted_df_product = cmethods.update_suppliers_pricelist_model_from_dframe(dframe,current_df_product)
    resulted_df_product.to_sql('suppliers_price_list',con = engine,if_exists = 'replace',index = False)
    resulted_df_product.to_excel(filepath,index = False)
    return cmethods.donwload_report(filepath,report_name)


# Create your views here.

