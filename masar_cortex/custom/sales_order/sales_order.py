import frappe


def validate(self, method):
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