import frappe
from frappe.utils import nowdate, get_formatted_email
from frappe import _, msgprint
from frappe.utils.user import get_users_with_role

def validate(self, method):
    validate_checkbox(self)
    validate_actual_qty(self)
def on_submit(self, method):
    validate_overdue_limit(self)

        
def validate_actual_qty(self):
    if self.items:
        for item in self.items:
            if item.qty > item.custom_available_qty or item.custom_available_qty < 0:
                frappe.throw(f"Available quantity for item {item.item_code} is less than the requested quantity.")
                
def validate_checkbox(self):
    if not self.custom_do and not self.custom_invoice:
        frappe.throw("Please select either 'Do' or 'Invoice'.")
    if self.custom_do and self.custom_invoice:
        frappe.throw("Please select either 'Do' or 'Invoice'. Both cannot be selected at the same time.")
                
@frappe.whitelist()            
def available_qty_sql(item, warehouse):
    if item:
        sql = frappe.db.sql("""
                             SELECT (bi.actual_qty - bi.reserved_qty) AS available_qty 
                             FROM tabBin bi 
                             WHERE bi.item_code = %s AND bi.warehouse = %s
                             """, (item, warehouse, ), as_dict=True)
        
        if sql and sql[0] and sql[0]['available_qty']:
            return sql[0]['available_qty']
        else:
            return 0
        
def validate_overdue_limit(self):
    if self.customer:
        overdue_amount = get_customer_overdue_amount(self.customer)
        customer_doc = frappe.get_doc("Customer", self.customer)
        if customer_doc.credit_limits:
            for limit in customer_doc.credit_limits:
                if limit.custom_bypass_overdue_check:
                    continue
                if limit.custom_overdue_limit and limit.custom_overdue_limit > 0:
                    if overdue_amount > limit.custom_overdue_limit:
                        message = _("Overdue limit has been crossed for customer {0} ({1}/{2})").format(
                            self.customer, overdue_amount, limit.custom_overdue_limit
                        )

                        message += "<br><br>"

                        # If not authorized person raise exception
                        credit_controller_role = frappe.db.get_single_value("Accounts Settings", "credit_controller")
                        if not credit_controller_role or credit_controller_role not in frappe.get_roles():
                            # form a list of emails for the credit controller users
                            credit_controller_users = get_users_with_role(credit_controller_role or "Sales Master Manager")

                            # form a list of emails and names to show to the user
                            credit_controller_users_formatted = [
                                get_formatted_email(user).replace("<", "(").replace(">", ")")
                                for user in credit_controller_users
                            ]
                            if not credit_controller_users_formatted:
                                frappe.throw(
                                    _("Please contact your administrator to extend the credit limits for {0}.").format(
                                        self.customer
                                    )
                                )

                            user_list = "<br><br><ul><li>{}</li></ul>".format("<li>".join(credit_controller_users_formatted))

                            message += _(
                                "Please contact any of the following users to extend the credit limits for {0}: {1}"
                            ).format(self.customer, user_list)

                            # if the current user does not have permissions to override credit limit,
                            # prompt them to send out an email to the controller users
                            frappe.msgprint(
                                message,
                                title=_("Overdue Limit Crossed"),
                                raise_exception=1,
                                primary_action={
                                    "label": "Send Email",
                                    "server_action": "erpnext.selling.doctype.customer.customer.send_emails",
                                    "hide_on_success": True,
                                    "args": {
                                        "customer": self.customer,
                                        "customer_outstanding": overdue_amount,
                                        "credit_limit": limit.custom_overdue_limit,
                                        "credit_controller_users_list": credit_controller_users,
                                    },
                                },
                            )

def get_customer_overdue_amount(customer):
    overdue = frappe.db.sql("""
        SELECT SUM(outstanding_amount) 
        FROM `tabSales Invoice`
        WHERE customer=%s 
          AND docstatus=1
          AND outstanding_amount > 0
          AND due_date < %s
    """, (customer, nowdate()))[0][0] or 0
    return overdue