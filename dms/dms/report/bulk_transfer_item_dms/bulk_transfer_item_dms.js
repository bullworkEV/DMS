// Copyright (c) 2023, xyz and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Bulk Transfer Item Dms"] = {
	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},
	onload: function(report) {
	    report.page.add_action_item(__("Transfer item to Prodn"), function() {
			let checked_rows_indexes = report.datatable.rowmanager.getCheckedRows();
			let checked_rows = checked_rows_indexes.map(i => report.data[i]);
			/* DO WHATEVER YOU LIKE WITH YOUR `checked_rows`!  */
            // debugger;
			frappe.call({
				method : 'dms.dms.report.bulk_transfer_item_dms.bulk_transfer_item_dms.trf_item_prodn_from_report',
				args : {
					selected_rows :checked_rows
					}
			})


		});
    },

};
