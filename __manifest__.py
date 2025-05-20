{
    "name": "iscapop",
    "summary": "iscapop",
    "description": """
Highschool items changer app
    """,
    "author": "Sergi",
    "website": "https://github.com/Betapoisoner",
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "web"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "security/security_rules.xml",
        "pdfs/donation_report_template.xml",
        "pdfs/retirement_report_template.xml",
        "views/menu_actions.xml",
        "views/categoryView.xml",
        "views/itemView.xml",
        "views/itemDetailsView.xml",
        "views/locationView.xml",
        "views/donationView.xml",
        "views/transferWizardView.xml",
        "views/retirementWizardView.xml",
        "views/claimWizardView.xml",
        "views/donationWizardView.xml",
        "views/reports.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "iscapop/static/src/css/kanban.css",
        ],
    },
    # only loaded in demonstration mode
    "demo": [],
    "application": True,
    "installable": True,
}
