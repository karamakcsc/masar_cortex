// Copyright (c) 2025, KCSC and contributors
// For license information, please see license.txt

frappe.query_reports["Delivery Note Report"] = {
	"filters": [
		{
			"fieldname": "d_note",
			"label": "Delivery Note",
			"fieldtype": "Link",
			"options": "Delivery Note"
		},
		{
			"fieldname": "item_code",
			"label": "Item Code",
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname": "from",
			"label": "From Date",
			"fieldtype": "Date"
		},
		{
			"fieldname": "to",
			"label": "To Date",
			"fieldtype": "Date"
		}
	]
};
