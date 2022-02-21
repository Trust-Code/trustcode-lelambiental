# -*- coding: utf-8 -*-
# © 2017 Fillipe Ramos, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Modelo de Cotação de Compra',
    'description': "Modelo de Cotação de Compra",
    'summary': "Modelo de Cotação de Compra",
    'version': '10.0.1.0.0',
    'category': "Sales",
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>',
    ],
    'depends': [
        'stock',
        'purchase',
        'l10n_br_purchase',
    ],
    'data': [
        'reports/purchase_order.xml',
    ],
}
