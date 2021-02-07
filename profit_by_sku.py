#!/usr/bin/env python
# coding: utf-8
################################################################################################################################################################################################################################################################################################################################################
## Make more wider with all jupyter layout:
#       from IPython.core.display import display, HTML
#       display(HTML("<style>.container { width:100% !important; }</style>"))
################################################################################################################################################################################################################################################################################################################################################
# Purpose: Analyze profits by each SKU
#
# Input: 1 csv files 
#        Data: Optimized Analysis Table, monthly csv file
#        Note1: Here We use 1 csv file for December 2020
# 
# Required Columns: [Sales Sku, Sales Order Number, Sales Order Date, Sales Channel Name, Fulfillment Item Id, Fulfillment Sku, Fulfillment Order Number, Fulfillment Channel Name, Fulfillment Channel Type, Quantity, Sku, Total Sales, Total Cost, Commission, Inventory Cost, Estimated Shipping Cost, Invoice Shipping Cost, Profit, Flag]
#        Note1: Before running this program, check column names in Sales Analysis Table, especially empty spaces.
#
# Output: 1 xlsx file
#        xlsx: Top/Bottom 20 profitable SKUs in a month
# 
# Customized configuration - Only need to change variables below: 
# * data           <- csv file of Optimized Analysis Table
# * pd.ExcelWriter <- Path of excel output file
#
# Optional Comments: If you want to create a text file for output, please refer to the comment (# Write in a text file)
#
################################################################################################################################################################################################################################################################################################################################################
import pandas as pd
import numpy as np

# This is for jupyter output and it can be ignored in py file
#pd.set_option('display.max_columns', 500)
#pd.set_option('display.width', 1000)

# Creating Excel Writer Object from Pandas  
writer = pd.ExcelWriter('output/analysis_result/Profit_Analysis_by_SKU.xlsx',engine='xlsxwriter', mode='w')   
workbook = writer.book

# Read data
data = pd.read_csv('data/optimized_analysis_table_dec.csv') 

# Keep columns: Sku, Profit, Vendors
data = data[['Sku', 'Total Sales', 'Profit', 'Fulfillment Channel Name']]

# Group by sku
agg_data = data.groupby('Sku').agg({'Total Sales': sum, 'Profit':sum, 'Sku':len}).rename(columns={'Sku': 'Orders'})
agg_data['Margin'] = round(agg_data['Profit'] / agg_data['Total Sales'],2)
vendor_col = data.groupby('Sku')['Fulfillment Channel Name'].unique()
agg_data_with_vendors = pd.concat([agg_data, vendor_col], axis=1)

# Sort by total profits
sort_agg_data_with_vendors = agg_data_with_vendors.sort_values(by=['Profit'], ascending=False)

# Monthly Top 20 profits
top20_profit_data = sort_agg_data_with_vendors[:20]

# Monthly Top 20 losses
sort_bottom_agg_data_with_vendors = agg_data_with_vendors.sort_values(by=['Profit'], ascending=True)
bottom20_profit_data = sort_bottom_agg_data_with_vendors[:20]

# Write data in Excel file
v = 'Monthly_Top20_Skus'
worksheet=workbook.add_worksheet(v)
writer.sheets[v] = worksheet
worksheet.write_string(0, 0, 'Monthly Top 20 profitable skus: ')
top20_profit_data.to_excel(writer,sheet_name=v,startrow=1 , startcol=0)   
worksheet.write_string(23, 0, 'Monthly Bottom 20 profitable skus: ')
bottom20_profit_data.to_excel(writer,sheet_name=v,startrow=24, startcol=0)

# Save file of .xlsx
writer.save()

##################################### For Reference #####################################
# Write in a text file
#with open('analysis_result/Profit_Analysis_bySKU.txt', 'w') as f:
#    f.write('Monthly Top 20 profitable skus: \n')
#    f.write(top20_profit_data.__repr__())
#    f.write('\n\nMonthly Bottom 20 profitable skus: \n')
#    f.write(bottom20_profit_data.__repr__())