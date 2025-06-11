# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	return columns(), data(filters)


def data(filters):
	conditions = " 1=1 "
	if filters.get("d_note"):
		conditions += f" AND tdn.name = '{filters.get('d_note')}'"
	if filters.get("item_code"):
		conditions += f" AND tdni.item_code = '{filters.get('item_code')}'"
  
	_from, to = filters.get("from"), filters.get("to")
	if _from and to:
		conditions += f" AND tdn.posting_date BETWEEN '{_from}' AND '{to}'"
  
	sql = frappe.db.sql(f"""
		SELECT 
			tdn.name AS `Delievry Note #`,
			tdn.customer AS `Customer`,
			tdn.posting_date AS `Posting Date`,
			tdn.total_qty AS `Total DN Qty`,
			tdn.custom_delivered_qty AS `Total DN Delivered Qty`,
			(tdn.total_qty - tdn.custom_delivered_qty) AS `Total Remaining Qty`,
			tdni.item_code AS `Item Code`,
			tdni.rate AS `Price`,
			tdni.qty AS `Qty`,
			tdni.custom_delivered_qty AS `Item Delivered Qty`,
			(tdni.qty - tdni.custom_delivered_qty) AS `Item Remaining Qty`,
			((tdni.qty - tdni.custom_delivered_qty) * tdni.rate) AS `Item Remaining Amount`
		FROM `tabDelivery Note` tdn 
		INNER JOIN `tabDelivery Note Item` tdni ON tdn.name = tdni.parent
		WHERE {conditions} AND tdn.docstatus = 1
		ORDER BY tdn.name 
	""")

	return sql

def columns():
    return [
		"Delievry Note #:Link/Delivery Note:200",
		"Customer:Link/Customer:200",
		"Posting Date:Date:150",
		"Total DN Qty:Float:150",
		"Total DN Delivered Qty:Float:200",
		"Total Remaining Qty:Float:200",
		"Item Code:Link/Item:200",
		"Price:Currency:125",
		"Qty:Float:125",
		"Item Delivered Qty:Float:175",
		"Item Remaining Qty:Float:175",
		"Item Remaining Amount:Currency:200",
	]
