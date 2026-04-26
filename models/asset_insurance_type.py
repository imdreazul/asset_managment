# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetInsuranceType(models.Model):
    _name = 'asset.insurance.type'
    _description = 'Asset asset Insurance Type'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Insurance Type Name',
        required=True,
        tracking=True,
        help='Name of the Insurance Type.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_unit_name', 'UNIQUE(name)', 'Unit name must be unique!')
    ]
