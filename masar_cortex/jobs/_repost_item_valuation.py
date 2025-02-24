import frappe


def repost_stock_entry():
    stock_entries = frappe.db.sql("""
                SELECT name FROM `tabStock Entry` WHERE stock_entry_type = 'Slitting' AND docstatus = 1
            """, as_dict=True)

    if stock_entries:
        for se in stock_entries:
            # se_doc = frappe.get_doc("Stock Entry", se.name)        
            new_repost = frappe.new_doc("Repost Item Valuation")
            new_repost.based_on = "Transaction"
            new_repost.voucher_type = "Stock Entry"
            new_repost.voucher_no = se.name
            new_repost.save()
            new_repost.submit()
        execute_repost()


def execute_repost():
    """Execute repost item valuation via scheduler."""
    frappe.get_doc("Scheduled Job Type", "repost_item_valuation.repost_entries").enqueue(force=True)
    frappe.msgprint("Repost item valuation job has been successfully scheduled.", alert=True)