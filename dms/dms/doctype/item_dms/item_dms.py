# -*- coding: utf-8 -*-
# Copyright (c) 2015, xyz and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
#import frappe
#from frappe.model.document import Document

import copy
import json
from typing import Dict, List, Optional
import pandas as pd

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import (
	cint,
	cstr,
	flt,
	formatdate,
	get_link_to_form,
	getdate,
	now_datetime,
	nowtime,
	strip,
	strip_html,
)
from frappe.utils.html_utils import clean_html

import erpnext
from erpnext.controllers.item_variant import (
	ItemVariantExistsError,
	copy_attributes_to_variant,
	get_variant,
	make_variant_item_code,
	validate_item_variant_attributes,
)
from erpnext.setup.doctype.item_group.item_group import invalidate_cache_for
from erpnext.stock.doctype.item_default.item_default import ItemDefault

class Itemdms(Document):
	def autoname(self):
		if frappe.get_doc("DMS Settings").item_dms_naming_by == "Naming Series":
			
			if self.item_code:
				template_item_name = frappe.db.get_value("Item dms", self.variant_of, "item_name")
				make_variant_item_code(self.variant_of, template_item_name, self)
			else:
				from frappe.model.naming import set_name_by_naming_series

				set_name_by_naming_series(self)
				frappe.msgprint(self.name)
				self.item_code = self.name

                
		self.item_code = strip(self.item_code)
		self.name = self.item_code



@frappe.whitelist()
def get_attribute_category(cat_name):
        attributes = frappe.db.sql(f""" SELECT b.attribute_name as attribute 
                       FROM `tabAttributes of Category` as a
                       left join `tabAttribute Character` as b on a.name=b.parent 
                       where  cat_name='{cat_name}' order by b.idx """, as_dict=True)
        return attributes
#changes made
@frappe.whitelist()
def query_attribute(doctype,txt,searchfield,start,page_len,filters):
        char_value=frappe.db.sql(""" select character_value
                       from `tabItem character` as a
                       left join `tabItem character value` as b
                       on a.name = b.parent 
                       where a.character_name='{charname}' """
                       .format(charname=filters["attribute"])
                       )
        return char_value

@frappe.whitelist()
def transfer_item_prodn(item_code,item_name,description,uom,item_group,
                                manual_part_number='',version='',weight_per_unit=0,weight_uom='Kg',valuation_rate=0,is_fixed_asset=0):

		has_variants = frappe.get_doc("Item dms",item_code).has_variants
		is_fixed_asset = frappe.get_doc("Item dms",item_code).is_fixed_asset
		asset_category = frappe.get_doc("Item dms",item_code).asset_category
		#frappe.msgprint(has_variants)
		if is_fixed_asset==1:
			is_stock_item = 0
		else:
			is_stock_item = 1

		if has_variants==1:
			transfer_item_variant_prodn(item_code,item_name,description,uom,item_group,has_variants,
								manual_part_number='',version='',weight_per_unit=0,weight_uom='Kg',valuation_rate=0,is_fixed_asset=0,is_stock_item=1,asset_category='')
		else:
			doc = frappe.get_doc({"doctype":"Item", "item_code" : item_code, "item_name": item_name,"description": description,
                                      "uom" : uom,"item_group" : item_group, "manual_part_number" : manual_part_number,
                                      "version" : version,"weight_per_unit" : weight_per_unit, "weight_uom":weight_uom,
                                      "valuation_rate":valuation_rate,"is_fixed_asset":is_fixed_asset,"is_stock_item":is_stock_item,"asset_category":asset_category})
			doc.insert()
			frappe.db.commit()
		#frappe.db.set_value("Item dms",item_code, "trf_prodn", 1)
		#frappe.db.commit()
		return item_code

@frappe.whitelist()
def transfer_item_variant_prodn(item_code,item_name,description,uom,item_group,has_variants,
                                manual_part_number='',version='',weight_per_unit=0,weight_uom='Kg',valuation_rate=0,is_fixed_asset=False,is_stock_item=1,asset_category=''
								):

		arg1 = {"doctype":"Item", "item_code" : item_code, "item_name": item_name,"description": description,
                                      "uom" : uom,"item_group" : item_group, "manual_part_number" : manual_part_number,
                                      "version" : version,"weight_per_unit" : weight_per_unit, "weight_uom":weight_uom,
                                      "valuation_rate":valuation_rate,"has_variants":1,"is_fixed_asset":is_fixed_asset,"is_stock_item":is_stock_item,"asset_category":asset_category}

		if has_variants==1:
			arg2 = {}
			arg3=[]
			doc1 = frappe.get_doc("Item dms",item_code)
			for d in doc1.attributes:
				#arg2["variant_of"]=item_code
				doc2 = frappe.get_doc("Item Attribute",d.attribute)
				arg2["attribute"]=d.attribute
				if doc2.numeric_values==1:
					arg2["numeric_values"]=doc2.numeric_values
					arg2["from_range"]=doc2.from_range
					arg2["to_range"]=doc2.to_range
					arg2["increment"]=doc2.increment
				arg3.append(arg2)
				arg2={}

			arg1['attributes']=arg3
			arg3=[]
			ag2={}
				

		doc = frappe.get_doc(arg1)
		doc.insert()
		frappe.db.commit()
		return item_code

@frappe.whitelist()
def update_trf_status_itemdms_background():
	df = frappe.get_all('Item dms',{'trf_prodn':0})
	df1 = pd.DataFrame.from_records(df)
	for index,row in df1.iterrows():
		doc= frappe.get_value('Item',row['name'])
		if doc:
			frappe.db.set_value("Item dms",row['name'], "trf_prodn", 1)
			frappe.db.commit()

