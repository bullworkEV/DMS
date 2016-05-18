# Copyright (c) 2013, xyz and contributors
# For license information, please see license.txt

cur_frm.cscript.parent_class_item = function(doc,cdt,cd)
{
	var d = locals[cdt][cdn];
	if (d.parent_class_item === "cap1") {
		msgprint(__("You can not change rate if BOM mentioned agianst any item"));
		
	}
	

};

