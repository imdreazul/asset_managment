# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetBrand(models.Model):
    _name = 'asset.brand'
    _description = 'Asset Brand'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Brand Name',
        required=True,
        tracking=True,
        help='Name of the asset brand.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_brand_name', 'UNIQUE(name)', 'Brand name must be unique!')
    ]
