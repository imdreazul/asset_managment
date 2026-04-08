# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetDepartment(models.Model):
    _name = 'asset.department'
    _description = 'Asset Department'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Department Name',
        required=True,
        tracking=True,
        help='Name of the department.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_department_name', 'UNIQUE(name)', 'Department name must be unique!')
    ]
