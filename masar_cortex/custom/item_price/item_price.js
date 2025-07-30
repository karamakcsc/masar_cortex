frappe.ui.form.on("Item Price", {
    custom_rate_per_kg: function(frm) {
        if (frm.doc.custom_weight_per_unit && frm.doc.custom_rate_per_kg > 0) {
            frm.set_value("price_list_rate", frm.doc.custom_weight_per_unit * frm.doc.custom_rate_per_kg);
            frm.refresh_field("price_list_rate");
        }
    }
})