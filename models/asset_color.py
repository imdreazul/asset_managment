# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetColor(models.Model):
    _name = 'asset.color'
    _description = 'Asset Color'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Color Name',
        required=True,
        tracking=True,
        help='Name of the color (e.g. Red, Blue, Black).'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_color_name', 'UNIQUE(name)', 'Color name must be unique!')
    ]
