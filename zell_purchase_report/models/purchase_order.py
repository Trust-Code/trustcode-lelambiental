# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _compute_tax_ipi_st(self):
        for item in self:
            item.total_st = sum(l.valor_st for l in item.order_line)
            item.total_ipi = sum(l.valor_ipi for l in item.order_line)

    total_ipi = fields.Monetary(
        string="Valor IPI", compute=_compute_tax_ipi_st)
    total_st = fields.Monetary(
        string="Valor ST", compute=_compute_tax_ipi_st)
    user_confirmed_purchased_order_id = fields.Many2one(
        "res.users", string="Usuário")

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            order.user_confirmed_purchased_order_id = self.env.user
        return res


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _compute_tax_ipi_st(self):
        for line in self:
            st = ipi = ali_ipi = 0.0
            price = line.price_unit
            ctx = line._prepare_tax_context()
            tax_ids = line.taxes_id.with_context(**ctx)
            taxes = tax_ids.compute_all(
                price, line.order_id.currency_id,
                line.product_qty,
                product=line.product_id,
                partner=line.order_id.partner_id)
            for tax in taxes['taxes']:
                tax_id = self.env['account.tax'].browse(tax['id'])
                if tax_id.domain == 'ipi':
                    ali_ipi += tax_id.amount
                    ipi += tax['amount']
                if tax_id.domain == 'icmsst':
                    st += tax['amount']
            line.update({
                'valor_ipi': ipi,
                'valor_st': st,
                'aliquota_ipi': ali_ipi
            })

    aliquota_ipi = fields.Float(string="% IPI", compute=_compute_tax_ipi_st)
    valor_ipi = fields.Monetary(
        string="Valor IPI", compute=_compute_tax_ipi_st)
    valor_st = fields.Monetary(
        string="Valor ST", compute=_compute_tax_ipi_st)
