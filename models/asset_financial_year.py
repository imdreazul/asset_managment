# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AssetFinancialYear(models.Model):
    _name = 'asset.financial.year'
    _description = 'Asset Financial Year'
    _order = 'start_date desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Financial Year Name',
        required=True,
        tracking=True,
        help='Name/label of the financial year (e.g. FY 2024-2025).'
    )
    start_date = fields.Date(
        string='Start Date',
        required=True,
        tracking=True,
        help='Start date of the financial year.'
    )
    end_date = fields.Date(
        string='End Date',
        required=True,
        tracking=True,
        help='End date of the financial year.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be archived and hidden from views.'
    )

    _sql_constraints = [
        ('unique_fy_name', 'UNIQUE(name)', 'Financial Year name must be unique!')
    ]

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.start_date >= record.end_date:
                    raise ValidationError(
                        "End Date must be strictly after Start Date for Financial Year '%s'." % record.name
                    )
