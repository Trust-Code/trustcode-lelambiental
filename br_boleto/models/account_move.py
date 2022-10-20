# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
from odoo import fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    boleto = fields.Boolean(related="payment_journal_id.boleto")

    def _get_email_template_invoice(self):
        return self.env.user.company_id.boleto_email_tmpl

    def send_email_boleto_queue(self):
        mail = self._get_email_template_invoice()
        if not mail:
            raise UserError(_("Modelo de email padrão não configurado"))

        attachment_obj = self.env["ir.attachment"]
        for item in self:

            atts = []
            self = self.with_context(
                {
                    "origin_model": "account.move",
                    "active_ids": [item.id],
                }
            )

            attachment_obj = self.env["ir.attachment"]
            boleto_report = self.env["ir.actions.report"].search(
                [("report_name", "=", "br_boleto.report.print")]
            )
            report_service = boleto_report.xml_id
            boleto, dummy = self.env.ref(report_service).render_qweb_pdf(
                [item.id]
            )

            if boleto:
                name = "boleto-%s-%s.pdf" % (
                    item.name,
                    item.partner_id.commercial_partner_id.name,
                )
                boleto_id = attachment_obj.create(
                    dict(
                        name=name,
                        datas_fname=name,
                        datas=base64.b64encode(boleto),
                        mimetype="application/pdf",
                        res_model="account.move",
                        res_id=item.id,
                    )
                )
                atts.append(boleto_id.id)

            values = {"attachment_ids": atts + mail.attachment_ids.ids}
            mail.send_mail(item.id, email_values=values)

    def action_post(self):
        res = super(AccountMove, self).action_post()
        error = ""
        for item in self:
            if not item.payment_journal_id:
                continue
            if item.payment_journal_id.type != "bank":
                continue
            if not item.payment_journal_id.boleto:
                continue
            if not item.company_id.partner_id.l10n_br_legal_name:
                error += "Empresa - Razão Social\n"
            if not item.company_id.l10n_br_cnpj_cpf:
                error += "Empresa - CNPJ\n"
            if not item.company_id.l10n_br_district:
                error += "Empresa - Bairro\n"
            if not item.company_id.zip:
                error += "Empresa - CEP\n"
            if not item.company_id.city_id.name:
                error += "Empresa - Cidade\n"
            if not item.company_id.street:
                error += "Empresa - Logradouro\n"
            if not item.company_id.l10n_br_number:
                error += "Empresa - Número\n"
            if not item.company_id.state_id.code:
                error += "Empresa - Estado\n"

            if not item.commercial_partner_id.name:
                error += "Cliente - Nome\n"
            if (
                item.commercial_partner_id.is_company
                and not item.commercial_partner_id.l10n_br_legal_name
            ):
                error += "Cliente - Razão Social\n"
            if not item.commercial_partner_id.l10n_br_cnpj_cpf:
                error += "Cliente - CNPJ/CPF \n"
            if not item.commercial_partner_id.l10n_br_district:
                error += "Cliente - Bairro\n"
            if not item.commercial_partner_id.zip:
                error += "Cliente - CEP\n"
            if not item.commercial_partner_id.city_id.name:
                error += "Cliente - Cidade\n"
            if not item.commercial_partner_id.street:
                error += "Cliente - Logradouro\n"
            if not item.commercial_partner_id.l10n_br_number:
                error += "Cliente - Número\n"
            if not item.commercial_partner_id.state_id.code:
                error += "Cliente - Estado\n"

            if item.name and len(item.name) > 12:
                error += (
                    "Numeração da fatura deve ser menor que 12 "
                    + "caracteres quando usado boleto\n"
                )

            if len(error) > 0:
                raise UserError(
                    _(
                        """Ação Bloqueada!
Para prosseguir é necessário preencher os seguintes campos:\n"""
                    )
                    + error
                )
        return res

    def action_print_boleto(self):
        if self.state in ("draft", "cancel"):
            raise UserError(
                _("Fatura provisória ou cancelada não permite emitir boleto")
            )
        self = self.with_context({"origin_model": "account.move"})
        return self.env.ref(
            "br_boleto.action_boleto_account_invoice"
        ).report_action(self)