# -*- coding: utf-8 -*-
# © 2015 Danimar Ribeiro <danimaribeiro@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state_id = fields.Many2one(related="partner_id.state_id", readonly=1, store=True)

    @api.depends('order_line.qty_delivered', 'order_line.qty_invoiced', 'state')
    def _compute_balance_to_invoice(self):
        for order in self:
            products_total = 0.0
            for line in order.order_line:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                products_total += max(line.qty_to_invoice, 0) * price

            order.balance_to_invoice = products_total

    balance_to_invoice = fields.Monetary(
        string="Saldo a faturar", compute='_compute_balance_to_invoice',
        store=True)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_category_id = fields.Many2one(
        related='product_id.categ_id', readonly=True, store=True)


class SaleReport(models.Model):
    _inherit = "sale.report"

    state_id = fields.Many2one('res.country.state', 'Estado', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['state_id'] = ", s.state_id as state_id"
        groupby += ', s.state_id'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
