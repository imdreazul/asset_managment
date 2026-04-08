# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetUnit(models.Model):
    _name = 'asset.unit'
    _description = 'Asset Unit'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Unit Name',
        required=True,
        tracking=True,
        help='Name of the unit.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_unit_name', 'UNIQUE(name)', 'Unit name must be unique!')
    ]
