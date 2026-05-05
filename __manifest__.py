# -*- coding: utf-8 -*-
{
    'name': "Asset Managment",
    'summary': 'Comprehensive Asset Management System - Independent from Accounting',
    'description': """
        Custom Asset Management Module for Odoo 18
        ==========================================
        A full-featured asset management system completely independent
        from the Odoo Accounting asset module.

        Features:
        ---------
        * Company, Division, District, Department management
        * Asset classification (Class → Category → Item)
        * Location management (Office Location → Floor Location)
        * Asset lifecycle tracking
        * Insurance management
        * Financial year tracking
        * Asset tagging, branding, and service management
    """,
    'author': "Reazul",
    'website': "https://github.com/imdreazul",
    'category': 'Generic Modules/Asset Management',
    'version': '1.2',

    'depends': ['base', 'mail', 'web','hr'],
    'data': [
        # Security
        'security/ir.model.access.csv',

        'data/ir_sequence.xml',
        'data/asset_dashboard_data.xml',

        # Views - Configuration Masters
        'views/asset_company_views.xml',
        'views/asset_division_views.xml',
        'views/asset_district_views.xml',
        'views/asset_department_views.xml',
        'views/asset_unit_views.xml',
        'views/asset_designation_views.xml',
        'views/asset_tag_views.xml',
        'views/asset_brand_views.xml',
        'views/asset_service_views.xml',
        'views/asset_accessory_views.xml',
        'views/asset_financial_year_views.xml',
        'views/asset_color_views.xml',
        'views/asset_insurance_partner_views.xml',
        'views/asset_item_views.xml',
        'views/asset_category_views.xml',
        'views/asset_class_views.xml',
        'views/asset_floor_location_views.xml',
        'views/asset_office_location_views.xml',
        'views/asset_supplier_views.xml',
        'views/asset_user_views.xml',
        'views/asset_insurance_type_views.xml',

        # Master View
        'views/asset_views.xml',
        'views/asset_depreciation_views.xml',

        # Dashboard
        'views/asset_dashboard_views.xml',

        # Menu
        'views/menu_views.xml',


    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',

}

