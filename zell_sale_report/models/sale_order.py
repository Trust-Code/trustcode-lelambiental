# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    transportadora = fields.Many2one('res.partner',
                                    domain="[('customer','=',True)]",
                                    string="Transportadora",
                                    )
    garantia = fields.Integer(string="Garantia")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    num_item = fields.Char(string="Núm Item")
