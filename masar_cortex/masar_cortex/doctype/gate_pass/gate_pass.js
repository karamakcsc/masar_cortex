// Copyright (c) 2025, KCSC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Gate Pass", {
	get_deliver_note_items: function(frm) {
        getDnItems(frm);
	},
});


function getDnItems(frm) {
    if (frm.doc.delivery_note && frm.doc.docstatus === 0) {
        frappe.call({
            doc: frm.doc,
            method: "get_dn_items",
            callback: function (r) {
                if (r.message) {
                    frm.clear_table("dn_items");
                    r.message.forEach(function (item) {
                        let row = frm.add_child("dn_items");
                        row.item_code = item.item_code;
                        row.item_name = item.item_name;
                        row.delivery_note_qty = item.qty;
                        row.qty = item.qty;
                        row.dn_name = item.dn_name;
                    });
                    frm.refresh_field("dn_items");
                    console.log("Items fetched successfully:", r.message);
                } else {
                    frappe.msgprint(__("All items are delivered for the selected Delivery Note."));
                }
            }
        });
    }
}
