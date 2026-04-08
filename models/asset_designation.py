# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetDesignation(models.Model):
    _name = 'asset.designation'
    _description = 'Asset Designation'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Designation Name',
        required=True,
        tracking=True,
        help='Name of the designation.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_designation_name', 'UNIQUE(name)', 'Designation name must be unique!')
    ]
