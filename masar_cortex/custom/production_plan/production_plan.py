import frappe

def validate(self, method):
    set_required_and_available_raw_materials(self)

def get_stock_qty_for_item(item_code, warehouse):
    return frappe.get_value("Bin", {"item_code": item_code, "warehouse": warehouse}, "actual_qty") or 0

def set_required_and_available_raw_materials(self):
    warehouse = "Semi-Finished Goods Store - MSCD"

    if not self.po_items:
        return

    for plan_item in self.po_items:
        if not plan_item.bom_no:
            continue

        bom = frappe.get_doc("BOM", plan_item.bom_no)
        if not bom.items:
            continue

        total_required_qty = 0
        total_available_qty = 0

        for bom_item in bom.items:
            raw_item_code = bom_item.item_code
            raw_qty = bom_item.qty
            available_qty = get_stock_qty_for_item(raw_item_code, warehouse)

            total_required_qty += raw_qty
            total_available_qty += available_qty

        plan_item.custom_required_raw_materials = total_required_qty
        plan_item.custom_available_raw_materials = total_available_qty
