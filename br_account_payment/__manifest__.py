# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{  # pylint: disable=C8101,C8103
    'name': 'Contas a Pagar e Receber',
    'summary': """Facilita a visualização de parcelas a pagar e receber
    no Odoo - Mantido por Trustcode""",
    'description': """Facilita a visualização de parcelas a pagar e receber
    no Odoo - Mantido por Trustcode""",
    'version': '12.0.1.0.0',
    'category': 'Invoicing & Payments',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>',
        'Carlos Alberto Cipriano Korovsky <carlos.korovsky@uktech.com.br',
    ],
    'depends': [
        'l10n_br_account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/br_account_payment.xml',
        'views/payment_order.xml',
        'views/res_settings.xml',
        'views/payment_statement.xml',
        'views/res_partner_bank.xml',
        'wizard/payment_cnab_import.xml',
        'wizard/payment_move_line.xml'
    ],
    'installable': True,
    'application': True,
}
