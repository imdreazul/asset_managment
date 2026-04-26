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

    # New fields strictly for the dashboard UI
    dashboard_asset_count = fields.Integer(compute='_compute_dashboard_data')
    dashboard_color = fields.Char(compute='_compute_dashboard_data')

    def _compute_dashboard_data(self):
        Asset = self.env['asset.asset']
        colors = [
            '#00c0ef', '#00a65a', '#001F3F', '#0073b7', '#00b5b8',
            '#6f42c1', '#e91e8c', '#f39c12', '#dd4b39', '#3d9970'
        ]

        for idx, rec in enumerate(self):
            # Count the assets
            rec.dashboard_asset_count = Asset.search_count([('asset_class', '=', rec.id)])
            # Assign a color from the array
            rec.dashboard_color = colors[idx % len(colors)]

    def action_open_assets_from_dashboard(self):
        """Action triggered when 'More Info' is clicked"""
        return {
            'name': f'{self.name} Assets',
            'type': 'ir.actions.act_window',
            'res_model': 'asset.asset',
            'view_mode': 'list,form',
            'domain': [('asset_class', '=', self.id)],
        }
