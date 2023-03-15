# Copyright (c) 2023, xyz and contributors
# For license information, please see license.txt

# import frappe


import functools
import re
from collections import deque
from operator import itemgetter
from typing import Dict, List

import frappe

from frappe.core.doctype.version.version import get_diff
from frappe.model.mapper import get_mapped_doc



#import erpnext
#from erpnext.setup.utils import get_exchange_rate
#from erpnext.stock.doctype.item.item import get_item_details
#from erpnext.stock.get_item_details import get_conversion_factor, get_price_list_rate

import pandas as pd

#from erpnext.stock.stock_balance import get_balance_qty_from_sle,get_reserved_qty,get_indented_qty,get_ordered_qty,get_planned_qty

import json


#from frappe import _, msgprint, throw

#from frappe.utils import cint, cstr, flt, get_link_to_form, getdate, new_line_sep, nowdate, today

#from erpnext.buying.utils import check_on_hold_or_closed_status, validate_for_items
#from erpnext.controllers.buying_controller import BuyingController
#from erpnext.manufacturing.doctype.work_order.work_order import get_item_details

#from erpnext.stock.stock_balance import get_indented_qty, update_bin_qty
from datetime import date, timedelta
from dms.dms.doctype.item_dms.item_dms import transfer_item_prodn

form_grid_templates = {"items": "templates/form_grid/item_grid.html"}

def execute(filters=None):
	columns, data = [], []
	data = []
	columns = get_columns()
	report_summary = []
	data = get_data(filters, data)

	message = ["Summary"]
	chart = [] 
	#report_summary = get_summary(data, report_summary)
	return columns, data  #, message , chart, report_summary


def get_data(filters, data):
	data = get_item_dms(data)
	return data


def get_item_dms(data,indent=0):
	data = frappe.db.sql(""" select 
	    item_code,item_name,description,stock_uom,item_group,
                                manual_part_number,version,weight_per_unit,weight_uom,valuation_rate
		from `tabItem dms` where trf_prodn = 0
		 order by item_code """,
		as_dict = 1
	)
	
	indent = 0
	return data


			
		

def get_columns():
	return [
		
		{
			"label": ("item_code"),
			"fieldtype": "Link",
			"fieldname": "item_code",
			"width": 300,
			"options": "Item dms",
		},
		{"label": ("item_name"), "fieldtype": "data", "fieldname": "item_name", "width": 100},
		{"label": ("item_group"), "fieldtype": "data", "fieldname": "item_group", "width": 100},
		{"label": ("manual_part_number"), "fieldtype": "data", "fieldname": "manual_part_number", "width": 100},
		{"label": ("version"), "fieldtype": "data", "fieldname": "version", "width": 100},
		{"label": ("stock_uom"), "fieldtype": "data", "fieldname": "stock_uom", "width": 100},
		{"label": ("description"), "fieldtype": "data", "fieldname": "description", "width": 200},
		{"label": ("weight_per_unit"), "fieldtype": "data", "fieldname": "weight_per_unit", "width": 100},
		{"label": ("weight_uom"), "fieldtype": "data", "fieldname": "weight_uom", "width": 100},
		{"label": ("valuation_rate"), "fieldtype": "data", "fieldname": "valuation_rate", "width": 100},
			
				
			
	]



@frappe.whitelist()
def trf_item_prodn_from_report(selected_rows):
	frappe.msgprint(selected_rows)
	#df1 = pd.DataFrame.from_records(json.loads(frappe.as_json(selected_rows)))
	df1 = (json.dumps(frappe.as_json(selected_rows)))
	#validate_selection(df1)
	#for doc in df1['item_code']:
	for doc in df1:
	
		""" if not d['weight_uom']:
			d['weight_uom']='Kg' """
		d = frappe.get_doc("Item dms",doc['item_code'])
		res = transfer_item_prodn(d.item_code,d.item_name,d.description,d.stock_uom,d.item_group,
                                d.manual_part_number,d.version,d.weight_per_unit,d.weight_uom,d.valuation_rate)
		frappe.msgprint("Transferred :",res)
		d.trf_prodn=1
		d.save()
		frappe.db.commit()
	return df1
		


""" 
def get_summary(data,report_summary):

	df = pd.DataFrame.from_dict(data)
	df = df[df['mr_level'] == 0]
	noofmrs = len(df.index)
	df1 = df.drop_duplicates(subset=['item_code'])
	noofitems = len(df1.index)
	df2 = df[df['draftpo'].notnull()]
	noofdraftpo = len(df2.index)

	report_summary = [{
        "value": noofmrs,
        "indicator": "Green" if noofmrs > 0 else "Red",
        "label": _("No. of Material Request"),
        "datatype": "Data"
		},
	{
        "value": noofitems,
        "indicator": "Green" if noofitems > 0 else "Red",
        "label": _("No. of items"),
        "datatype": "Data"
		},
        {
        "value": noofdraftpo,
        "indicator": "Green" if noofdraftpo > 0 else "Red",
        "label": _("No. of MRs with Draft PO"),
        "datatype": "Data"
                }

		]

	return report_summary
 """