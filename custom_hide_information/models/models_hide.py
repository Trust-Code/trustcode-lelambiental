from odoo import api, fields, models, _


class EletronicDocument(models.Model):
    _inherit = 'eletronic.document'


    def _compute_legal_information(self):
        res=super(EletronicDocument, self)._compute_legal_information
        fiscal_ids = self.fiscal_position_id.fiscal_observation_ids.filtered(
            lambda x: x.tipo == "fiscal"
                      and x.tipo_produto in [False] + self.document_line_ids.mapped("tipo_produto")
        )
        obs_ids = self.fiscal_position_id.fiscal_observation_ids.filtered(
            lambda x: x.tipo == "observacao"
                      and x.tipo_produto in [False] + self.document_line_ids.mapped("tipo_produto")
        )

        fiscal = self._compute_msg(fiscal_ids)

        observacao = self._compute_msg(obs_ids)
        self.informacoes_legais = fiscal
        self.informacoes_complementares = observacao
        return res