# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta


class AssetDepreciationGenerateWizard(models.TransientModel):
    _name = 'asset.depreciation.generate.wizard'
    _description = 'Generate Depreciation Schedule'

    asset_id = fields.Many2one(
        'asset.asset', string='Asset',
        required=True, ondelete='cascade',
    )
    depreciation_method = fields.Selection(
        related='asset_id.depreciation_method',
        readonly=True,
    )
    date_from = fields.Date(
        string='Schedule Start Date',
        required=True,
        help='First day of the first depreciation period.',
    )
    date_to = fields.Date(
        string='Schedule End Date',
        required=True,
        help='Last day of the last depreciation period to generate.',
    )
    period_type = fields.Selection([
        ('day',   'Daily'),
        ('month', 'Monthly'),
        ('year',  'Yearly'),
    ], string='Period Type', default='month', required=True,
        help='Granularity of each generated line.',
    )
    delete_existing = fields.Boolean(
        string='Delete Existing Lines',
        default=False,
        help='If checked, all existing depreciation lines for this asset '
             'will be removed before generating the new schedule.',
    )

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for rec in self:
            if rec.date_from and rec.date_to and rec.date_from > rec.date_to:
                raise UserError(_('Start Date must be before End Date.'))

    def action_generate(self):
        self.ensure_one()
        asset = self.asset_id

        if self.delete_existing:
            asset.depreciation_line_ids.unlink()

        periods = self._build_periods(self.date_from, self.date_to, self.period_type)

        lines_vals = []
        for p_from, p_to in periods:
            lines_vals.append({
                'asset_id':       asset.id,
                'period_type':    self.period_type,
                'date_from':      p_from,
                'date_to':        p_to,
                'cost_opening_balance': 0.0,
                'dep_opening_balance':  0.0,
            })

        self.env['asset.depreciation.line'].create(lines_vals)

        # Auto-propagate opening balances
        asset.action_propagate_dep_balances()

        return {
            'type':  'ir.actions.act_window',
            'name':  _('Depreciation Schedule'),
            'res_model': 'asset.asset',
            'res_id': asset.id,
            'view_mode': 'form',
            'target': 'current',
        }

    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def _build_periods(start: date, end: date, period_type: str):
        """Return list of (date_from, date_to) tuples for the range."""
        periods = []
        cursor = start

        if period_type == 'day':
            while cursor <= end:
                periods.append((cursor, cursor))
                cursor += timedelta(days=1)

        elif period_type == 'month':
            while cursor <= end:
                # End of this month
                month_end = (cursor + relativedelta(months=1)) - timedelta(days=1)
                period_end = min(month_end, end)
                periods.append((cursor, period_end))
                cursor = period_end + timedelta(days=1)

        elif period_type == 'year':
            while cursor <= end:
                year_end = date(cursor.year, 12, 31)
                period_end = min(year_end, end)
                periods.append((cursor, period_end))
                cursor = period_end + timedelta(days=1)

        return periods
