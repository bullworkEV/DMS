// Copyright (c) 2016, xyz and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item dms', {

                     validate: function(frm) {

                                           if(frm.doc.cat_name){
                                                        frm.doc.item_name = frm.doc.cat_name;
                                                        $.each(frm.doc.item_character,function(i,  d) {
                                                          if(d.attribute_value_both){
                                                            if(!d.attribute_value){
                                                        frm.doc.item_name += ' '+ d.attribute +':'+ d.attribute_value_both ;
                                                            }
                                                            else
                                                            {
                                                              frm.doc.item_name += ' '+  d.attribute_value_both ;
                                                                  }
                                                          }
                                                        });
                                                     }
                                          if(frm.doc.maintain_attribute & frm.doc.__islocal==1){
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
                                            if (frm.doc.naming_series.substring(0,2)!=frm.doc.item_group.substring(0,2))  {
                                              msgprint('Naming series should be relevant to Item Group..');
                                             validated = false;
                                         }   
                                         if (frm.doc.name!=frm.doc.item_code)  {
                                          msgprint('Item code should be same as Name..');
                                         validated = false;
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
                                                          if(d.attribute_value_both){
                                                            if(!d.attribute_value){
                                                        frm.doc.item_name += ' '+ d.attribute +':'+ d.attribute_value_both ;
                                                            }
                                                            else
                                                            {
                                                              frm.doc.item_name += ' '+  d.attribute_value_both ;
                                                                  }
                                                          }
                                                        });
                                                     }
                                                     if(!frm.doc.description){
                                                      frm.doc.description = frm.doc.item_name;
                                                        }
                                                
            
	                                },

                       refresh: function(frm,cdt,cdn) {
		                                           if (!frm.doc.trf_prodn && !frm.doc.__islocal) {
                                                  frm.add_custom_button(__("Transfer Item to Prodn"), function() {
		                                              var itemx = frappe.model.get_doc(cdt,cdn);
                                                  //msgprint("M" + itemx.manual_part_number);
                                                  //msgprint("M" + itemx.version); 
                                                 frappe.call({
                                                      method: "frappe.client.get_value",
                                                        args: {
                                                                 doctype: "Item",
                                                                 filters: [["item_name","=",itemx.item_name]],
                                                               fieldname: ["item_name","item_code"]
                                                           },

                                                      callback: function(r) {
                                                                //msgprint("Message_1");
                                                                console.log(r.message);
                                                                //msgprint(r.message.item_name);
                                                                //msgprint(r.message.item_code);

                                                                if (!r.message.item_name){

                                                                  let args1 = {
                                                                             
                                                                          "item_code" : itemx.item_code,
                                                                           "item_name" : itemx.item_name,
                                                                                   "uom": itemx.stock_uom,
                                                                            "item_group":itemx.item_group,
                                                                           "description":itemx.description,                                                                                   
                                                                            "manual_part_number":itemx.manual_part_number,                                                                                                                                                           
                                                                            "version":itemx.version,
                                                                            "weight_per_unit":itemx.weight_per_unit,
                                                                            "weight_uom":itemx.weight_uom,
                                                                            "valuation_rate":itemx.valuation_rate
                                                                                                                                                                                                                             
                                                                        //  "manufacturer":itemx.manufacturer,
                                                              //  "manufacturer_part_no":itemx.manufacturer_part_no
                                                                     
                                                                     }
                                                            /*          let args2 ={}
                                                                if (frm.doc.has_variants){

                                                                      args2 = {
                                                                        "has_variants" : 1
                                                                          
                                                                      }
                                                                } */
                                                                /* let args3 = {...args1,...args2} */
                                                                         frappe.call({
                                                                           method: "dms.dms.doctype.item_dms.item_dms.transfer_item_prodn",
                                                                           freeze: true,
                                                                					freeze_message: __('Transferring to Prodn..'),

                                                                           //type: "post",
                                                                           args: {
                                                                             
                                                                            "item_code" : itemx.item_code,
                                                                             "item_name" : itemx.item_name,
                                                                                     "uom": itemx.stock_uom,
                                                                              "item_group":itemx.item_group,
                                                                             "description":itemx.description,                                                                                   
                                                                              "manual_part_number":itemx.manual_part_number,                                                                                                                                                           
                                                                              "version":itemx.version,
                                                                              "weight_per_unit":itemx.weight_per_unit,
                                                                              "weight_uom":itemx.weight_uom,
                                                                              "valuation_rate":itemx.valuation_rate,
                                                                              "has_variants":itemx.has_variants
                                                                                                                                                   
                                                                          //  "manufacturer":itemx.manufacturer,
                                                                //  "manufacturer_part_no":itemx.manufacturer_part_no
                                                                       
                                                                       },
                                                                          callback: function(r1) {
                                                                                  console.log(r1.message);
                                                                               //   msgprint('XYZ');

                                                                                 //  msgprint(r1.message.item_code);
                                                                                   frm.set_value({trf_prodn : 1});
                                                                                   
                                                                                   frm.save();
                                                                                         }
                                                                                     });
                                                                          
                                                                              }
                                                                          }
                                                                     });
                                                        //msgprint(frm.doc.trf_prodn);

		                                                            });
                                                            }

                                frm.set_df_property('item_name',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('item_code',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('manual_part_number',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('version',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('item_group',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('stock_uom',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('description',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('item_character',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('maintain_attribute',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('cat_name',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('weight_per_unit',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('weight_uom',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('valuation_rate',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('has_variants',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('attribute',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('manufacturer',  'read_only',  frm.doc.trf_prodn==1);
                                frm.set_df_property('manufacturer_part_no',  'read_only',  frm.doc.trf_prodn==1);


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
