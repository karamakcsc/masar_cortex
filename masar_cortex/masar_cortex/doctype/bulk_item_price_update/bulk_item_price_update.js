// Copyright (c) 2025, KCSC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bulk Item Price Update", {
	validate: function(frm) {
        if (frm.doc.items.length > 0) {
            frm.doc.items.forEach(function(item) {
                if (item.weight_per_unit) {
                    item.new_price = item.rate_per_kg * item.weight_per_unit;
                } else {
                    frappe.throw("Weight per unit is required for all items.");
                }
            });
            frm.refresh_field('items');
        }
	},
});

frappe.ui.form.on("Bulk Item Price Item", {
	rate_per_kg: function(frm, cdt, cdn) {
        calcRate(frm, cdn, cdt);
    },
});


function calcRate(frm, cdn, cdt) {
    var row = locals[cdt][cdn];
    row.new_price = row.rate_per_kg * row.weight_per_unit;
    frm.refresh_field('items');
}