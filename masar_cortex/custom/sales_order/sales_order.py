import frappe
from frappe.utils import nowdate

def validate(self, method):
    validate_overdue_limit(self)
    validate_actual_qty(self)

        
def validate_actual_qty(self):
    if self.items:
        for item in self.items:
            if item.qty > item.custom_available_qty or item.custom_available_qty < 0:
                frappe.throw(f"Available quantity for item {item.item_code} is less than the requested quantity.")
                
@frappe.whitelist()            
def available_qty_sql(item, warehouse):
    if item:
        sql = frappe.db.sql("""
                             SELECT (bi.actual_qty - bi.reserved_qty) AS available_qty 
                             FROM tabBin bi 
                             WHERE bi.item_code = %s AND bi.warehouse = %s
                             """, (item, warehouse, ), as_dict=True)
        
        if sql and sql[0] and sql[0]['available_qty']:
            return sql[0]['available_qty']
        else:
            return 0
        
def validate_overdue_limit(self):
    if self.customer:
        overdue_amount = get_customer_overdue_amount(self.customer)
        customer_doc = frappe.get_doc("Customer", self.customer)
        if customer_doc.credit_limits:
            for limit in customer_doc.credit_limits:
                if limit.custom_bypass_overdue_check:
                    continue
                if limit.custom_overdue_limit and limit.custom_overdue_limit > 0:
                    if overdue_amount > limit.custom_overdue_limit:
                        frappe.throw(f"Customer: <b>{self.customer}</b> has an overdue amount of <b>{overdue_amount}</b>, which exceeds the allowed overdue limit of <b>{limit.custom_overdue_limit}</b>.")
        # if overdue_amount and overdue_amount > 0:
        #     frappe.throw(f"Customer: <b>{self.customer}</b> has an overdue amount of <b>{overdue_amount}</b>. Please clear the dues before proceeding with the sales order.")

def get_customer_overdue_amount(customer):
    overdue = frappe.db.sql("""
        SELECT SUM(outstanding_amount) 
        FROM `tabSales Invoice`
        WHERE customer=%s 
          AND docstatus=1
          AND outstanding_amount > 0
          AND due_date < %s
    """, (customer, nowdate()))[0][0] or 0
    return overdue