# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date


# ─── colour palette cycling for class cards ───────────────────────────────────
CLASS_COLOURS = [
    '#00c0ef',  # light-blue
    '#00a65a',  # green
    '#001F3F',  # navy
    '#0073b7',  # blue
    '#00b5b8',  # teal
    '#6f42c1',  # purple
    '#e91e8c',  # pink
    '#f39c12',  # orange
    '#dd4b39',  # red
    '#3d9970',  # olive
    '#001f3f',  # dark-navy
    '#0073b7',  # blue 2
    '#e91e8c',  # pink 2
    '#6f42c1',  # purple 2
    '#00a65a',  # green 2
]


class AssetDashboard(models.Model):
    """
    Singleton-style dashboard model.
    One record per company is created via data XML.
    All KPI fields are computed (store=False) so they always reflect live data.
    """
    _name = 'asset.dashboard'
    _description = 'Asset Management Dashboard'

    name = fields.Char(default='Asset Dashboard', readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company,
    )

    # ── Insurance KPIs ────────────────────────────────────────────────────────
    count_insurance = fields.Integer(
        string='Have Insurance', compute='_compute_insurance_kpis')
    count_premium_this_month = fields.Integer(
        string='Premium This Month', compute='_compute_insurance_kpis')
    count_premium_done_this_month = fields.Integer(
        string='Premium Done This Month', compute='_compute_insurance_kpis')
    count_premium_overdue = fields.Integer(
        string='Premium Overdue (Not Paid)', compute='_compute_insurance_kpis')
    count_reminder_upcoming = fields.Integer(
        string='Reminder Upcoming', compute='_compute_insurance_kpis')
    count_reminder_expired = fields.Integer(
        string='Reminder Expired', compute='_compute_insurance_kpis')

    # ── Status KPIs ───────────────────────────────────────────────────────────
    count_active = fields.Integer(compute='_compute_status_kpis')
    count_new = fields.Integer(compute='_compute_status_kpis')
    count_broken = fields.Integer(compute='_compute_status_kpis')
    count_faulty = fields.Integer(compute='_compute_status_kpis')
    count_idle = fields.Integer(compute='_compute_status_kpis')
    count_in_servicing = fields.Integer(compute='_compute_status_kpis')
    count_listed_for_dismantle = fields.Integer(compute='_compute_status_kpis')
    count_sold = fields.Integer(compute='_compute_status_kpis')
    count_lost = fields.Integer(compute='_compute_status_kpis')
    count_archived = fields.Integer(compute='_compute_status_kpis')

    # ── Class-wise HTML ───────────────────────────────────────────────────────
    class_summary_html = fields.Html(
        string='Class Summary', compute='_compute_class_summary',
        sanitize=False,
    )

    # ─────────────────────────────────────────────────────────────────────────
    # COMPUTE METHODS
    # ─────────────────────────────────────────────────────────────────────────

    def _compute_insurance_kpis(self):
        Asset = self.env['asset.asset']
        today = date.today()
        first_day = today.replace(day=1)
        # last day of month
        if today.month == 12:
            last_day = today.replace(day=31)
        else:
            last_day = today.replace(month=today.month + 1, day=1).replace(
                day=1) - __import__('datetime').timedelta(days=1)

        for rec in self:
            rec.count_insurance = Asset.search_count(
                [('is_insurance', '=', True)])

            rec.count_premium_this_month = Asset.search_count([
                ('is_insurance', '=', True),
                ('premium_date', '>=', first_day),
                ('premium_date', '<=', last_day),
            ])

            rec.count_premium_done_this_month = Asset.search_count([
                ('is_insurance', '=', True),
                ('insurance_complete_date', '>=', first_day),
                ('insurance_complete_date', '<=', last_day),
            ])

            rec.count_premium_overdue = Asset.search_count([
                ('is_insurance', '=', True),
                ('premium_date', '<', today),
                ('is_premium_paid', '=', False),
            ])

            rec.count_reminder_upcoming = Asset.search_count([
                ('is_reminder', '=', True),
                ('reminder_date', '>=', today),
            ])

            rec.count_reminder_expired = Asset.search_count([
                ('is_reminder', '=', True),
                ('reminder_date', '<', today),
            ])

    def _compute_status_kpis(self):
        Asset = self.env['asset.asset']
        for rec in self:
            rec.count_active              = Asset.search_count([('state', '=', 'active')])
            rec.count_new                 = Asset.search_count([('state', '=', 'new')])
            rec.count_broken              = Asset.search_count([('state', '=', 'broken')])
            rec.count_faulty              = Asset.search_count([('state', '=', 'faulty')])
            rec.count_idle                = Asset.search_count([('state', '=', 'idle')])
            rec.count_in_servicing        = Asset.search_count([('state', '=', 'in_servicing')])
            rec.count_listed_for_dismantle = Asset.search_count([('state', '=', 'listed_for_dismantle')])
            rec.count_sold                = Asset.search_count([('state', '=', 'sold')])
            rec.count_lost                = Asset.search_count([('state', '=', 'lost')])
            rec.count_archived            = Asset.search_count([('state', '=', 'archived')])

    def _compute_class_summary(self):
        for rec in self:
            classes = self.env['asset.class'].search([('active', '=', True)])
            Asset = self.env['asset.asset']

            cards_html = ''
            for idx, cls in enumerate(classes):
                count = Asset.search_count([('asset_class', '=', cls.id)])
                colour = CLASS_COLOURS[idx % len(CLASS_COLOURS)]
                action_url = (
                    f"/odoo/assets?asset_class={cls.id}"
                )
                cards_html += f"""
                <div style="
                    display:inline-block; width:calc(25% - 16px);
                    min-width:220px; margin:8px; vertical-align:top;
                    background:{colour}; border-radius:6px; overflow:hidden;
                    box-shadow:0 2px 6px rgba(0,0,0,.25); color:#fff;">
                  <div style="padding:18px 18px 10px; display:flex;
                              justify-content:space-between; align-items:center;">
                    <div>
                      <div style="font-size:36px; font-weight:700; line-height:1;">
                        {count}
                      </div>
                      <div style="font-size:15px; font-weight:700; margin-top:4px;">
                        {cls.name}
                      </div>
                      <div style="font-size:12px; opacity:.85; margin-top:4px;">
                        Class Assets Found
                      </div>
                    </div>
                    <div style="font-size:72px; opacity:.25; line-height:1;">
                      &#128722;
                    </div>
                  </div>
                  <div style="background:rgba(0,0,0,.2); padding:6px 18px;
                              font-size:12px; cursor:pointer;">
                    <a href="{action_url}"
                       style="color:#fff; text-decoration:none;">
                      More info &#8594;
                    </a>
                  </div>
                </div>"""

            rec.class_summary_html = (
                f'<div style="padding:4px 0;">{cards_html}</div>'
                if cards_html else
                '<p style="color:#888;">No asset classes configured yet.</p>'
            )

    # ─────────────────────────────────────────────────────────────────────────
    # ACTION METHODS  (called by "More info →" buttons)
    # ─────────────────────────────────────────────────────────────────────────

    def _asset_action(self, domain, name='Assets'):
        """Return a filtered asset list action."""
        action = self.env['ir.actions.act_window']._for_xml_id(
            'asset_management.action_asset_asset')
        action['name'] = name
        action['domain'] = domain
        action['context'] = {}
        return action

    def action_view_insurance(self):
        return self._asset_action(
            [('is_insurance', '=', True)], 'Assets with Insurance')

    def action_view_premium_this_month(self):
        from datetime import date as _d
        today = _d.today()
        first = today.replace(day=1)
        if today.month == 12:
            last = today.replace(day=31)
        else:
            import datetime
            last = (today.replace(month=today.month + 1, day=1)
                    - datetime.timedelta(days=1))
        return self._asset_action([
            ('is_insurance', '=', True),
            ('premium_date', '>=', str(first)),
            ('premium_date', '<=', str(last)),
        ], 'Premium This Month')

    def action_view_premium_done_this_month(self):
        from datetime import date as _d
        today = _d.today()
        first = today.replace(day=1)
        if today.month == 12:
            last = today.replace(day=31)
        else:
            import datetime
            last = (today.replace(month=today.month + 1, day=1)
                    - datetime.timedelta(days=1))
        return self._asset_action([
            ('is_insurance', '=', True),
            ('insurance_complete_date', '>=', str(first)),
            ('insurance_complete_date', '<=', str(last)),
        ], 'Premium Done This Month')

    def action_view_premium_overdue(self):
        return self._asset_action([
            ('is_insurance', '=', True),
            ('premium_date', '<', str(date.today())),
            ('is_premium_paid', '=', False),
        ], 'Premium Overdue (Not Paid)')

    def action_view_reminder_upcoming(self):
        return self._asset_action([
            ('is_reminder', '=', True),
            ('reminder_date', '>=', str(date.today())),
        ], 'Reminder Upcoming')

    def action_view_reminder_expired(self):
        return self._asset_action([
            ('is_reminder', '=', True),
            ('reminder_date', '<', str(date.today())),
        ], 'Reminder Expired')

    def action_view_state(self, state, label):
        return self._asset_action([('state', '=', state)], label)

    def action_view_active(self):
        return self.action_view_state('active', 'Active Assets')

    def action_view_new(self):
        return self.action_view_state('new', 'New Assets')

    def action_view_broken(self):
        return self.action_view_state('broken', 'Broken Assets')

    def action_view_faulty(self):
        return self.action_view_state('faulty', 'Faulty Assets')

    def action_view_idle(self):
        return self.action_view_state('idle', 'Idle Assets')

    def action_view_in_servicing(self):
        return self.action_view_state('in_servicing', 'In Servicing Assets')

    def action_view_listed_for_dismantle(self):
        return self.action_view_state('listed_for_dismantle', 'Listed for Dismantle')

    def action_view_sold(self):
        return self.action_view_state('sold', 'Sold Assets')

    def action_view_lost(self):
        return self.action_view_state('lost', 'Lost Assets')

    def action_view_archived(self):
        return self.action_view_state('archived', 'Archived Assets')

    def action_report_summary(self):
        return self._asset_action([], 'Asset Summary Report')

    def action_report_detail(self):
        return self._asset_action([], 'Asset Detail Report')

    # ── Class-wise Data (Replaces class_summary_html) ─────────────────────────
    class_ids = fields.Many2many(
        'asset.class',
        compute='_compute_class_ids',
        string='Asset Classes'
    )

    def _compute_class_ids(self):
        for rec in self:
            # Fetch all active classes to display on the dashboard
            rec.class_ids = self.env['asset.class'].search([('active', '=', True)]).ids
