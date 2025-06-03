frappe.ui.form.on('Sales Order', {
    validate: function(frm) {
        getAvailableQty(frm);
    }
});

frappe.ui.form.on('Sales Order Item', {
    item_code: function(frm, cdt, cdn) {
        getAvailableQtyForChild(frm, cdt, cdn);
    }
});


function getAvailableQty(frm) {
    frm.doc.items.forEach(function(row) {
        if (row.item_code && row.warehouse) {
            frappe.call({
                method: "masar_cortex.custom.sales_order.sales_order.available_qty_sql",
                args: {
                    item: row.item_code,
                    warehouse: row.warehouse
                },
                callback: function(r) {
                    if (r.message) {
                        console.log(`Available qty for ${row.item_code} in ${row.warehouse}: ${r.message}`);
                        frappe.model.set_value(row.doctype, row.name, 'custom_available_qty', r.message);
                    }
                }
            });
        }
    });
}


function getAvailableQtyForChild(frm, cdt, cdn) {
    var child = locals[cdt][cdn];

    setTimeout(function () {
        console.log(child.warehouse);
        if (child.item_code && child.warehouse) {
            frappe.call({
                method: "masar_cortex.custom.sales_order.sales_order.available_qty_sql",
                args: {
                    item: child.item_code,
                    warehouse: child.warehouse
                },
                callback: function (r) {
                    if (r.message !== undefined) {
                        frappe.model.set_value(cdt, cdn, 'custom_available_qty', r.message);
                    }
                }
            });
        }
    }, 1000); // delay for 300ms
}