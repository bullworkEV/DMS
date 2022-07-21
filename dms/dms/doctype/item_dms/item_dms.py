# -*- coding: utf-8 -*-
# Copyright (c) 2015, xyz and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Itemdms(Document):
	pass

@frappe.whitelist()
def get_attribute_category(cat_name):
        attributes = frappe.db.sql(f""" SELECT b.attribute_name as attribute 
                       FROM `tabAttributes of Category` as a
                       left join `tabDMS Character` as b on a.name=b.parent 
                       where  cat_name='{cat_name}' """, as_dict=True)
        return attributes

@frappe.whitelist()
def query_attribute(char_name):
        char_value=frappe.db.sql(""" select character_value 
                       from `tabItem character` as a
                       left join `tabItem character value` as b
                       on a.name = b.parent 
                       where a.character_name='Material' """,
                       as_dict=True)
        return char_value
