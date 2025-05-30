// Copyright (c) 2025, KCSC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bulk Item Price Update", {
	calculate_new_rate: function(frm) {
        if (frm.doc.items.length > 0) {
            frm.doc.items.forEach(function(item) {
                if (item.weight_per_unit) {
                    new_price = item.rate_per_kg * item.weight_per_unit;
                    frappe.model.set_value(item.doctype, item.name, 'new_price', new_price);
                }
            });
            frm.refresh_field('items');
        } else {
            frappe.throw("Please get items first.")
        }
	},
    default_rate_per_kg: function(frm) {
        if (frm.doc.items && frm.doc.items.length > 0) {
            frm.doc.items.forEach(function(row) {
                row.rate_per_kg = frm.doc.default_rate_per_kg;
            });
            frm.refresh_field("items");
        }
    },
    onload_post_render: function(frm) {
        if (frm.is_new()) {
            frm.doc.items.forEach(function(item) {
                getAvailableQty(frm, item.doctype, item.name);
                // if (!item.weight_per_unit || !item.wpu) {
                //     frappe.db.get_doc('Item', item.item_code).then(item_doc => {
                //         frappe.model.set_value(item.doctype, item.name, 'weight_per_unit', item_doc.custom_theoretical_wpu || 0);
                //         frappe.model.set_value(item.doctype, item.name, 'wpu', item_doc.weight_per_unit || 0);
                //     });
                // }
            });
        }
    }
});

frappe.ui.form.on("Bulk Item Price Item", {
	rate_per_kg: function(frm, cdt, cdn) {
        calcRate(frm, cdn, cdt);
    },
    validate: function(frm, cdt, cdn){
        getAvailableQty(frm, cdt, cdn);
    },
    onload: function(frm, cdt, cdn){
        getAvailableQty(frm, cdt, cdn);
    },
    refresh: function(frm, cdt, cdn){
        getAvailableQty(frm, cdt, cdn);
    }
});


function calcRate(frm, cdn, cdt) {
    var row = locals[cdt][cdn];
    row.new_price = row.rate_per_kg * row.weight_per_unit;
    frm.refresh_field('items');
}


function getAvailableQty(frm, cdt, cdn) {
    var child = locals[cdt][cdn];
    if (child.item_code) {
        frappe.call({
            method:"masar_cortex.masar_cortex.doctype.bulk_item_price_update.bulk_item_price_update.available_qty",
            args: {
                item: child.item_code,
            },
            callback: function(r) {
                if (r.message) {
                    console.log(r.message);
                    frappe.model.set_value(child.doctype, child.name, 'custom_available_qty', r.message);
                }
            }
        })
    }
}

/// comments