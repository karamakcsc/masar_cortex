// Copyright (c) 2025, KCSC and contributors
// For license information, please see license.txt

frappe.query_reports["Production Plan Report"] = {
	"filters": [
		{
			"fieldname":"p_plan",
			"label":"Production Plan",
			"fieldtype": "Link",
			"options": "Production Plan"
		},
		{
			"fieldname": "item_code",
			"label": "Item Code",
			"fieldtype": "Link",
			"options": "Item"
		}
	]
};
