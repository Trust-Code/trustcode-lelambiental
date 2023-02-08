{  # pylint: disable=C8101,C8103
    'name': "Hide legal Information NF-e",
    'summary': """  Remove a seguinte menssagem da Nf-e Valor Aprox. dos Tributos R$ 0.0. Fonte: IBPT """,
    'description': """ Remove a menssagem da Nf-e """,
    'category': 'website',
    'version': '14.01',

    "author": "Trustcode",
    "website": "https://trustcode.com.br",
    'contributors': [
        'Jonatas Biazus <jonatasbiazusct@gmail.com>',
    ],

    'depends': [
        'l10n_br_eletronic_document',
    ],
    'external_dependencies': {
        'python': [
            'pytrustnfe',
        ],
    },
    'data': [
    ],
    'demo': [
    ],
}