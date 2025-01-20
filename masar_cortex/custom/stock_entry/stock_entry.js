frappe.ui.form.on("Stock Entry", {
    refresh: function(frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(__("View Cost"), function() {
                frappe.call({
                    method: "masar_cortex.custom.stock_entry.stock_entry.calculate_cost_qty",
                    args: {
                        self: frm.doc,
                    },
                    callback: function(r) {
                        frappe.msgprint(r.message);
                    }
                });
            });
        }
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Re-Calculate Cost"), function() {
                frappe.call({
                    method: "masar_cortex.custom.stock_entry.stock_entry.recalculate_costs",
                    args: {
                        self: frm.doc,
                    },
                    callback: function(r) {
                        if (r.message) {
                            frm.refresh_field("items");
                            frm.reload_doc();
                            frm.reload();
                            frappe.msgprint("Re-Calculate Completed", alert=true);
                        }
                    }
                });
            });
        }
    }
});
