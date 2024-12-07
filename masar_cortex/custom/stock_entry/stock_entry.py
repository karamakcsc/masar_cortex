import frappe

def validate(self, method):
    validate_qty(self)
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


def validate_qty(self):
    if self.stock_entry_type == "Repack":
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