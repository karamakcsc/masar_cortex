# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	return columns(), data(filters)


def data(filters):
    conditions = " 1=1 "
    if filters.get("p_plan"):
        conditions += f" AND tpp.name = '{filters.get('p_plan')}'"
    if filters.get("item_code"):
        conditions += f" AND tppi.item_code = '{filters.get('item_code')}'"
    _from, to = filters.get("from"), filters.get("to")
    if _from and to:
        conditions += f" AND tpp.posting_date BETWEEN '{_from}' AND '{to}'"
    
    sql = frappe.db.sql(f"""
        SELECT
            tpp.name AS `Production Plan #`, 
            tpp.posting_date AS `Posting Date`,
            CASE WHEN tpp.status = 'Submitted' THEN 'Not Started' ELSE tpp.status END AS `Productio Plan Status`,
            CASE WHEN two.status = 'Draft' THEN 'Not Started' ELSE two.status END AS `Work Order Status`,
            tpp.total_planned_qty AS `Total Planned Qty`,
            tpp.total_produced_qty AS `Total Produced Qty`,
            tppi.item_code AS `Item Code`,
            tppi.custom_remarks AS `Remarks`,
            tppi.planned_qty AS `Planned Qty`,
            tppi.produced_qty AS `Produced Qty`,
            tppi.pending_qty AS `Pending Qty`,
            (IFNULL(two.produced_qty, 0) * IFNULL(ti.weight_per_unit, 0)) AS `Production Qty in Kg`,
            (IFNULL(two.process_loss_qty, 0) * IFNULL(ti.weight_per_unit, 0)) AS `Scrap in Kg`,
            IFNULL(two.planned_start_date, tppi.planned_start_date) AS `Planned Start Date`,
            two.actual_start_date AS `Actual Start Date`,
            two.actual_end_date AS `Actual End Date`
        FROM `tabProduction Plan` tpp
        INNER JOIN `tabProduction Plan Item` tppi  ON tppi.parent = tpp.name 
        LEFT JOIN `tabWork Order` two  ON tpp.name = two.production_plan AND tppi.name = two.production_plan_item AND two.docstatus IN (0, 1)
        LEFT JOIN `tabItem` ti ON ti.name = tppi.item_code
        WHERE {conditions} AND tpp.docstatus = 1 
	""")
    
    return sql

def columns():
    return[
         "Production Plan #:Link/Production Plan:250",
         "Posting Date:Date:200",
         "Productio Plan Status:Data:150",
         "Work Order Status:Data:150",
         "Total Planned Qty:Float:200",
         "Total Produced Qty:Float:200",
         "Item Code:Link/Item:200",
         "Remarks:Data:200",
         "Planned Qty:Float:150",
         "Produced Qty:Float:150",
         "Pending Qty:Float:150",
         "Production Qty in Kg:Float:200",
         "Scrap in Kg:Float:200",
         "Planned Start Date:Date:200",
         "Actual Start Date:Date:200",
         "Actual End Date:Date:200",
         
	]