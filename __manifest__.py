# -*- coding: utf-8 -*-
{
    'name': "iscapop",

    'summary': "iscapop",

    'description': """
Highschool items changer app
    """,

    'author': "Sergi",
    'website': "https://github.com/Betapoisoner",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/itemView.xml',
        'views/locationView.xml',
        'views/donationView.xml',
        'views/donationWizardView.xml',
        'views/itemDetailsView.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
    'installable':True,
}

