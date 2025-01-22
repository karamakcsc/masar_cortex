import frappe
import json
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry
update_stock_ledger = StockEntry.update_stock_ledger
make_gl_entries = StockEntry.make_gl_entries
set_total_incoming_outgoing_value = StockEntry.set_total_incoming_outgoing_value


def validate(self, method):
    validate_items(self)
    calc_cost_qty(self)

# def on_submit(self, method):
#     calc_cost_qty(self)

def calc_cost_qty(self):
    if self.stock_entry_type == "Slitting":
        total_raw_material_cost = 0
        total_finished_qty = 0
        # Calculate total raw material cost and total finished goods quantity
        for item in self.items:
            if item.s_warehouse:
                total_raw_material_cost = total_raw_material_cost + (item.basic_rate * item.qty)
            if item.is_finished_item and not item.is_scrap_item and item.t_warehouse:
                total_finished_qty += item.qty
        if self.total_additional_costs:
            total_raw_material_cost  += self.total_additional_costs 
        # Validate that raw material cost and finished goods quantity are defined
        if total_raw_material_cost == 0:
            frappe.throw("Total raw material cost is zero. Please ensure raw materials are properly defined.")
        if total_finished_qty == 0:
            frappe.throw("Total finished goods quantity is zero. Please ensure finished goods are properly defined.")
        # Distribute costs across finished goods
        cost_per_unit = (total_raw_material_cost / total_finished_qty) 
        for item in self.items:
            if item.is_finished_item and not item.is_scrap_item and item.t_warehouse:
                # Calculate percentage of this finished item's quantity
                # percentage = item.qty / total_finished_qty
                # cost_per_unit = (total_raw_material_cost * percentage) / item.qty
               
                # Update Basic Rate and Amount
                # item.basic_rate = cost_per_unit
                amount = cost_per_unit * item.qty
                item.basic_rate = cost_per_unit
                item.valuation_rate = cost_per_unit
                item.amount = amount
                self.save
                # Handle Scrap Items
            if item.is_scrap_item:
                # Assign a minimal cost to scrap items to avoid accounting errors
                item.basic_rate = 0.01
                item.valuation_rate  = 0.01
                item.amount = item.qty * item.basic_rate
                self.save
        return True


def validate_items(self):
    if self.stock_entry_type == "Slitting":
        total_target_qty = 0
        total_source_qty = 0
        for item in self.items:
            if item.s_warehouse:
                # frappe.msgprint(f" {item.item_code} source")
                total_source_qty += item.qty    
            if item.t_warehouse:
                # frappe.msgprint(f" {item.item_code} target")
                total_target_qty += item.qty
        if total_target_qty != total_source_qty:
            frappe.throw("Input Quantity Does Not Equal The Output Quantity.")
        
        for item in self.items:
            if item.t_warehouse:
                if not (item.is_finished_item or item.is_scrap_item):
                    frappe.throw(
                        f"Item {item.item_code} in Target Warehouse must be marked as either Finished or Scrap."
                    )
                if item.is_finished_item and item.is_scrap_item:
                    frappe.throw(
                        f"Item {item.item_code} cannot be both Finished and Scrap."
                    )
            
            
@frappe.whitelist()    
def calculate_cost_qty(self):
    self = frappe._dict(json.loads(self))
    if self.get('stock_entry_type') == "Slitting":
        total_raw_material_cost = 0
        total_finished_qty = 0
        for item in self.get('items'):
            if item.get('s_warehouse'):
                total_raw_material_cost = total_raw_material_cost + (item.get('basic_rate') * item.get('qty'))
            if not item.get('is_scrap_item') and item.get('t_warehouse'):
                total_finished_qty += item.get('qty')
        if self.get('total_additional_costs'):
            total_raw_material_cost  += self.get('total_additional_costs')
        cost_per_unit = (total_raw_material_cost / total_finished_qty) 
        return str(f"""
                   Total Finished Qty : {total_finished_qty}<br>
                   Total Raw Material Cost : { total_raw_material_cost} <br>
                   Cost Per Unit : {cost_per_unit}
                   """)
        
        
@frappe.whitelist()
def recalculate_costs(self):
    self = frappe._dict(json.loads(self))
    if self.stock_entry_type == "Slitting":
        
        #### Loop For Scrap, Finished Checkbox ####
        
        for item in self.get('items'):
            if item.get('t_warehouse') == 'Semi-Finished Goods Store - CKTM':
                frappe.db.set_value(item['doctype'], item['name'], "is_finished_item", 1)
                item['is_finished_item'] = 1
            if item.get('t_warehouse') == 'Scrap Store - CKTM':
                frappe.db.set_value(item['doctype'], item['name'], "is_scrap_item", 1)
                item['is_scrap_item'] = 1
        
        frappe.db.commit()
        #### End ####
        total_raw_material_cost = 0
        total_finished_qty = 0
        for item in self.get('items'):
            if item.get('s_warehouse'):
                total_raw_material_cost = total_raw_material_cost + (item.get('basic_rate') * item.get('qty'))
            if  not item.get('is_scrap_item') and item.get('t_warehouse'):# item.get('is_finished_item') and not item.get('is_scrap_item') and item.get('t_warehouse'):
                total_finished_qty += item.get('qty')
        if self.get('total_additional_costs'):
            total_raw_material_cost += self.get('total_additional_costs')

        if total_raw_material_cost == 0:
            frappe.throw("Total raw material cost is zero. Please ensure raw materials are properly defined.")
        if total_finished_qty == 0:
            frappe.throw("Total finished goods quantity is zero. Please ensure finished goods are properly defined.")

        cost_per_unit = (total_raw_material_cost / total_finished_qty) 
        for item in self.get('items'):
            if not item.get('is_scrap_item') and item.get('t_warehouse'): #item.get('is_finished_item') and not item.get('is_scrap_item') and item.get('t_warehouse'):
                frappe.db.set_value(item['doctype'], item['name'], "basic_rate", cost_per_unit)
                item['basic_rate'] = cost_per_unit
                frappe.db.set_value(item['doctype'], item['name'], "valuation_rate", cost_per_unit)
                item['valuation_rate'] = cost_per_unit
                frappe.db.set_value(item['doctype'], item['name'], "amount", cost_per_unit * item.get('qty'))
                item['amount'] = cost_per_unit * item.get('qty')
            elif item.get('is_scrap_item'):
                frappe.db.set_value(item['doctype'], item['name'], "basic_rate", 0.01)
                item['basic_rate'] = 0.01
                frappe.db.set_value(item['doctype'], item['name'], "valuation_rate", 0.01)
                item['valuation_rate'] = 0.01
                frappe.db.set_value(item['doctype'], item['name'], "amount", 0.01 * item.get('qty'))
                item['amount'] = 0.01 * item.get('qty')
        # self.run_method('save')
        frappe.db.commit()
        doc = frappe.get_doc("Stock Entry", self['name'])
        set_total_incoming_outgoing_value(doc)
        
        sle = frappe.qb.DocType("Stock Ledger Entry")
        sle_sql = (
            frappe.qb.from_(sle)
            .select(sle.name, sle.item_code)
            .where(sle.voucher_no == doc.name)
        ).run(as_dict=True)
        # update_stock_ledger(doc)
        for sle_name in sle_sql:
            frappe.db.set_value("Stock Ledger Entry", sle_name.name, "is_cancelled", 1)
            
        for sle_name in sle_sql:
            for i in doc.items:
                if not i.is_scrap_item and i.t_warehouse:
                    if i.item_code == sle_name.item_code:
                        frappe.db.set_value("Stock Ledger Entry", sle_name.name, "incoming_rate", i.basic_rate)
                
        for sle_name in sle_sql:
            frappe.db.set_value("Stock Ledger Entry", sle_name.name, "is_cancelled", 0)
        
        new_repost = frappe.new_doc("Repost Item Valuation")
        new_repost.based_on = "Transaction"
        new_repost.voucher_type = "Stock Entry"
        new_repost.voucher_no = doc.name
        new_repost.save()
        new_repost.submit()
        execute_repost()
        
        
        gle = frappe.qb.DocType("GL Entry")
        gle_sql = (
            frappe.qb.from_(gle)
            .select(gle.name)
            .where(gle.voucher_no == doc.name)
        ).run(as_dict=True)
        make_gl_entries(doc)
        for gle_name in gle_sql:
            frappe.db.set_value("GL Entry", gle_name.name, "is_cancelled", 1)
        
        
    return True


def execute_repost():
    """Execute repost item valuation via scheduler."""
    frappe.get_doc("Scheduled Job Type", "repost_item_valuation.repost_entries").enqueue(force=True)
    frappe.msgprint("Repost item valuation job has been successfully scheduled.", alert=True)