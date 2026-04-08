# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetFloorLocation(models.Model):
    _name = 'asset.floor.location'
    _description = 'Asset Floor Location'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Floor Location Name',
        required=True,
        tracking=True,
        help='Name of the floor location (e.g. Ground Floor, 1st Floor).'
    )
    office_location = fields.Many2one(
        comodel_name='asset.office.location',
        string='Office Location',
        required=True,
        ondelete='restrict',
        tracking=True,
        help='The office location this floor belongs to.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_floor_name_office', 'UNIQUE(name, office_location)',
         'Floor Location name must be unique per Office Location!')
    ]
