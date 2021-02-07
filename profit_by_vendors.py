#!/usr/bin/env python
# coding: utf-8
################################################################################################################################################################################################################################################################################################################################################
# Purpose: Analyze profits by each vendor
#
# Input: 1 csv file
#        Data: Optimized Analysis Table, monthly csv file
#        Note1: Here We use 1 csv file for December 2020
# 
# Required Columns: [Sales Sku, Sales Order Number, Sales Order Date, Sales Channel Name, Fulfillment Item Id, Fulfillment Sku, Fulfillment Order Number, Fulfillment Channel Name, Fulfillment Channel Type, Quantity, Sku, Total Sales, Total Cost, Commission, Inventory Cost, Estimated Shipping Cost, Invoice Shipping Cost, Profit, Flag]
#        Note1: Before running this program, check column names in Sales Analysis Table, especially empty spaces.
#
# Output: 2 csv files
#        xlsx: Top 20 Profits/Losses SKUs in each vendor, one sheet per vendor.
#        csv: Business information by vendors
# 
# Customized configuration - Only need to change variables below: 
# * vendor_list    <- Add/Drop vendors
# * data           <- csv file of Optimized Analysis Table
# * pd.ExcelWriter <- Path of excel output file
# * info_df.to_csv <- Path of csv output file  
#
################################################################################################################################################################################################################################################################################################################################################
import pandas as pd
import numpy as np

# List of vendors, add here when cooperating new vendors
vendor_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

# Creating Excel Writer Object from Pandas  
writer = pd.ExcelWriter('output/analysis_result/Profit_by_Vendors/Top_Bottom_Profit_Sku_by_Vendors.xlsx',engine='xlsxwriter', mode='w')   
workbook = writer.book

info_list = []
for v in vendor_list:
    # import monthly data
    data = pd.read_csv('data/optimized_analysis_table_dec.csv')  

    # Filter Vendors' data
    vendor_data = data[data['Fulfillment Channel Name'] == v]

    # Keep columns: Sku, Profit
    vendor_data = vendor_data[['Sku', 'Total Sales', 'Profit']]

    # Group by sku
    vendor_agg_data = vendor_data.groupby('Sku').agg({'Total Sales': sum, 'Profit':sum, 'Sku':len})                                                 .rename(columns={'Sku': 'Orders'})
    vendor_agg_data['Margin'] = round(vendor_agg_data['Profit'] / vendor_agg_data['Total Sales'],2)

    # Sort by total profits
    vendor_agg_data = vendor_agg_data.sort_values(by=['Profit'], ascending=False)

    # top 20 & bottom 20 profits/losses
    top20_sales = vendor_agg_data[:20]
    top20_sales.reset_index(inplace=True)
    top20_sales.index += 1
    
    vendor_agg_data_for_bottom = vendor_agg_data.sort_values(by=['Profit'], ascending=True)
    bottom20_sales = vendor_agg_data_for_bottom[:20]
    bottom20_sales.reset_index(inplace=True)
    bottom20_sales.index += 1

    # Basic stats
    # Total orders & distinct Skus & breakeven
    total_orders = vendor_data['Sku'].count()
    total_skus = vendor_agg_data['Profit'].count()
    total_profits = round(vendor_data['Profit'].sum(),2)
    total_sales = round(vendor_data['Total Sales'].sum(),2)
    if total_sales != 0:
        total_margin = total_profits / total_sales
        total_margin = round(total_margin,2)
    else:
        total_margin = 0
    
    # File in Excel
    worksheet=workbook.add_worksheet(v)
    writer.sheets[v] = worksheet
    worksheet.write_string(0, 0, 'Monthly Top 20 Losses: ')
    bottom20_sales.to_excel(writer,sheet_name=v,startrow=1 , startcol=0)   
    worksheet.write_string(23, 0, 'Monthly Top 20 Profits: ')
    top20_sales.to_excel(writer,sheet_name=v,startrow=24, startcol=0)
        
    # Integrate business information with each vendors
    business_data = [v, total_profits, total_sales, total_margin, total_orders, total_skus]
    info_list.append(business_data)
    
# Create a file for business information
info_df = pd.DataFrame(info_list, columns=['Vendor', 'Monthly Breakeven', 'Monthly Sales', 'Margin', 'Monthly Orders', 'Monthly Skus'])
info_df = info_df.set_index('Vendor')
info_df.to_csv('output/analysis_result/Profit_by_Vendors/Profits_Info_by_AllVendors.csv')

# Save file for xlsx
writer.save()