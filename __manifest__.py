# -*- coding: utf-8 -*-
{
    'name': 'Open Academy',
    'version': '18.0.1.0',
    'summary': 'Manage Trainings, Courses, Sessions and Attendees',
    'description': """
    Open Academy Module
    ====================
    This module helps you to manage:
     - Courses
     - Sessions
     - Attendees
    """,
    'author': 'Arafa',
    'website': 'https://www.yourcompany.com',
    'category': 'Education',
    'depends': ['base', 'mail', 'website'],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/openacademy_course_views.xml',
        'views/openacademy_session_views.xml',
        'views/partner_id_view.xml',
        'views/session_website.xml',
        'wizard/openacademy_wizard.xml',
        'reports/paperformat.xml',
        'reports/reports.xml',
        'reports/custom_header_footer.xml',
        'reports/sale_qweb_template.xml',
        # 'reports/header_footer.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'openacademy/static/src/css/style.css',
        ],
    },

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
