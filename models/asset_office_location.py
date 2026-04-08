# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetOfficeLocation(models.Model):
    _name = 'asset.office.location'
    _description = 'Asset Office Location'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Office Location Name',
        required=True,
        tracking=True,
        help='Name of the office location.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )
    floor_location_ids = fields.One2many(
        comodel_name='asset.floor.location',
        inverse_name='office_location',
        string='Floor Locations',
        help='Floor locations within this office location.'
    )
    floor_count = fields.Integer(
        string='Floor Count',
        compute='_compute_floor_count',
        help='Number of floor locations under this office.'
    )

    def _compute_floor_count(self):
        for rec in self:
            rec.floor_count = len(rec.floor_location_ids)

    _sql_constraints = [
        ('unique_office_location_name', 'UNIQUE(name)', 'Office Location name must be unique!')
    ]
