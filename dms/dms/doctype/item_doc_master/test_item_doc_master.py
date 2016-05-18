# Copyright (c) 2013, xyz and Contributors
# See license.txt

import frappe
import unittest

test_records = frappe.get_test_records('Item_doc_master')

class TestItem_doc_master(unittest.TestCase):
	pass
