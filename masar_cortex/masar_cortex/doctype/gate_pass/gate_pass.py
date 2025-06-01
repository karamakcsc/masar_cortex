# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GatePass(Document):
	def validate(self):
		self.validate_qty()
	def on_submit(self):
		self.validate_driver_details()
		self.update_delivered_qty()
	def on_cancel(self):
		self.return_delivered_qty()

	def validate_qty(self):
		if not self.dn_items:
			return

		dn_items_dict = {}
		dn_doc = frappe.get_doc("Delivery Note", self.delivery_note)
		for item in dn_doc.items:
			dn_items_dict[item.item_code] = item.qty
   
		for item in self.dn_items:
			if item.qty <= 0:
				frappe.throw(f"Quantity for item {item.item_code} must be greater than zero.")
			if item.item_code not in dn_items_dict:
				frappe.throw(f"Item {item.item_code} not found in the Delivery Note {self.delivery_note}.")
			available_qty = dn_items_dict[item.item_code]
			if item.qty > available_qty:
				frappe.throw(f"""Quantity for item {item.item_code} exceeds the quantity in Delivery Note {self.delivery_note}.
								Available quantity: {available_qty}, Requested quantity: {item.qty}""")
    
	def validate_driver_details(self):
		if not self.driver:
			frappe.throw("Driver details are required. Please add the driver.")
		if not self.plate_number:
			frappe.throw("Plate number is required. Please enter the plate number.")


	def update_delivered_qty(self):
		if not self.dn_items:
			frappe.throw("No items to update. Please fetch Delivery Note items first.")
		de_qty = 0
		for item in self.dn_items:
			if item.qty <= 0:
				frappe.throw(f"Quantity for item {item.item_code} must be greater than zero.")
			dn_doc = frappe.get_doc("Delivery Note Item", item.dn_name)
			remaining_qty = dn_doc.qty - dn_doc.custom_delivered_qty
			if item.qty > remaining_qty:
				frappe.throw(f"""Quantity for item {item.item_code} exceeds the available quantity in Delivery Note {self.delivery_note}.
								Available quantity: {remaining_qty}, Requested quantity: {item.qty}""")
			
			new_qty = dn_doc.custom_delivered_qty + item.qty
			de_qty += item.qty
			frappe.db.set_value("Delivery Note Item", item.dn_name, "custom_delivered_qty", new_qty)
		frappe.db.set_value("Delivery Note", self.delivery_note, "custom_delivered_qty", de_qty)
		frappe.db.commit()
		frappe.msgprint("Delivered quantities have been updated successfully.", alert=True, indicator='green')
			
	def return_delivered_qty(self):
		if not self.dn_items:
			frappe.throw("No items to reset. Please fetch Delivery Note items first.")
		de_qty = 0
		for item in self.dn_items:
			dn_doc = frappe.get_doc("Delivery Note Item", item.dn_name)
			new_qty = dn_doc.custom_delivered_qty - item.qty
			if new_qty < 0:
				new_qty = 0
			de_qty += new_qty
			frappe.db.set_value("Delivery Note Item", item.dn_name, "custom_delivered_qty", new_qty)
		frappe.db.set_value("Delivery Note", self.delivery_note, "custom_delivered_qty", de_qty)
		frappe.db.commit()
		frappe.msgprint("Delivered quantities have been reset to zero for all items in the Delivery Note.", alert=True, indicator='green')


	@frappe.whitelist()
	def get_dn_items(self):
		if not self.delivery_note:
			frappe.throw("Please select a Delivery Note to get items.")

		dn_items = frappe.db.sql("""
				SELECT
					tdni.item_code,
					tdni.item_name,
					tdni.qty - tdni.custom_delivered_qty AS qty,
					tdni.name AS dn_name
				FROM
					`tabDelivery Note Item` AS tdni
				WHERE
					tdni.parent = %s
					AND tdni.custom_delivered_qty != tdni.qty
			""", (self.delivery_note,), as_dict=True)
		if dn_items:
			return dn_items
		return False
