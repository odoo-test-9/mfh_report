# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    $Id: account.py 1005 2005-07-25 08:41:42Z nicoe $
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _

class wizard_daily_report(osv.osv_memory):
    _name = 'wizard.report'
    _description = 'Wizard that opens the information.'
    _columns = {
        'date_from': fields.date('Date from', required=True),
        'date_to': fields.date('Date to', required=True),
        'company_id': fields.many2one('res.company', 'Company'),
    }

    _defaults = {
        'date_from': fields.datetime.now,
        'date_to': fields.datetime.now,
        'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'res.partner', context=c),

    }

    def print_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)[0]
        if not data['date_from'] or not data['date_to']:
            raise osv.except_osv(_('Error!'), _('You have to select at least one Day. And try again.'))
        datas = {
             'ids': [],
             'model': 'ir.ui.menu',
             'form': data
            }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'mfh_report.report_mfh',
            'datas': datas,
            }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
