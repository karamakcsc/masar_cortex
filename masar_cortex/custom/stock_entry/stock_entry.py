import frappe

def validate(self, method):
    validate_qty(self)
    calc_cost_qty(self)
    

def calc_cost_qty(self):
    if self.stock_entry_type == "Repack":
        total_raw_material_cost = 0
        total_finished_qty = 0

        # Calculate total raw material cost and total finished goods quantity
        for item in self.items:
            if not item.is_finished_item and not item.is_scrap_item and item.s_warehouse:
                total_raw_material_cost += item.basic_rate * item.qty

            if item.is_finished_item and not item.is_scrap_item and item.t_warehouse:
                total_finished_qty += item.qty

        # Validate that raw material cost and finished goods quantity are defined
        if total_raw_material_cost == 0:
            frappe.throw("Total raw material cost is zero. Please ensure raw materials are properly defined.")
        if total_finished_qty == 0:
            frappe.throw("Total finished goods quantity is zero. Please ensure finished goods are properly defined.")

        # Distribute costs across finished goods
        for item in self.items:
            if item.is_finished_item and not item.is_scrap_item and item.t_warehouse:
                # Calculate percentage of this finished item's quantity
                percentage = item.qty / total_finished_qty
                cost_per_unit = (total_raw_material_cost * percentage) / item.qty

                # Update Basic Rate and Amount
                # item.basic_rate = cost_per_unit
                amount = cost_per_unit * item.qty
                frappe.db.set_value("Stock Entry Detail", item.name, "valuation_rate", cost_per_unit)
                frappe.db.set_value("Stock Entry Detail", item.name, "basic_rate", cost_per_unit)
                frappe.db.set_value("Stock Entry Detail", item.name, "amount", amount)
        # self.reload()
        # Add a comment to the document
        # frappe.msgprint("Costs have been successfully distributed across finished goods.")



def validate_qty(self):
    if self.stock_entry_type == "Repack":
        total_target_qty = 0
        total_source_qty = 0

        for item in self.items:
            if item.s_warehouse:
                total_source_qty += item.qty
                                
            if item.t_warehouse:
                total_target_qty += item.qty
                     
        if total_target_qty != total_source_qty:
            frappe.throw("Input Quantity Does Not Equal The Output Quantity.")            