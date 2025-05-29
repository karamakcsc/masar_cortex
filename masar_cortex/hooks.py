app_name = "masar_cortex"
app_title = "Masar Cortex"
app_publisher = "KCSC"
app_description = "Masar Cortex"
app_email = "info@kcsc.com.jo"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "masar_cortex",
# 		"logo": "/assets/masar_cortex/logo.png",
# 		"title": "Masar Cortex",
# 		"route": "/masar_cortex",
# 		"has_permission": "masar_cortex.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/masar_cortex/css/masar_cortex.css"
# app_include_js = "/assets/masar_cortex/js/masar_cortex.js"

# include js, css files in header of web template
# web_include_css = "/assets/masar_cortex/css/masar_cortex.css"
# web_include_js = "/assets/masar_cortex/js/masar_cortex.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "masar_cortex/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Stock Entry" : "custom/stock_entry/stock_entry.js",
    "Sales Order" : "custom/sales_order/sales_order.js",
    "Item Group" : "custom/item_group/item_group.js",
    "Delivery Note" : "custom/delivery_note/delivery_note.js"
    }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "masar_cortex/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "masar_cortex.utils.jinja_methods",
# 	"filters": "masar_cortex.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "masar_cortex.install.before_install"
# after_install = "masar_cortex.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "masar_cortex.uninstall.before_uninstall"
# after_uninstall = "masar_cortex.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "masar_cortex.utils.before_app_install"
# after_app_install = "masar_cortex.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "masar_cortex.utils.before_app_uninstall"
# after_app_uninstall = "masar_cortex.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "masar_cortex.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Purchase Receipt": {
		"on_submit": "masar_cortex.custom.purchase_receipt.purchase_receipt.on_submit"
	},
    "Stock Entry": {
        "validate": "masar_cortex.custom.stock_entry.stock_entry.validate",
        # "validate": "masar_cortex.custom.stock_entry.stock_entry.on_submit"
    },
    "Batch": {
        "before_naming" :  "masar_cortex.custom.batch.batch.get_git_no",
    },
    "Sales Order": {
        "validate": "masar_cortex.custom.sales_order.sales_order.validate",
    },
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"masar_cortex.tasks.all"
# 	],
	# "daily": [
	# 	# "masar_cortex.jobs._repost_item_valuation.repost_stock_entry",
    #     "masar_cortex.jobs.update_so_status.update_so_status"
	# ],
	# "hourly": [
	# 	"masar_cortex.jobs._repost_item_valuation.repost_stock_entry"
	# ],
	"weekly": [
		"masar_cortex.jobs._repost_item_valuation.repost_stock_entry"
	],
# 	"monthly": [
# 		"masar_cortex.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "masar_cortex.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "masar_cortex.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "masar_cortex.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["masar_cortex.utils.before_request"]
# after_request = ["masar_cortex.utils.after_request"]

# Job Events
# ----------
# before_job = ["masar_cortex.utils.before_job"]
# after_job = ["masar_cortex.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"masar_cortex.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
fixtures = [
    {"dt": "Custom Field", "filters": [
        [
            "name", "in", [
                    "Purchase Receipt-custom_has_git", 
                    "Purchase Receipt-custom_git_no",
                    "Purchase Order-custom_has_git",
                    "Purchase Order-custom_git_no", 
                    "Batch-custom_git_no",
                    "Purchase Receipt Item-custom_gross_weight",
                    "Batch-custom_gross_weight",
                    "Batch-custom_thickness",
                    "Stock Entry Detail-custom_weight_per_unit",
                    "Stock Entry Detail-custom_weight_uom",
                    "Sales Order Item-custom_available_qty",
                    "Item Group-custom_rate_kg",
                    "Item Group-custom_update_item_price",
                    "Item-custom_theoretical_wpu",
                    "Delivery Note Item-custom_delivered_qty",
                    "Delivery Note-custom_delivered_qty",
                    "Production Plan-custom_remarks",
                    "Stock Entry-custom_total_qty_difference",
                    "Stock Entry-custom_total_outgoing_qty_kg",
                    "Stock Entry-custom_total_incoming_qty_kg",
                    "Stock Entry-custom_section_break_wgdbv",
                    "Stock Entry-custom_column_break_r87kr"
            ]
        ]
    ]},
    {
        "doctype": "Property Setter",
        "filters": [
            [
                "name",
                "in",
                [
                    "Purchase Receipt Item-net_amount-hidden",
                    "Purchase Receipt Item-main-field_order",
                    "Purchase Receipt Item-from_warehouse-hidden",
                    "Purchase Receipt Item-barcode-hidden",
                    "Purchase Receipt Item-base_rate-permlevel",
                    "Purchase Receipt Item-billed_amt-hidden",
                    "Purchase Receipt Item-rate_difference_with_purchase_invoice-hidden",
                    "Purchase Receipt Item-landed_cost_voucher_amount-hidden",
                    "Purchase Receipt Item-base_net_amount-hidden",
                    "Purchase Receipt Item-base_net_rate-hidden",
                    "Purchase Receipt Item-net_rate-hidden",
                    "Purchase Receipt Item-stock_uom_rate-hidden",
                    "Purchase Receipt Item-base_amount-hidden",
                    "Purchase Receipt Item-amount-hidden",
                    "Purchase Receipt Item-rate-hidden",
                    "Purchase Receipt Item-base_rate_with_margin-hidden",
                    "Purchase Receipt Item-discount_amount-hidden",
                    "Purchase Receipt Item-rate_with_margin-hidden",
                    "Purchase Receipt Item-base_price_list_rate-hidden",
                    "Purchase Receipt Item-price_list_rate-hidden",
                    "Batch-batch_id-reqd",
                    "Batch-main-field_order",
                    "Stock Entry Detail-basic_amount-allow_on_submit",
                    "Stock Entry Detail-valuation_rate-allow_on_submit",
                    "Stock Entry Detail-amount-allow_on_submit",
                    "Stock Entry Detail-basic_rate-allow_on_submit",
                    "Stock Entry Detail-additional_cost-allow_on_submit",
                    "Stock Entry Detail-is_scrap_item-allow_on_submit",
                    "Stock Entry Detail-is_finished_item-allow_on_submit",
                    "Delivery Note Item-base_amount-permlevel",
                    "Delivery Note Item-base_rate-permlevel",
                    "Delivery Note Item-amount-permlevel",
                    "Delivery Note Item-rate-permlevel"
                ]
            ]
        ]
    }
]
