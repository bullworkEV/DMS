# -*- coding: utf-8 -*-
# Copyright (c) 2015, xyz and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
#import frappe
#from frappe.model.document import Document

import copy
import json
from typing import Dict, List, Optional

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
                        if self.variant_of:
                                if not self.item_code:
                                        template_item_name = frappe.db.get_value("Item dms", self.variant_of, "item_name")
                                        make_variant_item_code(self.variant_of, template_item_name, self)
                        else:
                                from frappe.model.naming import set_name_by_naming_series

                                set_name_by_naming_series(self)
                                self.item_code = self.name

                
                self.item_code = strip(self.item_code)
                self.name = self.item_code
	

@frappe.whitelist()
def get_attribute_category(cat_name):
        attributes = frappe.db.sql(f""" SELECT b.attribute_name as attribute 
                       FROM `tabAttributes of Category` as a
                       left join `tabAttribute Character` as b on a.name=b.parent 
                       where  cat_name='{cat_name}' """, as_dict=True)
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
