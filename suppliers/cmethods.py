import os
from django.http.response import HttpResponse
import pandas as pd
import parmap
import numpy as np
from django.conf import settings
import sqlalchemy
from os.path import exists
from django.utils.deconstruct import deconstructible
from sqlalchemy.types import SmallInteger
from functools import reduce
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
pd.options.mode.chained_assignment = None


datatypes = {
    'price':SmallInteger,
    'quantity':SmallInteger
    }

filetypes = [
        ('XML', u'XML'),
        ('XLS', u'Excel')
    ]

# Initialize DB connection
def init_db_connection():
    database_name = settings.DATABASES['default']['NAME']
    database_url = f'sqlite:///{database_name}'
    engine = sqlalchemy.create_engine(database_url)
    return engine
# ---------------------------------------------------------------------------------
# Get current products price-list from sql
def get_current_df_product(table):
    engine = init_db_connection()
    current_df_product = pd.read_sql_table(table,con = engine) # get current table
    current_df_product['quantity'] = 0
    return current_df_product
# ---------------------------------------------------------------------------------
def update_product_table_model_from_dframe(dframe,current_df_product):
    dframe['quantity'] = pd.to_numeric(dframe['quantity'], errors='coerce')
    dframe['price'] = pd.to_numeric(dframe['price'], errors='coerce')
    dframe = dframe.groupby('sku',as_index = False).agg({'quantity':'sum','price':'min'})
    current_df_product = pd.concat([current_df_product,dframe[['sku','quantity','price']]]).groupby('sku',as_index = False).agg({'quantity':'sum','price':get_not_nan_values,'name':get_not_nan_values})
    return current_df_product[['sku','name','quantity','price']]
# ---------------------------------------------------------------------------------    
def update_suppliers_pricelist_model_from_dframe(dframe,current_df_product):
    current_df_product = current_df_product[['sku','name']]
    name_col = dframe.merge(current_df_product, how = 'left')['name']
    dframe.insert(1, 'name', name_col)
    return dframe
# ---------------------------------------------------------------------------------  
# From multiple excel files to dataframe
def process_files_to_dataframe(suppliers,current_df_product):
    df_list = parmap.map(parallel_process_files_to_dataframe,suppliers,current_df_product) # read multiple excel files in parallel
    dframe = pd.concat(df_list,ignore_index = True) 
    return dframe
# ---------------------------------------------------------------------------------
# From multiple excel files to dataframe
def process_files_to_pricelist(suppliers,current_df_product):
    df_list = parmap.map(parallel_process_files_to_pricelist,suppliers,current_df_product) # read multiple excel files in parallel
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['sku'],how='outer'), df_list)
    return df_merged
# ---------------------------------------------------------------------------------
# Generate dataframe with only columns specified from admin 
def parallel_process_files_to_dataframe(supplier_dict,current_df_product):
    if supplier_dict['types'] == 'XLS':
       df = process_excel_file(supplier_dict,current_df_product)
       return df
    elif supplier_dict['types'] == 'XML':
        df = process_xml_file(supplier_dict,current_df_product)
        return df
# ---------------------------------------------------------------------------------   
# Generate dataframe with only columns specified from admin 
def parallel_process_files_to_pricelist(supplier_dict,current_df_product):
    if supplier_dict['types'] == 'XLS':
       df = process_excel_file_to_pricelist(supplier_dict,current_df_product)
       return df
    elif supplier_dict['types'] == 'XML':
        df = process_xml_file_to_pricelist(supplier_dict,current_df_product)
        return df
# ---------------------------------------------------------------------------------   
def get_not_nan_values(dframe_col):
    if pd.isna(dframe_col.iloc[-1]): # check if new pricelist contains missing prices
        return dframe_col.iloc[0] # return old prices
    return dframe_col.iloc[-1] # return new prices if not nan
# ---------------------------------------------------------------------------------   
# ---------------------------------------------------------------------------------   
def parse_and_apply_column_specific(dframe,supplier_dict):
    if supplier_dict['quantity_specific'] == '':
        return dframe
    else:
        diction = {}
        specific_list = supplier_dict['quantity_specific'].split(',')
        for specific in specific_list:
            formula = specific.split('=')
            diction[formula[0]] = formula[1]
        dframe['quantity'] = dframe['quantity'].replace(diction)
        return dframe
# ---------------------------------------------------------------------------------   
def process_excel_file(supplier_dict,current_df_product):
    if supplier_dict['update_price']:
        supplier_filepath = supplier_dict['price_list']
        sku_column = int(supplier_dict['sku_colunmn_number'])-1
        price_column = int(supplier_dict['price_colunmn_number'])-1
        quantity_colunmn = int(supplier_dict['quantity_colunmn_number'])-1
        df = pd.read_excel(supplier_filepath,header = None)
        df = df[[sku_column,quantity_colunmn,price_column]]
        df.columns = ['sku','quantity','price']
        df = df[df['sku'].isin(current_df_product['sku'])]
        df['price'] = df['price'].replace(0,np.nan)
        df = parse_and_apply_column_specific(df,supplier_dict)
        return df
    else:
        supplier_filepath = supplier_dict['price_list']
        sku_column = int(supplier_dict['sku_colunmn_number'])-1
        quantity_colunmn = int(supplier_dict['quantity_colunmn_number'])-1
        df = pd.read_excel(supplier_filepath,header = None)
        df = df[[sku_column,quantity_colunmn]]
        df.columns = ['sku','quantity']
        df = df[df['sku'].isin(current_df_product['sku'])]
        df['price'] = np.nan
        df = parse_and_apply_column_specific(df,supplier_dict)
        return df
# ---------------------------------------------------------------------------------   
def process_xml_file(supplier_dict,current_df_product):
    if supplier_dict['update_price']:
        supplier_filepath = supplier_dict['price_list_link']
        offer_column = supplier_dict['offer_column_name']
        sku_column = supplier_dict['sku_colunmn_number']
        price_column = supplier_dict['price_colunmn_number']
        quantity_colunmn = supplier_dict['quantity_colunmn_number']
        df = pd.read_xml(supplier_filepath,parser = 'etree',xpath=f".//{offer_column}")
        df = df[[sku_column,quantity_colunmn,price_column]]
        df.columns = ['sku','quantity','price']
        df = df[df['sku'].isin(current_df_product['sku'])]
        df['price'] = df['price'].replace(0,np.nan)
        df = parse_and_apply_column_specific(df,supplier_dict) 
        return df
    else:
        supplier_filepath = supplier_dict['price_list_link']
        sku_column = supplier_dict['sku_colunmn_number']
        quantity_colunmn = supplier_dict['quantity_colunmn_number']
        df = pd.read_xml(supplier_filepath,parser = 'etree',xpath=f".//{offer_column}")
        df = df[[sku_column,quantity_colunmn]]
        df.columns = ['sku','quantity']
        df = df[df['sku'].isin(current_df_product['sku'])]
        df['price'] = np.nan
        df = parse_and_apply_column_specific(df,supplier_dict) 
        return df
# ---------------------------------------------------------------------------------   
def process_excel_file_to_pricelist(supplier_dict,current_df_product):
    supplier_filepath = supplier_dict['price_list']
    sku_column = int(supplier_dict['sku_colunmn_number'])-1
    price_column = int(supplier_dict['price_colunmn_number'])-1
    quantity_colunmn = int(supplier_dict['quantity_colunmn_number'])-1
    quantity = f'{supplier_dict["supplier_name"]}_quantity' 
    price = f'{supplier_dict["supplier_name"]}_price'
    df = pd.read_excel(supplier_filepath,header = None)
    df = df[[sku_column,quantity_colunmn,price_column]]
    df.columns = ['sku',quantity,price]
    df = df[df['sku'].isin(current_df_product['sku'])]
    df[quantity] = df[quantity].replace({0:np.nan,'':np.nan,'0':np.nan})
    df[price] = df[price].replace({0:np.nan,'':np.nan,'0':np.nan})
    df.dropna(inplace = True)
    return df

# ---------------------------------------------------------------------------------   
def process_xml_file_to_pricelist(supplier_dict,current_df_product):
    supplier_filepath = supplier_dict['price_list_link']
    offer_column = supplier_dict['offer_column_name']
    sku_column = supplier_dict['sku_colunmn_number']
    price_column = supplier_dict['price_colunmn_number']
    quantity_colunmn = supplier_dict['quantity_colunmn_number']
    quantity = f'{supplier_dict["supplier_name"]}_quantity' 
    price = f'{supplier_dict["supplier_name"]}_price'
    df = pd.read_xml(supplier_filepath,parser = 'etree',xpath=f".//{offer_column}")
    df = df[[sku_column,quantity_colunmn,price_column]]
    df.columns = ['sku',quantity,price]
    df = df[df['sku'].isin(current_df_product['sku'])]
    df[quantity] = df[quantity].replace({0:np.nan,'':np.nan,'0':np.nan})
    df[price] = df[price].replace({0:np.nan,'':np.nan,'0':np.nan})
    df.dropna(inplace = True)
    return df
# ---------------------------------------------------------------------------------   
def donwload_report(filepath,filename):
    path_to_file = os.path.realpath(filepath)
    with open(path_to_file, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

# Class to rename and replace if exists excel file downloaded from admin panel
@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path):
        self.sub_path = path
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(instance.pk, ext)
        if exists(os.path.join(self.sub_path, filename)):
            os.remove(os.path.join(self.sub_path, filename))
        return os.path.join(self.sub_path, filename)
# ---------------------------------------------------------------------------------