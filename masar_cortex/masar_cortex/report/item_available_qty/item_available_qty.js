// Copyright (c) 2025, KCSC and contributors
// For license information, please see license.txt

frappe.query_reports["Item Available Qty"] = {
	"filters": [
		{
			"fieldname":"item_code",
			"label":"Item",
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname":"warehouse",
			"label":"Warehouse",
			"fieldtype":"Link",
			"options":"Warehouse"
		}
	]
};
