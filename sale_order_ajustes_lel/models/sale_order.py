# -*- coding: utf-8 -*-
# © 2015 Danimar Ribeiro <danimaribeiro@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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
