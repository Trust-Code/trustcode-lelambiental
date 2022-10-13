# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

from ..boleto.document import getBoletoSelection


selection = getBoletoSelection()
IMPLEMENTADOS = ('1', '3', '4', '6', '7', '8', '9', '10')


class AccountJournal(models.Model):
    _inherit = "account.journal"

    acc_codigo_convenio = fields.Char(
        related="bank_account_id.codigo_convenio"
    )
    boleto = fields.Boolean(string="Boleto?")
    nosso_numero_sequence = fields.Many2one(
        "ir.sequence", string="Seq. do Nosso Número"
    )
    late_payment_fee = fields.Float(
        string="Percentual Multa", digits=dp.get_precision("Account")
    )
    late_payment_interest = fields.Float(
        string="Juros de Mora", digits=dp.get_precision("Account")
    )
    late_payment_interest_type = fields.Selection(
        [
            ("01", "JUROS DIA"),
            ("02", "JUROS MENSAL"),
            ("03", "ISENTO"),
        ],
        string="Código de Juros",
        default="03",
    )
    instrucoes = fields.Text(string="Instruções")
    boleto_carteira = fields.Char("Carteira", size=3)
    boleto_modalidade = fields.Char("Modalidade", size=2)
    boleto_variacao = fields.Char("Variação", size=2)
    boleto_cnab_code = fields.Char("Código Convênio", size=20)
    boleto_aceite = fields.Selection(
        [("S", "Sim"), ("N", "Não")], string="Aceite", default="N"
    )
    boleto_type = fields.Selection(selection, string="Banco do Boleto")
    boleto_especie = fields.Selection(
        [
            ("01", "DUPLICATA MERCANTIL"),
            ("02", "NOTA PROMISSÓRIA"),
            ("03", "NOTA DE SEGURO"),
            ("04", "MENSALIDADE ESCOLAR"),
            ("05", "RECIBO"),
            ("06", "CONTRATO"),
            ("07", "COSSEGUROS"),
            ("08", "DUPLICATA DE SERVIÇO"),
            ("09", "LETRA DE CÂMBIO"),
            ("13", "NOTA DE DÉBITOS"),
            ("15", "DOCUMENTO DE DÍVIDA"),
            ("16", "ENCARGOS CONDOMINIAIS"),
            ("17", "CONTA DE PRESTAÇÃO DE SERVIÇOS"),
            ("99", "DIVERSOS"),
        ],
        string="Espécie do Título",
        default="01",
    )
    boleto_protesto = fields.Selection(
        [
            ("0", "Sem instrução"),
            ("1", "Protestar (Dias Corridos)"),
            ("2", "Protestar (Dias Úteis)"),
            ("3", "Não protestar"),
            ("4", "Protestar Fim Falimentar - Dias Úteis"),
            ("5", "Protestar Fim Falimentar - Dias Corridos"),
            ("7", "Negativar (Dias Corridos)"),
            ("8", "Não Negativar"),
        ],
        string="Códigos de Protesto",
        default="0",
    )
    boleto_protesto_prazo = fields.Char("Prazo protesto", size=2)
    l10n_br_environment = fields.Selection(
        [('test', 'Teste'),
         ('production', 'Produção')],
        string='Ambiente',
        default='production'
    )

    @api.onchange("boleto_type")
    def br_boleto_onchange_boleto_type(self):
        vals = {}

        if (self.boleto_type) and (self.boleto_type not in IMPLEMENTADOS):
            vals["warning"] = {
                "title": _("Ação Bloqueada!"),
                "message": _("Este boleto ainda não foi implementado!"),
            }

        if self.boleto_type == "1":
            if self.journal_id.bank_account_id.bank_id.bic != "001":
                vals["warning"] = {
                    "title": _("Ação Bloqueada!"),
                    "message": _(
                        "Este boleto não combina com a conta bancária!"
                    ),
                }

            self.boleto_carteira = "17"
            self.boleto_variacao = "19"

        if self.boleto_type == "3":
            if self.journal_id.bank_account_id.bank_id.bic != "237":
                vals["warning"] = {
                    "title": _("Ação Bloqueada!"),
                    "message": _(
                        "Este boleto não combina com a conta bancária!"
                    ),
                }
            self.boleto_carteira = "9"

        if self.boleto_type == "4":
            if self.journal_id.bank_account_id.bank_id.bic != "104":
                vals["warning"] = {
                    "title": _("Ação Bloqueada!"),
                    "message": _(
                        "Este boleto não combina com a conta bancária!"
                    ),
                }
            self.boleto_carteira = "1"
            self.boleto_modalidade = "14"

        if self.boleto_type == "7":
            if self.journal_id.bank_account_id.bank_id.bic != "033":
                vals["warning"] = {
                    "title": _("Ação Bloqueada!"),
                    "message": _(
                        "Este boleto não combina com a conta bancária!"
                    ),
                }
            self.boleto_carteira = "101"

        if self.boleto_type == "9":
            if self.journal_id.bank_account_id.bank_id.bic != "756":
                vals["warning"] = {
                    "title": _("Ação Bloqueada!"),
                    "message": _(
                        "Este boleto não combina com a conta bancária!"
                    ),
                }
            self.boleto_carteira = "1"
            self.boleto_modalidade = "01"

        if self.boleto_type == "10":
            if self.journal_id.bank_account_id.bank_id.bic != "0851":
                vals["warning"] = {
                    "title": _("Ação Bloqueada!"),
                    "message": _(
                        "Este boleto não combina com a conta bancária!"
                    ),
                }
            self.boleto_carteira = "01"
            self.boleto_protesto = "3"

        return vals

    @api.onchange("boleto_carteira")
    def br_boleto_onchange_boleto_carteira(self):
        vals = {}

        if self.boleto_type == "9" and len(self.boleto_carteira) != 1:
            vals["warning"] = {
                "title": _("Ação Bloqueada!"),
                "message": _(
                    "A carteira deste banco possui apenas um digito!"
                ),
            }

        return vals

    @api.onchange("boleto_protesto", "boleto_type")
    def _check_boleto_protesto(self):
        if self.boleto_protesto == "0" and self.boleto_type == "3":
            raise UserError(
                _("Código de protesto inválido para banco Bradesco!")
            )

    @api.constrains("boleto", "journal_id", "type", "boleto_type")
    def _check_payment_mode(self):
        for rec in self:
            if rec.type != "receivable" or not rec.boleto:
                continue
            if not rec.journal_id:
                raise ValidationError(_("Para boleto o diário é obrigatório"))
            if not rec.journal_id.bank_account_id:
                raise ValidationError(
                    _(
                        "Não existe conta bancária cadastrada no \
                      diário escolhido"
                    )
                )
            if not rec.nosso_numero_sequence:
                raise ValidationError(
                    _("Para boleto a Sequência do Nosso Número é obrigatória")
                )
            total = self.search_count(
                [
                    (
                        "nosso_numero_sequence",
                        "=",
                        rec.nosso_numero_sequence.id,
                    ),
                    ("id", "!=", rec.id),
                ]
            )
            if total > 0:
                raise ValidationError(
                    _("Sequência já usada em outro modo de pagamento")
                )
            if not rec.boleto_type:
                raise ValidationError(_("Escolha o banco do boleto!"))

    def write(self, vals):
        res = super(AccountJournal, self).write(vals)
        self._check_boleto_protesto()
        return res
