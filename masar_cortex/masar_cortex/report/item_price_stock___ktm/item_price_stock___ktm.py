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
	item_price = frappe.qb.DocType("Item Price")
	bin = frappe.qb.DocType("Bin")
	item = frappe.qb.DocType("Item")

	query = (
		frappe.qb.from_(item_price)
		.inner_join(item)
		.on(item_price.item_code == item.item_code)
		.left_join(bin)
		.on(item_price.item_code == bin.item_code)
		.select(
			item_price.item_code,
			item_price.item_name,
			item.item_group,
			item.weight_per_unit,
			item.custom_theoretical_wpu,
			item_price.name.as_("price_list_name"),
			bin.warehouse.as_("warehouse"),
			(bin.actual_qty - bin.reserved_qty).as_("available_qty"),
		)
		.where((bin.actual_qty - bin.reserved_qty) > 0)
	)

	if filters.get("item_code"):
		query = query.where(item_price.item_code == filters.get("item_code"))
	if filters.get("warehouse"):
		query = query.where(bin.warehouse == filters.get("warehouse"))

	item_results = query.run(as_dict=True)

	price_list_names = list(set(item.price_list_name for item in item_results))

	selling_price_map = get_price_map(price_list_names, selling=1)

	result = []
	if item_results:
		for item_dict in item_results:
			data = {
				"item_code": item_dict.item_code,
				"item_name": item_dict.item_name,
				"item_group": item_dict.item_group,
				"wpu": item_dict.weight_per_unit,
				"theoretical_wpu": item_dict.custom_theoretical_wpu,
				"warehouse": item_dict.warehouse,
				"available_qty": item_dict.available_qty or 0,
				"selling_price_list": "",
				"selling_rate": 0.0,
				"total_amount": 0.0,
				"total_weight": (item_dict.available_qty or 0) * item_dict.custom_theoretical_wpu
			}

			price_list = item_dict["price_list_name"]
			if selling_price_map.get(price_list):
				data["selling_price_list"] = selling_price_map.get(price_list)["Selling Price List"] or ""
				data["selling_rate"] = selling_price_map.get(price_list)["Selling Rate"] or 0
				data["total_amount"] = data["selling_rate"] * data["available_qty"]

			result.append(data)

	return result


def get_price_map(price_list_names, buying=0, selling=0):
	price_map = {}

	if not price_list_names:
		return price_map

	rate_key = "Buying Rate" if buying else "Selling Rate"
	price_list_key = "Buying Price List" if buying else "Selling Price List"

	filters = {"name": ("in", price_list_names)}
	if buying:
		filters["buying"] = 1
	else:
		filters["selling"] = 1

	pricing_details = frappe.get_all(
		"Item Price", fields=["name", "price_list", "price_list_rate"], filters=filters
	)

	for d in pricing_details:
		name = d["name"]
		price_map[name] = {price_list_key: d["price_list"], rate_key: d["price_list_rate"]}

	return price_map