// Copyright (c) 2016, xyz and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item dms', {

  cat_name: function(frm){

  let cat_name = frm.doc.cat_name;

//    frm.doc.cat_name=;

//    frm.add_child('item_character',{attribute: 'Shape'});
//    frm.refresh_field('item_character')
    frappe.call({
     method: "dms.dms.doctype.item_dms.item_dms.get_attribute_category",
     args: {'cat_name':cat_name},
     callback: function(r){
    //   frm.doc.item_character = []
//   msgprint('not passing records'+r.message+cat_name)   
   $.each(r.message, function(i, r){
       frm.add_child('item_character',{attribute: r.attribute,attribute_of:cat_name});
       frm.refresh_field('item_character')
//       msgprint('not passing records'+r.attribute+cat_name)   

    }) 
   },
 })

  }

//   refresh(frm) {
//           frm.set_query('attribute_value','item_character',
//                                   function(doc,cdt,cdn) {

//                       var d = locals[cdt][cdn];
//                        return{
//                              " filters": {
//                                     "attribute" : d.attribute
//                                       }
//                              };
//                           });
//                }

});
