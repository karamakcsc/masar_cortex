# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	return columns(), data(filters)


def data(filters):
    conditions = " 1=1 "
    if filters.get("p_plan"):
        conditions += f" AND tpp.name = '{filters.get("p_plan")}'"
    if filters.get("item_code"):
        conditions += f" AND tppi.item_code = '{filters.get("item_code")}'"
    
    sql = frappe.db.sql(f"""
        SELECT
			tpp.name AS `Production Plan #`, 
			tpp.company AS `Company`,
			CASE WHEN tpp.status = 'Submitted' THEN 'Not Started' ELSE tpp.status END AS `Status`,
			tppi.item_code AS `Item Code`,
			tppi.custom_remarks AS `Remarks`,
			tppi.planned_qty AS `Planned Qty`,
			IFNULL(two.planned_start_date, tppi.planned_start_date) AS `Planned Start Date`,
			two.actual_start_date AS `Actual Start Date`,
			two.actual_end_date AS `Actual End Date`
		FROM `tabProduction Plan` tpp
		INNER JOIN `tabProduction Plan Item` tppi  ON tppi.parent = tpp.name 
		LEFT JOIN `tabWork Order` two  ON tpp.name = two.production_plan AND tppi.name = two.production_plan_item AND two.docstatus = 1
		WHERE {conditions} AND tpp.docstatus = 1 
	""")
    
    return sql

def columns():
    return[
         "Production Plan #:Link/Production Plan:300",
         "Company:Link/Company:300",
         "Status:Data:200",
         "Item Code:Link/Item:200",
         "Remarks:Data:200",
         "Planned Qty:Float:200",
         "Planned Start Date:Date:300",
         "Actual Start Date:Date:300",
         "Actual End Date:Date:300",
         
	]