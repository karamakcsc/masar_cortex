// Copyright (c) 2025, KCSC and contributors
// For license information, please see license.txt

frappe.query_reports["Item Price Stock - KTM"] = {
	"filters": [
		{
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item",
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
			default: "Finished Goods Store - CKTM"
		},
	]
};
