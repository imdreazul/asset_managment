# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetSupplier(models.Model):
    _name = 'asset.supplier'
    _description = 'Asset Supplier'
    _order = 'name asc'
    _rec_name = 'name'

    # Company Info
    name = fields.Char(string='Name', required=True)
    primary_email = fields.Char(string='Primary Email')
    secondary_email = fields.Char(string='Secondary Email')
    phone = fields.Char(string='Phone')
    website = fields.Char(string='Supplier Website')

    # Status Selection
    status = fields.Selection([
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended')
    ], string='Status', default='pending')

    # Contact Person Info
    contact_name = fields.Char(string='Contact Person Name')
    contact_phone = fields.Char(string='Contact Person Phone')
    contact_secondary_phone = fields.Char(string='Contact Person Secondary Phone')
    contact_email = fields.Char(string='Contact Person Email')
    address = fields.Text(string='Address')