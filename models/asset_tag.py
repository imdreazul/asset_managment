# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetTag(models.Model):
    _name = 'asset.tag'
    _description = 'Asset Tag'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Tag Name',
        required=True,
        tracking=True,
        help='Name of the asset tag.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'Tag name must be unique!')
    ]
