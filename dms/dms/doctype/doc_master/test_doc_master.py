# Copyright (c) 2013, xyz and Contributors
# See license.txt

import frappe
import unittest

test_records = frappe.get_test_records('Doc_master')

class TestDoc_master(unittest.TestCase):
	pass
