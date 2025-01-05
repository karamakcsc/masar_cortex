

frappe.ui.form.on('Stock Entry', {
    refresh: function(frm){ 
        frm.add_custom_button(__("Calculate"), function() {
            frappe.call({
                method: "masar_cortex.custom.stock_entry.stock_entry.calculate_cost_qty", 
                args:{
                    self:frm.doc,
                }, 
                callback: function(r){ 
                    frappe.msgprint(r.message);
                }
            })
    });
}
});