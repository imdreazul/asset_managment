# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetService(models.Model):
    _name = 'asset.service'
    _description = 'Asset Service'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Service Name',
        required=True,
        tracking=True,
        help='Name of the asset service.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_service_name', 'UNIQUE(name)', 'Service name must be unique!')
    ]
