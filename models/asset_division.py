# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetDivision(models.Model):
    _name = 'asset.division'
    _description = 'Asset Division'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Division Name',
        required=True,
        tracking=True,
        help='Name of the division.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_division_name', 'UNIQUE(name)', 'Division name must be unique!')
    ]
