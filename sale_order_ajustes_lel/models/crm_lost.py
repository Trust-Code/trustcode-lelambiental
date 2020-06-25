from odoo import api, fields, models


class CrmLeadLost(models.TransientModel):
    _inherit = 'crm.lead.lost'
    
    def action_lost_reason_apply(self):
        if self.env.context.get('default_type') == 'sale_order':
            orders = self.env['sale.order'].browse(self.env.context.get('active_ids'))
            orders.write({'lost_reason_id': self.lost_reason_id.id})
            orders.action_cancel()
        else:
            return super(CrmLeadLost, self).action_lost_reason_apply()