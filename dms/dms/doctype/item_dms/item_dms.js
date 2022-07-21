// Copyright (c) 2016, xyz and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item dms', {

  refresh: function(frm){

  let cat_name = frm.doc.cat_name;

   if(cat_name){
    frappe.call({
     method: "dms.dms.doctype.item_dms.item_dms.get_attribute_category",
     args: {cat_name: cat_name}
    }).then(records => {

   frm.doc.item_character = []

   $.each(records, function(i, r){
       frm.add_child("item_character",{attribute: r.attribute});
   })
 })

}
  }
});
