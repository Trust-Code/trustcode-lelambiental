# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_bank_account(self):
        for rec in self:
            acc = self.env['res.partner.bank'].search(
                [('partner_id', '=', rec.id)], limit=1)
            if acc:
                rec.account_ids = acc.id

    account_ids = fields.Many2one('res.partner.bank', string="Conta Bancária",
                                  compute='_get_bank_account')
