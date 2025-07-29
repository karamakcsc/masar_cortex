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
		},
		{
			"fieldname": "pp_status",
			"label": "Production Plan Status",
			"fieldtype": "Select",
			"options": "\nDraft\nSubmitted\nNot Started\nIn Process\nCompleted\nClosed\nCancelled\nMaterial Requested"
		},
		{
			"fieldname": "wo_status",
			"label": "Work Order Status",
			"fieldtype": "Select",
			"options": "\nDraft\nSubmitted\nNot Started\nIn Process\nCompleted\nStopped\nClosed\nCancelled"
		}
	]
};
