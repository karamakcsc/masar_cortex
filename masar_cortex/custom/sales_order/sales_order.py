import frappe


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