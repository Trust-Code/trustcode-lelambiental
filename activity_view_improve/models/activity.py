
from odoo import models


class MailActivity(models.Model):
    _inherit = 'mail.activity'
    
    def action_view_object(self):
        return {
            'name': 'Atividades',
            'view_mode': 'form',
            'res_model': self.res_model,
            'res_id': self.res_id,
            'views': [(False, 'form')],
            'type': 'ir.actions.act_window',
        }
