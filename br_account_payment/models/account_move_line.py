# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    l10n_br_order_line_id = fields.Many2one(
        'payment.order.line', string='Linha de Pagamento')

    def action_register_payment(self):
        dummy, act_id = self.env['ir.model.data'].get_object_reference(
            'account', 'action_account_invoice_payment')
        receivable = (self.account_id.internal_type == 'receivable')
        vals = self.env['ir.actions.act_window'].browse(act_id).read()[0]
        vals['context'] = {
            'default_amount': self.debit or self.credit,
            'default_partner_type': 'customer' if receivable else 'supplier',
            'default_partner_id': self.partner_id.id,
            'default_communication': self.name,
            'default_payment_type': 'inbound' if receivable else 'outbound',
            'default_move_line_id': self.id,
        }
        if self.invoice_id:
            vals['context']['default_invoice_ids'] = [self.invoice_id.id]
        return vals

    def action_register_payment_move_line(self):
        dummy, act_id = self.env['ir.model.data'].get_object_reference(
            'br_account_payment', 'action_payment_account_move_line'
        )
        receivable = (self.account_id.internal_type == 'receivable')
        vals = self.env['ir.actions.act_window'].browse(act_id).read()[0]
        vals['context'] = {
            'default_amount': self.debit or self.credit,
            'default_partner_type': 'customer' if receivable else 'supplier',
            'default_partner_id': self.partner_id.id,
            'default_communication': self.name,
            'default_move_line_id': self.id,
        }
        return vals
