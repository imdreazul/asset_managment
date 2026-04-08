# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AssetItem(models.Model):
    _name = 'asset.item'
    _description = 'Asset Item'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Item Name',
        required=True,
        tracking=True,
        help='Name of the asset item (lowest level classification).'
    )
    asset_category = fields.Many2one(
        comodel_name='asset.category',
        string='Asset Category',
        required=True,
        ondelete='restrict',
        tracking=True,
        help='The category this item belongs to.'
    )
    asset_class = fields.Many2one(
        comodel_name='asset.class',
        string='Asset Class',
        related='asset_category.asset_class',
        store=True,
        readonly=True,
        tracking=True,
        help='The class is automatically determined from the selected category.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_item_name_category', 'UNIQUE(name, asset_category)',
         'Item name must be unique per Asset Category!')
    ]
