import frappe


def validate(self, method):
    get_available_qty(self)

def get_available_qty(self):
    if self.items:
        for item in self.items:
            if item.item_code and item.warehouse:
                item.custom_available_qty = available_qty_sql(item.item_code, item.warehouse)
            
def available_qty_sql(item, warehouse):
    if item:
        sql = frappe.db.sql("""
                             SELECT (bi.actual_qty - bi.reserved_qty) AS available_qty 
                             FROM tabBin bi 
                             WHERE bi.item_code = %s AND bi.warehouse = %s
                             """, (item, warehouse, ), as_dict=True)
        
        if sql and sql[0] and sql[0]['available_qty']:
            return sql[0]['available_qty']