from odoo import models, fields


class AssetUser(models.Model):
    _name = 'asset.user'
    _description = 'Asset User'

    # Basic Information
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    additional_email = fields.Char(string='Additional Email')
    additional_phone = fields.Char(string='Additional Phone')
    employee_id = fields.Char(string='Employee ID')

    # Relational Fields (Many2one)
    company_id = fields.Many2one(
        'asset.company',
        string='Company'
    )
    department_id = fields.Many2one(
        'asset.department',
        string='Department'
    )
    district_id = fields.Many2one(
        'asset.district',
        string='District'
    )
    division_id = fields.Many2one(
        'asset.division',
        string='Division'
    )
    unit_id = fields.Many2one(
        'asset.unit',
        string='Unit'
    )
    office_location_id = fields.Many2one(
        'asset.office.location',
        string='Office Location'
    )
    designation_id = fields.Many2one(
        'asset.designation',
        string='Designation'
    )