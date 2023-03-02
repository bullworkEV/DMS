// Copyright (c) 2016, xyz and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item dms', {

                     validate: function(frm) {

                                           if(frm.doc.cat_name){
                                                        frm.doc.item_name = frm.doc.cat_name;
                                                        $.each(frm.doc.item_character,function(i,  d) {
                                                        frm.doc.item_name += ' '+ d.attribute_value_both;
                                                        });
                                                     }
                                          if(frm.doc.maintain_attribute && frm.doc.__islocal==1){
                                            frappe.call({
                                                      method: "frappe.client.get_value",
                                                        args: {
                                                                 doctype: "Item",
                                                                 filters: [["item_name","=",frm.doc.item_name]],
                                                               fieldname: ["item_name","item_code"]
                                                           },

                                                      callback: function(r) {
                                                                
                                                                console.log(r.message);
                                                                msgprint(r.message.item_name);
                                                                msgprint(r.message.item_code);

                                                                if (r.message.item_name){
                                                msgprint('Material with this name already exist in Prodn. Cannot Save..');
                                                            validated = false;
                                                                                }
                                                      }
                                                 });

                                            frappe.call({
                                                  method: "frappe.client.get_value",
                                                    args: {
                                                             doctype: "Item dms",
                                                             filters: [["item_name","=",frm.doc.item_name]],
                                                           fieldname: ["item_name","item_code"]
                                                       },

                                                  callback: function(r) {
                                                            
                                                            console.log(r.message);
                                                            msgprint(r.message.item_name);
                                                            msgprint(r.message.item_code);

                                                            if (r.message.item_name){
                                            msgprint('Material with this name already exist in DMS. Cannot Save..');
                                                        validated = false;
                                                                            }
                                                  }
                                             });
                                            }
                                        },

                      cat_name: function(frm){

                                let cat_name = frm.doc.cat_name;

                                frappe.call({
                                       method: "dms.dms.doctype.item_dms.item_dms.get_attribute_category",
                                         args: {'cat_name':cat_name},
                                     callback: function(r){
                                      
                                          $.each(r.message, function(i, r){
                                          
                                          frm.add_child('item_character',{attribute: r.attribute,attribute_of:cat_name});
                                          frm.refresh_field('item_character')
  
                                             }) 
                                            },
                                        });

                                   },

                          attribute: function(frm,cdt,cdn) {
                               
                                  },




                   before_save: function(frm) {
		                                           if(frm.doc.cat_name){
                                                        frm.doc.item_name = frm.doc.cat_name;
                                                        $.each(frm.doc.item_character,function(i,  d) {
                                                        frm.doc.item_name += ' '+ d.attribute_value_both;
                                                        });
                                                     }
                                                
            
	                                },

                       refresh: function(frm,cdt,cdn) {
		                                          if (!frm.doc.trf_prodn && !frm.doc.__islocal) {
                                                  frm.add_custom_button(__("Transfer Item to Prodn"), function() {
		                                              var itemx = frappe.model.get_doc(cdt,cdn);
                                                  msgprint("M" + itemx.item_name);
                                                  msgprint("M" + itemx.item_code);
                                                  msgprint("M" + itemx.name);
                                                 frappe.call({
                                                      method: "frappe.client.get_value",
                                                        args: {
                                                                 doctype: "Item",
                                                                 filters: [["item_name","=",itemx.item_name]],
                                                               fieldname: ["item_name","item_code"]
                                                           },

                                                      callback: function(r) {
                                                                msgprint("Message_1");
                                                                console.log(r.message);
                                                                msgprint(r.message.item_name);
                                                                msgprint(r.message.item_code);

                                                                if (!r.message.item_name){
                      
                                                                         frappe.call({
                                                                            url: "/api/resource/Item/",
                                                                           type: "post",
                                                                           args: {
                                                                             data: {
                                                                                    "item_code" : itemx.name,
                                                                                    "item_name" : itemx.item_name,
                                                                                           "uom": itemx.uom,
                                                                                    "item_group":itemx.item_group,
                                                                                   "description":itemx.description,
                                                                                  "manufacturer":itemx.manufacturer,
                                                                        "manufacturer_part_no":itemx.manufacturer_part_no
                                                                                }
                                                                             },
                                                                          callback: function(r1) {
                                                                                   console.log(JSON.stringfy(r1));
                                                                                   msgprint(r1.message.item_code);
                                                                                         }
                                                                                     });
                                                                           frm.set_value({trf_prodn : 1});
                                                                         //frm.set_value({item_code : r.message.item_code});
                                                                          frm.save();
                                                                              }
                                                                          }
                                                                     });
                                                        msgprint(frm.doc.trf_prodn);

		                                                            });
                                                            } 
                                              // let d1 = frappe.get_doc(cdt,cdn);
                                                  //msgprint(d1.attribute);
                                                frm.set_query('attribute_value','item_character',
                                                       function(frm,cdt,cdn) {

                                                      let  d = frappe.get_doc(cdt,cdn);
                                                     // msgprint(d.attribute);
                                                      return{
                                             query: 'dms.dms.doctype.item_dms.item_dms.query_attribute',
                                          doctype : 'Item character',
                                            txt   : '',
                                        searchfield: '',
                                          start   : '',
                                          page_len: '',
                                          
                                          filters : {
                                                     'attribute' : d.attribute
                                                                          }
                                                            
                                                                   }
                                                         });   
	                                                    }
                                });

frappe.ui.form.on('Item character attribute', {
                           attribute_value:function(frm,cdt,cdn){
                             let row = frappe.get_doc(cdt,cdn);
                           /*   var attrx = frappe.call({
                              method: "frappe.db.get_list",
                                args: {
                                         doctype: "Item character value",
                                         filters: [["character_value","=",'Aluminium']],
                                       fields: ["abbr"]
                                   },

                              callback: function(r) {
                                        msgprint("Message_1");
                                        console.log(r.message);
                                        msgprint(r.message.abbr);
                                    }
                            })    */
                            
                            row.attribute_value_both = row.attribute_value;
                           frm.set_df_property('attribute_value_both',  'read_only',  !frm.doc.attribute_value ? 0 : 1);
                                                             }

   
                 
	                                         });
