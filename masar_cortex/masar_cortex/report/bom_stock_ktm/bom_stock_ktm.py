# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder.functions import Floor, Sum, Coalesce
from frappe.utils import cint


def execute(filters=None):
    columns = get_columns()
    data = get_bom_stock(filters)
    return columns, data


def get_columns():
    return [
        {
            "fieldname": "item_code",
            "label": _("Item"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "fieldname": "item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
            "width": 240
        },
        {
            "fieldname": "description",
            "label": _("Description"),
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "bom_qty",
            "label": _("BOM Qty"),
            "fieldtype": "Float",
            "width": 160
        },
        {
            "fieldname": "stock_uom",
            "label": _("BOM UoM"),
            "fieldtype": "Data",
            "width": 160
        },
        {
            "fieldname": "required_qty",
            "label": _("Required Qty"),
            "fieldtype": "Float",
            "width": 120
        },
        {
            "fieldname": "in_stock_qty",
            "label": _("In Stock Qty"),
            "fieldtype": "Float",
            "width": 120
        },
        {
            "fieldname": "enough_parts_to_build",
            "label": _("Enough Parts to Build"),
            "fieldtype": "Float",
            "width": 200
        },
    ]


def get_bom_stock(filters):
    # Validate qty_to_produce
    qty_to_produce = cint(filters.get("qty_to_produce", 1))
    if qty_to_produce <= 0:
        frappe.throw(_("Quantity to Produce should be greater than zero."))

    # Determine BOM item table based on exploded view
    bom_item_table = (
        "BOM Explosion Item" if filters.get("show_exploded_view") else "BOM Item"
    )

    # Get warehouse details if warehouse filter is provided
    warehouse = filters.get("warehouse")
    warehouse_details = None
    if warehouse:
        warehouse_details = frappe.db.get_value(
            "Warehouse",
            warehouse,
            ["lft", "rgt"],
            as_dict=1,
        )

    # Define query builder tables
    BOM = frappe.qb.DocType("BOM")
    BOM_ITEM = frappe.qb.DocType(bom_item_table)
    BIN = frappe.qb.DocType("Bin")
    WH = frappe.qb.DocType("Warehouse")

    # Build stock subquery based on warehouse filter
    if warehouse_details:
        # Warehouse selected → sum under the warehouse tree
        bin_subquery = (
            frappe.qb.from_(BIN)
            .join(WH)
            .on(BIN.warehouse == WH.name)
            .select(
                BIN.item_code.as_("item_code"),
                Sum(BIN.actual_qty).as_("actual_qty"),
            )
            .where(
                (WH.lft >= warehouse_details.lft)
                & (WH.rgt <= warehouse_details.rgt)
            )
            .groupby(BIN.item_code)
        )
    else:
        # No warehouse selected → sum all warehouses
        bin_subquery = (
            frappe.qb.from_(BIN)
            .select(
                BIN.item_code.as_("item_code"),
                Sum(BIN.actual_qty).as_("actual_qty"),
            )
            .groupby(BIN.item_code)
        )

    # Build main query
    query = (
        frappe.qb.from_(BOM)
        .join(BOM_ITEM)
        .on(BOM.name == BOM_ITEM.parent)
        .left_join(bin_subquery)
        .on(BOM_ITEM.item_code == bin_subquery.item_code)
        .select(
            BOM_ITEM.item_code.as_("item_code"),
            BOM_ITEM.item_name.as_("item_name"),
            BOM_ITEM.description.as_("description"),
            Sum(BOM_ITEM.stock_qty).as_("bom_qty"),
            BOM_ITEM.stock_uom.as_("stock_uom"),
            ((Sum(BOM_ITEM.stock_qty) * qty_to_produce) / BOM.quantity).as_("required_qty"),
            Coalesce(bin_subquery.actual_qty, 0).as_("in_stock_qty"),
            Floor(
                Coalesce(bin_subquery.actual_qty, 0)
                / (
                    (Sum(BOM_ITEM.stock_qty) * qty_to_produce)
                    / BOM.quantity
                )
            ).as_("enough_parts_to_build"),
        )
        .where(BOM_ITEM.parenttype == "BOM")
        .groupby(
            BOM_ITEM.item_code, 
            BOM_ITEM.item_name, 
            BOM_ITEM.description, 
            BOM_ITEM.stock_uom,
            bin_subquery.actual_qty
        )
    )

    # Apply BOM filter if provided
    if filters.get("bom"):
        query = query.where(BOM.name == filters.get("bom"))
    
    # Apply Item Code filter if provided
    if filters.get("item_code"):
        query = query.where(BOM_ITEM.item_code == filters.get("item_code"))

    # Execute query and return results
    return query.run(as_dict=True)