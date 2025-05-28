import frappe

@frappe.whitelist()
def create_gate_pass(dn_name):
    if not dn_name:
        frappe.throw("Delivery Note name is required.")

    dn = frappe.get_doc("Delivery Note", dn_name)
    gate_pass = frappe.new_doc("Gate Pass")
    gate_pass.delivery_note = dn.name
    gate_pass.customer = dn.customer
    gate_pass.posting_date = frappe.utils.nowdate()

    gate_pass.insert()
    frappe.db.commit()

    return gate_pass.name