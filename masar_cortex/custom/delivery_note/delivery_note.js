// Copyright (c) 2023, KCSC and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delivery Note', {
	refresh: function(frm) {
        createGatePass(frm);
	}
});

function createGatePass(frm) {
    if (frm.doc.docstatus === 1) {
        frm.add_custom_button(__("Create Gate Pass"), function() {
                frappe.call({
                    method: "masar_cortex.custom.delivery_note.delivery_note.create_gate_pass",
                    args: {
                        dn_name: frm.doc.name,
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.set_route('Form', 'Gate Pass', r.message);
                        }
                    }
                });
            });
    }
}