import frappe
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
update_status = SalesOrder.update_status


def update_so_status():
    so_sql = frappe.db.sql("""
            SELECT name FROM `tabSales Order` WHERE delivery_date < CURDATE() AND docstatus = 1 and status != 'Closed'
        """, as_dict=True)
    
    if so_sql and so_sql[0] and so_sql[0]['name']:
        for so in so_sql:
            so_doc = frappe.get_doc("Sales Order", so.name)
            # if so_doc.status != "Closed":
            update_status(so_doc, "Closed")