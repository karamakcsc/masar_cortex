###
import frappe 

def validate(self , method):
    get_git_no(self, method)
    
def get_git_no(self , method): 
    if (self.reference_doctype == 'Purchase Receipt') and (self.reference_name is not None ) :
        pr = frappe.get_doc('Purchase Receipt' , self.reference_name)
        if pr.custom_git_no: 
            self.custom_git_no = pr.custom_git_no