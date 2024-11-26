import frappe 

def on_submit(self , method):
    if self.custom_has_git:
        add_git_code(self)

def add_git_code(self):
    for i in self.items: 
        if i.purchase_order is not None : 
            po_doc = frappe.get_doc('Purchase Order' , i.purchase_order)
            if po_doc.custom_git_no is None: 
                po_doc.custom_git_no = self.custom_git_no
                po_doc.custom_has_git =1 
                po_doc.run_method('save')
                frappe.db.set_value('Purchase Order' , i.purchase_order , 'custom_has_git' ,1)
                frappe.db.set_value('Purchase Order' , i.purchase_order , 'custom_git_no' ,self.custom_git_no)
            if i.serial_and_batch_bundle: 
                sbb = frappe.get_doc('Serial and Batch Bundle' , i.serial_and_batch_bundle)
                for e in sbb.entries:
                    if e.batch_no :
                        batch_doc = frappe.get_doc('Batch' , e.batch_no )
                        batch_doc.custom_git_no = self.custom_git_no
                        frappe.db.set_value('Batch' ,e.batch_no , 'custom_git_no' , self.custom_git_no)
                            