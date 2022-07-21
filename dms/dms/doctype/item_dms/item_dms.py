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
attributes = frappe.db.sql(f""" SELECT attribute FROM `tabAttributes of Category` WHERE cat_name='{cat_name}' """, as_dict=True)
return attributes
