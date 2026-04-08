# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AssetInsurancePartner(models.Model):
    _name = 'asset.insurance.partner'
    _description = 'Asset Insurance Partner'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Insurance Partner Name',
        required=True,
        tracking=True,
        help='Name of the insurance company or partner.'
    )
    contact_person = fields.Char(
        string='Contact Person',
        tracking=True,
        help='Name of the primary contact person at the insurance partner.'
    )
    contact_person_no = fields.Char(
        string='Contact Number',
        tracking=True,
        help='Phone or mobile number of the contact person.'
    )
    website = fields.Char(
        string='Website',
        tracking=True,
        help='Website URL of the insurance partner.'
    )
    email = fields.Char(
        string='Email',
        tracking=True,
        help='Email address of the insurance partner or contact person.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_insurance_partner_name', 'UNIQUE(name)', 'Insurance Partner name must be unique!')
    ]

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError(
                    "Please provide a valid email address for '%s'." % record.name
                )
