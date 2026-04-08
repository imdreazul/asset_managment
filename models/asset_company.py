# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AssetCompany(models.Model):
    _name = 'asset.company'
    _description = 'Asset Company'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Company Name',
        required=True,
        tracking=True,
        help='Name of the company for asset management purposes.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    logo = fields.Image(string="Company Logo")

    _sql_constraints = [
        ('unique_company_name', 'UNIQUE(name)', 'Company name must be unique!')
    ]
