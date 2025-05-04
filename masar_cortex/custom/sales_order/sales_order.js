frappe.ui.form.on('Sales Order Item', {
    item_code: function(frm, cdt, cdn) {
        getAvailableQty(frm, cdt, cdn);
    },
    warehouse: function (frm, cdt, cdn) {
        getAvailableQty(frm, cdt, cdn);
    },
    validate: function(frm, cdt, cdn) {
        getAvailableQty(frm, cdt, cdn);
    }
});

function getAvailableQty(frm, cdt, cdn) {
    var child = locals[cdt][cdn];
    if (child.item_code && child.warehouse) {
        console.log(child.warehouse);
        console.log(child.item_code);
        frappe.call({
            method:"masar_cortex.custom.sales_order.sales_order.available_qty_sql",
            args: {
                item: child.item_code,
                warehouse: child.warehouse
            },
            callback: function(r) {
                if (r.message) {
                    console.log(r.message);
                    // child.custom_available_qty = r.message;
                    frappe.model.set_value(cdt, cdn, 'custom_available_qty', r.message);
                }
            }
        })
    }
}