###
import frappe 

def validate(self , method):
    get_git_no(self, method)
    
def get_git_no(self , method): 
    if (self.reference_doctype == 'Purchase Receipt') and (self.reference_name is not None ) :
        pr = frappe.get_doc('Purchase Receipt' , self.reference_name)
        if pr.custom_git_no: 
            self.custom_git_no = pr.custom_git_no
    sql = frappe.db.sql("""
            SELECT 
                tia.attribute_value as thickness
            FROM 
                tabItem ti
            INNER JOIN 
                `tabItem Variant Attribute` tia ON ti.name = tia.parent 
            WHERE 
                LOWER(tia.`attribute`) LIKE %s
            AND ti.name = %s
            """, ('%thickness%',self.item),as_dict = True)
    if sql and sql[0] and sql[0]['thickness']: 
        self.custom_thickness = sql[0]['thickness']