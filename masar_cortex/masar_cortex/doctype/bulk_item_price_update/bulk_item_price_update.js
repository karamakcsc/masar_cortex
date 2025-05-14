// Copyright (c) 2025, KCSC and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Bulk Item Price Update", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Bulk Item Price Item", {
	rate_per_kg: function(frm, cdt, cdn) {
        calcRate(frm, cdn, cdt);
    },
});


function calcRate(frm, cdn, cdt) {
    var row = locals[cdt][cdn];
    console.log("Nice");
    row.new_price = row.rate_per_kg * row.weight_per_unit;
    frm.refresh_field('items');
}