import frappe
import json
from erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool import get_account_balance


@frappe.whitelist()
def save_bank_reconciliation_tool(self):
    self = json.loads(self)
    closing_balance = get_account_balance(self.get("bank_account"), self.get("bank_statement_to_date"), self.get("company"))
    
    new_brh = frappe.new_doc("Bank Reconciliation History")
    new_brh.bank_account = self.get("bank_account")
    new_brh.from_date = self.get("bank_statement_from_date")
    new_brh.to_date = self.get("bank_statement_to_date")
    new_brh.company = self.get("company")
    new_brh.filter_by_reference_date = self.get("filter_by_reference_date")
    new_brh.account_opening_balance = self.get("account_opening_balance")
    new_brh.from_reference_date = self.get("from_reference_date")
    new_brh.to_reference_date = self.get("to_reference_date")
    new_brh.closing_balance_erp = closing_balance
    new_brh.closing_balance_bs = self.get("bank_statement_closing_balance")
    new_brh.bank_statement_closing_balance = self.get("bank_statement_closing_balance")
    new_brh.difference = closing_balance - self.get("bank_statement_closing_balance")
    
    new_brh.save(ignore_permissions=True)
    new_brh.submit()
    
    return new_brh.name