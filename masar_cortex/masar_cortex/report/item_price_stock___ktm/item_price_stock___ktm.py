# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters, columns)
	return columns, data


def get_columns():
	return [
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 120,
		},
		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 120},
		{
			"label": _("Item Group"),
			"fieldname": "item_group",
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 120,
		},
		{"label": _("Weight Per Unit"), "fieldname": "wpu", "fieldtype": "Float", "width": 120},
		{"label": _("Weight"), "fieldname": "theoretical_wpu", "fieldtype": "Float", "width": 120},
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 120,
		},
		{"label": _("Rate Per Kg"), "fieldname": "rate_per_kg", "fieldtype": "Float", "width": 120},
		{
			"label": _("Available Qty"),
			"fieldname": "available_qty",
			"fieldtype": "Float",
			"width": 120,
		},
		{"label": _("Selling Price"), "fieldname": "selling_rate", "fieldtype": "Currency", "width": 120},
		{"label": _("Total Amount"), "fieldname": "total_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Total Weight"), "fieldname": "total_weight", "fieldtype": "Float", "width": 120},
	]


def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data


def get_item_price_qty_data(filters):
	conditions = " 1=1 "
	if filters.get("item_code"):
		conditions += f" AND pl.item_code = '{filters.get('item_code')}'"
	if filters.get("warehouse"):
		conditions += f" AND b.warehouse = '{filters.get('warehouse')}'"
	query = f"""
			WITH price_list AS ( SELECT 
				ip.item_code , 
				ip.price_list,
				ip.price_list_rate
			FROM `tabItem Price` ip 
			WHERE ip.selling = 1
			AND ip.modified = (
                SELECT MAX(modified)
                FROM `tabItem Price` ip2
                WHERE ip2.item_code = ip.item_code AND ip2.selling = 1
            )
			GROUP BY ip.item_code ) , 
			item AS (SELECT  
				item_code , 
				item_name , 
				item_group , 
				weight_per_unit , 
				custom_theoretical_wpu 
			FROM tabItem i 
			), 
			bin AS (
				SELECT item_code , warehouse  , 
				(actual_qty  - reserved_qty) AS available_qty 
				FROM tabBin tb 
				HAVING available_qty > 0 
			) , 
			by_kg AS (
			SELECT item_code , rate_per_kg FROM 
			`tabBulk Item Price Item` tbipi
			WHERE docstatus = 1
			AND tbipi.modified = (
                SELECT MAX(modified)
                FROM `tabBulk Item Price Item` tbipi2
                WHERE tbipi2.item_code = tbipi.item_code
            )
			GROUP BY item_code 
			)
			SELECT 
				pl.item_code , i.item_name , i.item_group , 
				i.weight_per_unit , i.custom_theoretical_wpu , 
				b.warehouse ,  b.available_qty , kg.rate_per_kg , pl.price_list , pl.price_list_rate
			FROM price_list pl
			INNER JOIN item  i ON pl.item_code = i.item_code 
			INNER JOIN bin b ON b.item_code = pl.item_code
			INNER JOIN by_kg kg ON  pl.item_code = kg.item_code
			WHERE {conditions}
	"""

	item_results = frappe.db.sql(query, as_dict=True)

	result = []
	for item_dict in item_results:
		available_qty = item_dict.available_qty or 0
		theoretical_wpu = item_dict.custom_theoretical_wpu or 0
		price = item_dict.price_list_rate or 0

		result.append({
			"item_code": item_dict.item_code,
			"item_name": item_dict.item_name,
			"item_group": item_dict.item_group,
			"wpu": item_dict.weight_per_unit,
			"theoretical_wpu": theoretical_wpu,
			"warehouse": item_dict.warehouse,
			"available_qty": available_qty,
			"rate_per_kg": item_dict.rate_per_kg,
			"selling_rate": price,
			"total_amount": available_qty * price,
			"total_weight": available_qty * theoretical_wpu,
		})

	return result