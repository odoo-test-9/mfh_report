# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
from openerp import api, models
from openerp.osv import fields,osv
from openerp.tools.translate import _
from openerp.tools.sql import drop_view_if_exists
from datetime import date, timedelta

class MfhReport(osv.AbstractModel):
    _name = 'report.mfh_report.report_mfh'
    
    #~ def render_html(self, cr, uid, ids, data=None, context=None):
        #~ report_obj = self.pool['report']
        #~ wizard_obj = self.pool['wizard.report']
        #~ docs = wizard_obj.read(cr, uid, context['active_id'], context=context)
        #~ report = report_obj._get_report_from_name(cr, uid, 'mfh_report.report_mfh')

        #~ docargs = {
            #~ 'doc_ids': [context['active_id']],
            #~ 'doc_model': report.model,
            #~ 'docs': docs,
        #~ }
        #~ return report_obj.render(cr, uid, ids, 'mfh_report.report_mfh', docargs, context=context)

    @api.multi
    def render_html(self, data):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        
        # Intanciamos el Modelo que queremos filtrar para pasarlo a la vista
        # Filtramos por cuentas
        accounts = self.env['account.account'].search([('code', 'like', '1%')])  
        
        lis_accounts = []
        for i in accounts:
            lis_accounts.append(i.id)      
        
        # account.move.line - Tienen todos los movimientos contables
        # account = self.env["account.move.line"].search([date])        
        moves = self.env['account.move.line'].search([('date', '>=',data['form']['date_from'] ),
                                                      ('date', '<=', data['form']['date_to']),
                                                      ('account_id', 'in', lis_accounts)])
        print accounts
                
        suma = 0
        for mv in moves:
			suma += mv.debit
            
        
        docargs = {
            'doc_ids': self.env.context.get('active_ids', []),
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'move': moves,
            'msuma' : suma,
        }

        return self.env['report'].render('mfh_report.report_mfh', docargs)
