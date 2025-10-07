# Copyright (c) 2025, KCSC
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


# ------------------------------------------------------------------------
# Columns
# ------------------------------------------------------------------------
def get_columns():
	return [
		{"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 130},
		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 160},
		{"label": _("Item Group"), "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 130},
		{"label": _("Weight Per Unit"), "fieldname": "weight_per_unit", "fieldtype": "Float", "width": 120},
		{"label": _("Theoretical WPU"), "fieldname": "theoretical_wpu", "fieldtype": "Float", "width": 130},
		{"label": _("Warehouse"), "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
		{"label": _("Rate Per Kg"), "fieldname": "rate_per_kg", "fieldtype": "Float", "width": 120},
		{"label": _("Available Qty"), "fieldname": "available_qty", "fieldtype": "Float", "width": 120},
		{"label": _("Selling Rate"), "fieldname": "selling_rate", "fieldtype": "Currency", "width": 130},
		{"label": _("Total Amount"), "fieldname": "total_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Total Weight"), "fieldname": "total_weight", "fieldtype": "Float", "width": 130},
	]


# ------------------------------------------------------------------------
# Data Fetching
# ------------------------------------------------------------------------
def get_data(filters):
	items = get_item_data(filters)
	result = []

	for d in items:
		available_qty = d.available_qty or 0
		theoretical_wpu = d.custom_theoretical_wpu or 0
		price = d.price_list_rate or 0
		rate_per_kg = d.rate_per_kg or 0

		result.append({
			"item_code": d.item_code,
			"item_name": d.item_name,
			"item_group": d.item_group,
			"weight_per_unit": d.weight_per_unit,
			"theoretical_wpu": theoretical_wpu,
			"warehouse": d.warehouse,
			"available_qty": available_qty,
			"rate_per_kg": rate_per_kg,
			"selling_rate": price,
			"total_amount": available_qty * price,
			"total_weight": available_qty * theoretical_wpu,
		})

	return result


# ------------------------------------------------------------------------
# Optimized Query
# ------------------------------------------------------------------------
def get_item_data(filters):
	conditions = []
	values = {}

	if filters.get("item_code"):
		conditions.append("i.item_code = %(item_code)s")
		values["item_code"] = filters["item_code"]

	if filters.get("warehouse"):
		conditions.append("b.warehouse = %(warehouse)s")
		values["warehouse"] = filters["warehouse"]

	where_clause = " AND ".join(conditions) if conditions else "1=1"

	# ⚡ Optimized SQL
	# - Uses window functions instead of correlated subqueries
	# - Avoids unnecessary GROUP BY
	# - Only joins the latest records once per table
	query = f"""
		WITH latest_price AS (
			SELECT ip.item_code, ip.price_list_rate,
				   ROW_NUMBER() OVER (PARTITION BY ip.item_code ORDER BY ip.modified DESC) AS rn
			FROM `tabItem Price` ip
			WHERE ip.selling = 1
		),
		latest_kg AS (
			SELECT tbipi.item_code, tbipi.rate_per_kg,
				   ROW_NUMBER() OVER (PARTITION BY tbipi.item_code ORDER BY tbipi.modified DESC) AS rn
			FROM `tabBulk Item Price Item` tbipi
			WHERE tbipi.docstatus = 1
		)
		SELECT
			i.item_code,
			i.item_name,
			i.item_group,
			i.weight_per_unit,
			i.custom_theoretical_wpu,
			b.warehouse,
			(b.actual_qty - b.reserved_qty) AS available_qty,
			lp.price_list_rate,
			lkg.rate_per_kg
		FROM `tabItem` i
		INNER JOIN `tabBin` b ON b.item_code = i.item_code
		LEFT JOIN latest_price lp ON lp.item_code = i.item_code AND lp.rn = 1
		LEFT JOIN latest_kg lkg ON lkg.item_code = i.item_code AND lkg.rn = 1
		WHERE (b.actual_qty - b.reserved_qty) > 0
		  AND {where_clause}
	"""

	return frappe.db.sql(query, values=values, as_dict=True)
