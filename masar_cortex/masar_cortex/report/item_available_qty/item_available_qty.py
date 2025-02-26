# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	return columns(), data(filters)

def data(filters):
    conditions='1=1'
    if filters.get('item_code'):
         conditions += f' AND bi.item_code ="{filters.get("item_code")}"'
    if filters.get('warehouse'):
        conditions += f' AND bi.warehouse ="{filters.get("warehouse")}"'
    sql = frappe.db.sql(f"""
	SELECT 
    bi.item_code,
    ti.item_name,
    bi.warehouse,
    bi.stock_uom,                                        
    bi.actual_qty,
    bi.reserved_qty,
    bi.projected_qty,
    
    (bi.actual_qty - bi.reserved_qty) AS available_qty
    
	FROM tabBin bi 
	INNER JOIN tabItem ti 
	ON bi.item_code = ti.item_code
    WHERE {conditions}
""")
    return sql


def columns():
    return[
         "Item Code:Link/Item:300",
         "Item Name:Data:300",
         "Warehouse:Link/Warehouse:200",
         "UOM:Link/UOM:300",
         "Actual Qty:Float:300",
         "Reserved Qty:Float:300",
         "Projected Qty:Float:200",
         
         "Available Qty:Float:300"
         
	]