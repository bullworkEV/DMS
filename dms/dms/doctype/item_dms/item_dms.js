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
 });

  },

   refresh: function(frm) {
           frm.set_query('attribute_value','item_character',
                                   function(doc,cdt,cdn) {

                       var d = locals[cdt][cdn];
                        return{
                              query: 'dms.dms.doctype.item_dms.item_dms.query_attribute',
                              filters : {
                                     'attribute' : d.attribute
                                       }
                                                            
                            }
                           });
                },

    before_save: function(frm) {
		 //let row = frappe.get_doc(cdt,cdn);
        //var row = locals['Item character attribute'][cdn];
        //frappe.model.set_value(d.doctype, d.name, 'attribute_value_both', (d.attribute_value));
        if(frm.doc.cat_name){
        frm.doc.item_name = frm.doc.cat_name;
        $.each(frm.doc.item_character,function(i,  d) {
         frm.doc.item_name += ' '+ d.attribute_value_both;
        //msgprint("Message6" +frm.doc.item_name);
    });
           }
        //msgprint("Message5" +frm.doc.item_name);
    
	},

  refresh: function(frm,cdt,cdn) {
		 if (!frm.doc.trf_prodn && !frm.doc.__islocal) {
                 frm.add_custom_button(__("Transfer Item to Prodn"), function() {
		//	frappe.set_route("List", "Item Price", {"item_code": frm.doc.name});
                 var itemx = frappe.model.get_doc(cdt,cdn);
                 msgprint("M" + itemx.item_name);
                 frappe.call({
                              url: "/api/resource/Item/",
                              type: "post",
                              args: {
                                  data: {"item_name" : itemx.item_name,
                                                "uom": itemx.uom,
                                          "item_group":itemx.item_group,
                                          "description":itemx.description,
                                         "manufacturer":itemx.manufacturer,
                                 "manufacturer_part_no":itemx.manufacturer_part_no
                                       }

                                    },
                              callback: function(r) {
                                        console.log(JSON.stringfy(r));
                              $.each(r.message, function(i, r){
                               msgprint(r.item_code);
                                        })    
                                  }
                            });
                 frm.set_value({trf_prodn : 1});
                 frm.save();
                 msgprint(frm.doc.trf_prodn);

		});
           }
	}

});


frappe.ui.form.on('Item character attribute', {
	attribute_value:function(frm,cdt,cdn){
        
       let row = frappe.get_doc(cdt,cdn);
       //msgprint("message"+row.attribute_value);
       row.attribute_value_both = row.attribute_value
       //msgprint(row);
       frm.set_df_property('attribute_value_both',  'read_only',  !frm.doc.attribute_value ? 0 : 1);
       
        } 
	
});
