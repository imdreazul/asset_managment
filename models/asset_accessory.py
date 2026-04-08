# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetAccessory(models.Model):
    _name = 'asset.accessory'
    _description = 'Asset Accessory'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Accessory Name',
        required=True,
        tracking=True,
        help='Name of the asset accessory.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_accessory_name', 'UNIQUE(name)', 'Accessory name must be unique!')
    ]
