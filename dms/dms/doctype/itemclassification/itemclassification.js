# Copyright (c) 2013, xyz and contributors
# For license information, please see license.txt

cur_frm.cscript.item_name = function(doc,cdt,cd)
{
	var d = locals[cdt][cdn];
	if (d.ItemClassification) {
		msgprint(__("You can not change rate if BOM mentioned agianst any item"));
		
	}
	

};

