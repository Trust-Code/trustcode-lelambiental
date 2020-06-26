
from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    state_id = fields.Many2one(related="partner_id.state_id", readonly=1, store=True)
