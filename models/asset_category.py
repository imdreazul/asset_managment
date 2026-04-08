# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetCategory(models.Model):
    _name = 'asset.category'
    _description = 'Asset Category'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Category Name',
        required=True,
        tracking=True,
        help='Name of the asset category.'
    )
    asset_class = fields.Many2one(
        comodel_name='asset.class',
        string='Asset Class',
        required=True,
        ondelete='restrict',
        tracking=True,
        help='The asset class this category belongs to.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )
    item_ids = fields.One2many(
        comodel_name='asset.item',
        inverse_name='asset_category',
        string='Items',
        help='Items belonging to this category.'
    )
    item_count = fields.Integer(
        string='Item Count',
        compute='_compute_item_count',
        help='Number of items under this category.'
    )

    def _compute_item_count(self):
        for rec in self:
            rec.item_count = len(rec.item_ids)

    _sql_constraints = [
        ('unique_category_name_class', 'UNIQUE(name, asset_class)',
         'Category name must be unique per Asset Class!')
    ]
