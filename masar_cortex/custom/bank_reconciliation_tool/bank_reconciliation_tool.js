frappe.ui.form.on("Bank Reconciliation Tool", {
    refresh: function(frm) {
        frm.add_custom_button(__("Save Record"), function () {
			if (!frm.doc.bank_account) {
				frappe.msgprint(__("Please select Bank Account"));
				return;
			}
			frappe.call({
				method: "masar_cortex.custom.bank_reconciliation_tool.bank_reconciliation_tool.save_bank_reconciliation_tool",
				args: {
					self: frm.doc
				},
				callback: function (r) {
					if (r.message) {
						frappe.msgprint(__("Record Saved Successfully"));
					}
				}
			});
		});
    }
});