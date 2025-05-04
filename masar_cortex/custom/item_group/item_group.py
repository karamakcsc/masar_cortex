import frappe

@frappe.whitelist()
def update_item_price(item_group, rate_kg):
    items_sql = frappe.db.sql("""
            SELECT ti.name, ti.item_name, ti.item_group, ti.weight_per_unit, ti.stock_uom
            FROM tabItem ti
            WHERE ti.item_group = %s
        """, (item_group,), as_dict=True)
    
    item_price_sql = frappe.db.sql("""
            SELECT tip.name, tip.item_code, tip.price_list_rate 
            FROM `tabItem Price` tip 
            INNER JOIN tabItem ti ON tip.item_code = ti.name
            WHERE ti.item_group = %s AND tip.valid_from = %s
        """, (item_group, frappe.utils.nowdate()), as_dict=True)
    
    exisiting_item_price = set()
    for item_price in item_price_sql:
        exisiting_item_price.add(item_price['item_code'])
        
    if items_sql:
        for item in items_sql:
            if item.name in exisiting_item_price:
                # frappe.msgprint(str(f"The item: {item.name} already has a price list rate."))
                continue
            
            if item.weight_per_unit in [None, 0]:
                frappe.throw(str(f"The item: {item.name}'s weight per unit is empty or 0."))
            
            new_price = float(item.weight_per_unit) * float(rate_kg)
            new_item_price = frappe.new_doc("Item Price")
            new_item_price.item_code = item.name
            new_item_price.uom = item.stock_uom
            new_item_price.price_list = "Standard Selling"
            new_item_price.price_list_rate = new_price
            new_item_price.valid_from = frappe.utils.nowdate()
            new_item_price.save()

        frappe.msgprint(str(f"All item prices in the item group: {item_group} have been updated successfully."), alert=True, indicator='green')
    else:
        frappe.msgprint(str(f"There are no items in the item group: {item_group}."), alert=True, indicator='red')