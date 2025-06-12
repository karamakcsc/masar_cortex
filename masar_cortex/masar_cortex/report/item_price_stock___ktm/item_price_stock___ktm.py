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
	query = """
		SELECT
			tip.item_code,
			ti.item_name,
			ti.item_group,
			ti.weight_per_unit,
			ti.custom_theoretical_wpu,
			tb.warehouse,
			(tb.actual_qty - tb.reserved_qty) AS available_qty,
			tbi.rate_per_kg,
			tip.price_list,
			tip.price_list_rate
		FROM `tabItem Price` tip
		INNER JOIN (
			SELECT MAX(name) AS max_name, item_code, MAX(valid_from) AS max_valid_from
			FROM `tabItem Price`
			WHERE selling = 1
			GROUP BY item_code
		) latest_tip
			ON tip.item_code = latest_tip.item_code
			AND tip.valid_from = latest_tip.max_valid_from
			AND tip.name = latest_tip.max_name
		INNER JOIN `tabItem` ti ON tip.item_code = ti.item_code
		LEFT JOIN `tabBin` tb ON tip.item_code = tb.item_code
		LEFT JOIN (
			SELECT DISTINCT
				item_code,
				item_price_ref,
				rate_per_kg,
				docstatus
			FROM `tabBulk Item Price Item`
			ORDER BY item_code, item_price_ref, rate_per_kg DESC
		) tbi
			ON tip.name = tbi.item_price_ref AND tip.item_code = tbi.item_code AND tbi.docstatus = 1
		WHERE (tb.actual_qty - tb.reserved_qty) > 0
	"""

	if filters.get("item_code"):
		query += f" AND tip.item_code = '{filters.get('item_code')}'"
	if filters.get("warehouse"):
		query += f" AND tb.warehouse = '{filters.get('warehouse')}'"

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