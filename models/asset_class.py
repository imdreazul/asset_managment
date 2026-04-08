# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetClass(models.Model):
    _name = 'asset.class'
    _description = 'Asset Class'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Class Name',
        required=True,
        tracking=True,
        help='Name of the asset class (top-level classification).'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )
    category_ids = fields.One2many(
        comodel_name='asset.category',
        inverse_name='asset_class',
        string='Categories',
        help='Categories belonging to this asset class.'
    )
    category_count = fields.Integer(
        string='Category Count',
        compute='_compute_category_count',
        help='Number of categories under this class.'
    )

    def _compute_category_count(self):
        for rec in self:
            rec.category_count = len(rec.category_ids)

    _sql_constraints = [
        ('unique_class_name', 'UNIQUE(name)', 'Asset Class name must be unique!')
    ]
