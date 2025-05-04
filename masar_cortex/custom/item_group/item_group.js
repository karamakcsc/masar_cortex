frappe.ui.form.on("Item Group", {
    custom_update_item_price: function(frm) {
        updateItemPrice(frm);
    }
});


function updateItemPrice(frm) {
    if (frm.doc.custom_rate_kg) {
        frappe.call({
            method: "masar_cortex.custom.item_group.item_group.update_item_price",
            args: {
                item_group: frm.doc.name,
                rate_kg: frm.doc.custom_rate_kg
            },
            callback: function(r) {
                console.log("r.message");
            }
        })
    } else {
        frappe.msgprint(__('Please enter rate per kg.'));
    }
}