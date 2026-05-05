# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date


class AssetDepreciationLine(models.Model):
    _name = 'asset.depreciation.line'
    _description = 'Asset Depreciation Line'
    _order = 'date_from asc, id asc'
    _rec_name = 'asset_id'

    # ── Relation ──────────────────────────────────────────────────
    asset_id = fields.Many2one(
        'asset.asset', string='Asset',
        required=True, ondelete='cascade', index=True,
    )

    # ── Period ────────────────────────────────────────────────────
    period_type = fields.Selection([
        ('day',   'Day'),
        ('month', 'Month'),
        ('year',  'Year'),
    ], string='Period Type', default='month', required=True)

    date_from = fields.Date(string='From Date', required=True)
    date_to   = fields.Date(string='To Date',   required=True)

    days = fields.Integer(
        string='Days',
        compute='_compute_days', store=True,
        help='Number of calendar days in this period.',
    )
    months = fields.Integer(
        string='Months',
        compute='_compute_months', store=True,
    )
    years = fields.Float(
        string='Years (Fraction)',
        compute='_compute_days', store=True,
        digits=(16, 6),
    )

    # ── COST Section ──────────────────────────────────────────────
    cost_opening_balance = fields.Float(
        string='Opening Balance (Cost)',
        digits=(16, 2),
        help='Opening balance of the asset cost for this period.',
    )
    cost_addition = fields.Float(
        string='Addition',
        digits=(16, 2),
        help='Cost additions (purchases, improvements) during this period.',
    )
    cost_adjustment = fields.Float(
        string='Adjustment (Disposal/Write-off)',
        digits=(16, 2),
        help='Cost reductions (disposals, write-offs) during this period.',
    )
    cost_closing_balance = fields.Float(
        string='Closing Balance (Cost)',
        compute='_compute_cost_closing', store=True,
        digits=(16, 2),
        help='= Opening + Addition − Adjustment',
    )

    # ── DEPRECIATION Section ──────────────────────────────────────
    dep_opening_balance = fields.Float(
        string='Opening Balance (Depreciation)',
        digits=(16, 2),
        help='Accumulated depreciation brought forward.',
    )
    dep_charge = fields.Float(
        string='Charge During Period',
        compute='_compute_dep', store=True,
        digits=(16, 2),
        help='Depreciation expense recognised this period.',
    )
    dep_adjustment = fields.Float(
        string='Adjustment (Depreciation)',
        digits=(16, 2),
        help='Depreciation reversed on disposed / written-off assets.',
    )
    dep_closing_balance = fields.Float(
        string='Closing Balance (Depreciation)',
        compute='_compute_dep', store=True,
        digits=(16, 2),
        help='= Opening + Charge − Adjustment',
    )
    written_down_value = fields.Float(
        string='Written Down Value (WDV)',
        compute='_compute_dep', store=True,
        digits=(16, 2),
        help='= Closing Cost − Closing Depreciation',
    )

    # ── KM / Per-Hour / Copy Method ───────────────────────────────
    km_this_period = fields.Float(
        string='KM / Service / Copy (this period)',
        digits=(16, 2),
        help='Actual usage units consumed during this period (KM, service count, copies printed, etc.).',
    )

    # ── Display Helpers ───────────────────────────────────────────
    depreciation_method = fields.Selection(
        related='asset_id.depreciation_method', store=False, readonly=True,
    )

    # ─────────────────────────────────────────────────────────────
    # COMPUTE  –  Days / Years
    # ─────────────────────────────────────────────────────────────
    @api.depends('date_from', 'date_to')
    def _compute_days(self):
        for line in self:
            if line.date_from and line.date_to:
                delta = (line.date_to - line.date_from).days + 1   # inclusive
                line.days  = delta
                line.years = delta / 365.0
            else:
                line.days  = 0
                line.years = 0.0

    @api.depends('date_from', 'date_to')
    def _compute_months(self):
        for line in self:
            if line.date_from and line.date_to:
                d1, d2 = line.date_from, line.date_to
                line.months = (d2.year - d1.year) * 12 + (d2.month - d1.month + 1)
            else:
                line.months = 0

    # ─────────────────────────────────────────────────────────────
    # COMPUTE  –  Cost Closing Balance
    # ─────────────────────────────────────────────────────────────
    @api.depends('cost_opening_balance', 'cost_addition', 'cost_adjustment')
    def _compute_cost_closing(self):
        for line in self:
            line.cost_closing_balance = (
                line.cost_opening_balance
                + line.cost_addition
                - line.cost_adjustment
            )

    # ─────────────────────────────────────────────────────────────
    # COMPUTE  –  Depreciation Charge, Closing Dep & WDV
    # ─────────────────────────────────────────────────────────────
    @api.depends(
        'cost_closing_balance',
        'dep_opening_balance', 'dep_adjustment',
        'days', 'km_this_period',
        'asset_id.depreciation_method',
        'asset_id.depreciation_rate',
        'asset_id.expected_km',
    )
    def _compute_dep(self):
        for line in self:
            method = line.asset_id.depreciation_method
            rate   = (line.asset_id.depreciation_rate or 0.0) / 100.0
            days   = line.days or 0

            # ── 1. Reducing Balance (Written Down Value) ──────────
            if method == 'reducing':
                # WDV Base = Closing Cost − Opening Dep + Dep Adjustment
                wdv_base = (
                    line.cost_closing_balance
                    - line.dep_opening_balance
                    + line.dep_adjustment
                )
                # Prorate by days: annual rate × (days / 365)
                line.dep_charge = wdv_base * rate * (days / 365.0) if days else 0.0

            # ── 2. Straight-Line Method ───────────────────────────
            elif method == 'straight_line':
                # Charge = Closing Cost × Rate × (Days / 365)
                line.dep_charge = (
                    line.cost_closing_balance * rate * (days / 365.0)
                ) if days else 0.0

            # ── 3. KM / Per-Hour / Copy Method ────────────────────
            elif method == 'km_per_hour':
                expected = line.asset_id.expected_km or 1.0
                # Charge = Closing Cost / Expected Total KM × KM this period
                line.dep_charge = (
                    line.cost_closing_balance / expected * line.km_this_period
                )

            else:
                line.dep_charge = 0.0

            # Closing Dep = Opening Dep + Charge − Adjustment
            line.dep_closing_balance = (
                line.dep_opening_balance
                + line.dep_charge
                - line.dep_adjustment
            )

            # Written Down Value = Closing Cost − Closing Dep
            line.written_down_value = (
                line.cost_closing_balance - line.dep_closing_balance
            )

    # ─────────────────────────────────────────────────────────────
    # CONSTRAINTS
    # ─────────────────────────────────────────────────────────────
    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for line in self:
            if line.date_from and line.date_to and line.date_from > line.date_to:
                raise UserError(_(
                    "From Date cannot be later than To Date on depreciation line."
                ))

    @api.constrains('cost_closing_balance')
    def _check_cost_not_negative(self):
        for line in self:
            if line.cost_closing_balance < 0:
                raise UserError(_(
                    "Closing Balance of Cost cannot be negative. "
                    "Please check the Adjustment amount for period %s – %s."
                ) % (line.date_from, line.date_to))
