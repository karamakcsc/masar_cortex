# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe
import pandas as pd
from io import BytesIO
from frappe.utils.file_manager import get_file
from frappe.model.document import Document


class BulkItemPriceUpdate(Document):
    def validate(self):
        self.fetch_items()
        self.set_available_qty()
        
    def on_submit(self):
        self.update_item_price()
        

    def set_available_qty(self):
        if self.items:
            for item in self.items:
                available_qty = available_qty_sql(item.item_code)
                item.available_qty = available_qty if available_qty else 0
    
    def fetch_items(self):
        if self.via_excel:
            return
        
        if not self.item_group and not self.brand and not self.supplier and not self.items:
            return
        
        if self.items:
            for row in self.items:
                if not row.price_list:
                    row.price_list = self.default_price_list or ''
                if not row.rate_per_kg:
                    row.rate_per_kg = self.default_rate_per_kg or 0
            return
        
        self.items = []
  
        conditions = '1=1'
        if self.item_group:
            conditions += f' AND ti.item_group = "{self.item_group}"'
        if self.brand:
            conditions += f' AND ti.brand = "{self.brand}"'
        if self.supplier:
            conditions += f' AND tip.supplier = "{self.supplier}"'

        items_sql = frappe.db.sql(f"""
            SELECT
                ti.name AS item_code,
                ti.item_name,
                ti.item_group,
                tip.price_list_rate,
                ti.brand,
                tip.price_list,
                ti.stock_uom,
                (tb.actual_qty - tb.reserved_qty) AS available_qty,
                ti.weight_per_unit AS wpu,
                ti.custom_theoretical_wpu,
                tip.name AS item_price_ref
            FROM tabItem ti
            LEFT JOIN (
                SELECT ip.item_code, ip.price_list_rate, ip.price_list, ip.uom, ip.supplier, ip.modified, ip.name
                FROM `tabItem Price` ip
                INNER JOIN (
                    SELECT item_code, MAX(modified) AS latest_modified
                    FROM `tabItem Price`
                    WHERE selling = 1
                    GROUP BY item_code
                ) latest_ip ON ip.item_code = latest_ip.item_code AND ip.modified = latest_ip.latest_modified
                WHERE ip.selling = 1
            ) tip ON tip.item_code = ti.name
            LEFT JOIN `tabBin` tb ON tb.item_code = ti.name AND tb.warehouse = 'Finished Goods Store - CKTM'
            WHERE {conditions} AND ti.has_variants = 0
        """, as_dict=True)
        
        if items_sql:
            for item in items_sql:
                self.append('items', {
                    "item_code": item.item_code,
                    "item_name": item.item_name,
                    "item_group": item.item_group,
                    "wpu": item.wpu or 0,
                    "weight_per_unit": item.custom_theoretical_wpu or 0,
                    "rate_per_kg": self.default_rate_per_kg or 0,
                    "old_price": item.price_list_rate or 0,
                    "brand": item.brand,
                    "price_list": item.price_list or self.default_price_list or '',
                    "uom": item.stock_uom or '',
                    "available_qty": item.available_qty or 0,
                    "item_price_ref": item.item_price_ref or '',
                })

    def update_item_price(self):
        if self.via_excel and self.attach:
            self.update_from_excel()
        elif self.items:
            for item in self.items:
                if not item.uom or not item.price_list:
                    frappe.throw(f"Item {item.item_code} in row {item.idx} is missing UOM or Price List.")
                if not item.weight_per_unit:
                    frappe.throw(f"Item {item.item_code} in row {item.idx} is missing weight per unit.")
                if not item.rate_per_kg:
                    frappe.throw(f"Item {item.item_code} in row {item.idx} is missing rate per kg.")
                if not item.new_price:
                    frappe.throw(f"Item {item.item_code} in row {item.idx} is missing new price.")
                existing_price = frappe.db.sql("""
                    SELECT name FROM `tabItem Price`
                    WHERE item_code = %s AND uom = %s AND price_list = %s AND selling = 1
                    ORDER BY modified DESC LIMIT 1
                """, (item.item_code, item.uom, item.price_list), as_dict=True)
                existing_price = existing_price[0]['name'] if existing_price else None
                if existing_price:
                    # frappe.db.set_value("Item Price", item.item_price_ref, "price_list_rate", item.new_price)
                    item_price_doc = frappe.get_doc("Item Price", existing_price)
                    item_price_doc.price_list_rate = item.new_price
                    item_price_doc.save(ignore_permissions=True)
                elif not item.old_price and item.new_price:
                    new_item_price = frappe.new_doc("Item Price")
                    new_item_price.item_code = item.item_code
                    new_item_price.uom = item.uom
                    new_item_price.price_list = item.price_list
                    new_item_price.price_list_rate = item.new_price
                    new_item_price.valid_from = frappe.utils.nowdate()
                    new_item_price.save(ignore_permissions=True)
        frappe.msgprint("Item prices updated successfully.", alert=True, indicator='green')
                    
    def update_from_excel(self):
        file_url = self.attach
        if not file_url:
            frappe.throw("No Excel file attached.")

        _, file_path = get_file(file_url)
        df = pd.read_excel(BytesIO(file_path), engine='openpyxl')

        required_columns = {"Item Code", "Rate", "UOM", "Price List"}
        if not required_columns.issubset(set(df.columns)):
            frappe.throw(f"Excel must contain columns: {', '.join(required_columns)}")

        for _, row in df.iterrows():
            item_code = row["Item Code"]
            new_price = row["Rate"]
            uom = row["UOM"]
            price_list = row["Price List"]

            existing_price = frappe.db.get_value("Item Price", {
                "item_code": item_code,
                "uom": uom,
                "price_list": price_list,
                "selling": 1
            }, ["name"])
            if existing_price:
                # frappe.db.set_value("Item Price", existing_price, "price_list_rate", new_price)
                item_price_doc = frappe.get_doc("Item Price", existing_price)
                item_price_doc.price_list_rate = new_price
                item_price_doc.save(ignore_permissions=True)
            else:
                new_item_price = frappe.new_doc("Item Price")
                new_item_price.item_code = item_code
                new_item_price.uom = uom
                new_item_price.price_list = price_list
                new_item_price.price_list_rate = new_price
                new_item_price.valid_from = frappe.utils.nowdate()
                new_item_price.selling = 1
                new_item_price.save(ignore_permissions=True)

@frappe.whitelist()
def available_qty_sql(item):
    if item:
        warehouse = 'Finished Goods Store - MSCD'
        sql = frappe.db.sql("""
            SELECT (COALESCE(bi.actual_qty, 0) - COALESCE(bi.reserved_qty, 0)) AS available_qty
            FROM tabBin bi
            WHERE bi.item_code = %s AND bi.warehouse = %s
        """, (item, warehouse), as_dict=True)
        if sql and sql[0] and sql[0]['available_qty'] is not None:
            return sql[0]['available_qty']
        else:
            return 0