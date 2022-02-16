
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    state_id = fields.Many2one(related="partner_id.state_id", readonly=1, store=True)
