# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetDistrict(models.Model):
    _name = 'asset.district'
    _description = 'Asset District'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='District Name',
        required=True,
        tracking=True,
        help='Name of the district.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_district_name', 'UNIQUE(name)', 'District name must be unique!')
    ]
