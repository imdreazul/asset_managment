# -*- coding: utf-8 -*-
import base64
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AssetAsset(models.Model):
    _name = 'asset.asset'
    _description = 'Asset'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'asset_name asc'
    _rec_name = 'asset_name'

    # ── Classification ────────────────────────────────────────────
    asset_class    = fields.Many2one('asset.class',    string='Asset Class',    required=True, tracking=True)
    asset_category = fields.Many2one('asset.category', string='Asset Category', tracking=True)
    asset_item     = fields.Many2one('asset.item',     string='Asset Item',     tracking=True)
    asset_brand    = fields.Many2one('asset.brand',    string='Brand',          tracking=True)
    asset_name     = fields.Char(string='Asset Name',  required=True,           tracking=True)
    asset_model    = fields.Char(string='Asset Model', tracking=True)
    description    = fields.Text(string='Description')
    remarks    = fields.Text(string='Remarks')

    state = fields.Selection([
        ('new',                  'New'),
        ('active',               'Active'),
        ('idle',                 'Idle'),
        ('in_servicing',         'In Servicing'),
        ('broken',               'Broken'),
        ('faulty',               'Faulty'),
        ('listed_for_dismantle', 'Listed for Dismantle'),
        ('sold',                 'Sold'),
        ('lost',                 'Lost'),
        ('archived',             'Archived'),
    ], string='State', default='active', tracking=True)

    is_premium_paid = fields.Boolean(
        string='Premium Paid',
        tracking=True,
        help='Mark when the current insurance premium has been paid.',
    )

    qty   = fields.Float(string='Quantity', default=1.0)
    image = fields.Image(string='Asset Image')

    # ── QR Code & Identification ──────────────────────────────────
    qr_number = fields.Char(
        string='QR Number', required=True, copy=False,
        readonly=True, default=lambda self: _('New'),
    )
    qr_code_image = fields.Image(string='QR Code Label', max_width=512, max_height=512)

    # ── References & Origins ──────────────────────────────────────
    bd_voucher    = fields.Char('BD Voucher',       tracking=True)
    jv_voucher    = fields.Char('JV Voucher',       tracking=True)
    supplier      = fields.Many2one('asset.supplier', string='Supplier', tracking=True)
    manufacture_sn = fields.Char('Manufacture S/N', tracking=True)
    purchase_date = fields.Date('Purchase Date',    tracking=True)
    f_year        = fields.Many2one('asset.financial.year', string='Financial Year', tracking=True)

    # ── Specifications ────────────────────────────────────────────

    asset_user = fields.Many2one('asset.user', string='User', tracking=True)
    color           = fields.Many2one('asset.color', string='Color', tracking=True)
    have_warranty   = fields.Boolean('Have Warranty?', tracking=True)
    warranty        = fields.Integer('Warranty (Months)', tracking=True)
    is_compound_asset = fields.Boolean('Is Compound Asset?', tracking=True)
    is_depreciation = fields.Boolean('Is Depreciation Applicable?', tracking=True)

    # ── Depreciation Configuration ────────────────────────────────
    depreciation_method = fields.Selection([
        ('reducing',      'Reducing Method'),
        ('straight_line', 'Straight Line'),
        ('km_per_hour',   'KM Per Hour'),
    ], string='Depreciation Method', tracking=True)

    depreciation_rate = fields.Float(
        string='Depreciation Rate (%)',
        digits=(16, 4),
        tracking=True,
        help='Annual rate as a percentage (e.g. 20 = 20% per annum). '
             'Not used for the KM/Per-Hour method.',
    )
    depreciation_start_date = fields.Date(
        string='Depreciation Start Date',
        tracking=True,
        help='Date from which depreciation begins.',
    )
    expected_km = fields.Float(
        string='Expected KM / Service / Copy (Total)',
        digits=(16, 2),
        tracking=True,
        help='Total expected life in KM, service count, or copy count. '
             'Used only for the KM/Per-Hour/Copy method.',
    )
    residual_value = fields.Float(
        string='Residual / Scrap Value',
        digits=(16, 2),
        tracking=True,
        help='Estimated salvage / residual value at end of asset life '
             '(e.g. value on transfer to employee).',
    )

    # ── Depreciation Lines ────────────────────────────────────────
    depreciation_line_ids = fields.One2many(
        'asset.depreciation.line', 'asset_id',
        string='Depreciation Schedule',
    )
    depreciation_line_count = fields.Integer(
        string='Lines',
        compute='_compute_depreciation_line_count',
    )

    # ── Compound Asset ────────────────────────────────────────────
    parent_asset_id = fields.Many2one(
        'asset.asset',
        string='Parent Asset',
        ondelete='set null',
        tracking=True,
        help='If this asset is a component, select the parent compound asset here.',
    )
    child_asset_ids = fields.One2many(
        'asset.asset',
        'parent_asset_id',
        string='Component Assets',
        help='Assets that make up this compound asset.',
    )
    component_count = fields.Integer(
        string='Components',
        compute='_compute_component_count',
        store=True,
    )

    # ── Financials ────────────────────────────────────────────────
    asset_value         = fields.Float('Asset Value',          tracking=True)
    other_cost          = fields.Float('Other Cost',           tracking=True)
    registration_amount = fields.Float('Registration Amount',  tracking=True)
    vat_amount          = fields.Float('VAT Amount',           tracking=True)
    installation_cost   = fields.Float('Installation Cost',    tracking=True)
    tds_amount          = fields.Float('TDS Amount',           tracking=True)
    insurance_cost      = fields.Float('Insurance Cost',       tracking=True)
    total = fields.Float('Total', compute='_compute_total', store=True)


    # _____ Insurance _______________________________________________

    is_insurance = fields.Boolean('Is Insurance?', tracking=True)
    insurance_partner_id = fields.Many2one('asset.insurance.partner', string='Insurance Partner')
    insurance_type = fields.Many2one('asset.insurance.type', string='Premium Type')
    initial_payment = fields.Float('Initial Payment/Premium Amount', tracking=True)
    premium_date = fields.Date('First Premium Date', tracking=True)
    insurance_complete_date = fields.Date('Insurance Complete on', tracking=True)
    claim_n_impact = fields.Text(string='Insurance Claim & Impact', tracking=True)


    is_reminder = fields.Boolean('Reminder', tracking=True)
    reminder_title = fields.Char('Reminder Title', tracking=True)
    reminder_type = fields.Selection([
        ('one_time',       'One Time Reminder'),
        ('recurrent',       'Recurrent Reminder'),
    ], string='Reminder Type', tracking=True)
    reminder_date = fields.Date('Reminder Date', tracking=True)


    # ── Locations & Organisation ──────────────────────────────────
    company             = fields.Many2one('asset.company',        string='Company',         tracking=True)
    division            = fields.Many2one('asset.division',       string='Division',        tracking=True)
    department          = fields.Many2one('asset.department',     string='Department',      tracking=True)
    office_location     = fields.Many2one('asset.office.location',string='Office Location', tracking=True)
    asset_floor_location= fields.Many2one('asset.floor.location', string='Floor Location',  tracking=True)

    # ── Many2Many ─────────────────────────────────────────────────
    services    = fields.Many2many('asset.service',   string='Services')
    tags        = fields.Many2many('asset.tag',       string='Tags')
    accessories = fields.Many2many('asset.accessory', string='Accessories')

    # ─────────────────────────────────────────────────────────────
    # COMPUTED
    # ─────────────────────────────────────────────────────────────
    # ─────────────────────────────────────────────────────────────
    # DEPRECIATION HELPERS
    # ─────────────────────────────────────────────────────────────
    def _compute_depreciation_line_count(self):
        for rec in self:
            rec.depreciation_line_count = len(rec.depreciation_line_ids)

    def action_propagate_dep_balances(self):
        """
        Re-links every depreciation line's opening balances to the
        previous line's closing balances (day-ordered).
        First line: cost opening = asset total, dep opening = 0.
        """
        for rec in self:
            lines = rec.depreciation_line_ids.sorted(
                key=lambda l: (l.date_from, l.id)
            )
            if not lines:
                return

            # First line seeds
            prev_cost_closing = rec.total
            prev_dep_closing  = 0.0

            for line in lines:
                line.write({
                    'cost_opening_balance': prev_cost_closing,
                    'dep_opening_balance':  prev_dep_closing,
                })
                # Read back after write so computed fields refresh
                prev_cost_closing = line.cost_closing_balance
                prev_dep_closing  = line.dep_closing_balance

        return {
            'type':    'ir.actions.client',
            'tag':     'display_notification',
            'params': {
                'title':   _('Balances Propagated'),
                'message': _(
                    'Opening balances have been recalculated from previous period closing balances.'
                ),
                'type':    'success',
                'sticky': False,
            },
        }

    def action_generate_dep_lines(self):
        """
        Opens a wizard to auto-generate depreciation schedule lines.
        (Wizard defined below as a transient model.)
        """
        self.ensure_one()
        if not self.is_depreciation:
            raise UserError(_('Please enable "Is Depreciation Applicable?" first.'))
        if not self.depreciation_method:
            raise UserError(_('Please select a Depreciation Method first.'))
        if not self.depreciation_start_date:
            raise UserError(_('Please set a Depreciation Start Date first.'))
        return {
            'type':    'ir.actions.act_window',
            'name':    _('Generate Depreciation Schedule'),
            'res_model': 'asset.depreciation.generate.wizard',
            'view_mode': 'form',
            'target':  'new',
            'context': {
                'default_asset_id':            self.id,
                'default_depreciation_method': self.depreciation_method,
                'default_date_from':           self.depreciation_start_date,
            },
        }

    @api.depends('asset_value', 'other_cost', 'registration_amount',
                 'vat_amount', 'installation_cost', 'tds_amount', 'insurance_cost')
    def _compute_total(self):
        for rec in self:
            rec.total = (
                rec.asset_value + rec.other_cost + rec.registration_amount
                + rec.vat_amount + rec.installation_cost
                + rec.tds_amount + rec.insurance_cost
            )

    @api.depends('child_asset_ids')
    def _compute_component_count(self):
        for rec in self:
            rec.component_count = len(rec.child_asset_ids)

    # ─────────────────────────────────────────────────────────────
    # ONCHANGE
    # ─────────────────────────────────────────────────────────────
    @api.onchange('is_compound_asset')
    def _onchange_is_compound_asset(self):
        """Clear children when compound flag is turned off."""
        if not self.is_compound_asset:
            self.child_asset_ids = [(5, 0, 0)]

    @api.onchange('asset_category')
    def _onchange_asset_category(self):
        self.asset_item = False

    # ─────────────────────────────────────────────────────────────
    # CONSTRAINTS
    # ─────────────────────────────────────────────────────────────
    @api.constrains('parent_asset_id', 'is_compound_asset')
    def _check_compound_loop(self):
        for rec in self:
            # A compound asset cannot be a component of itself
            if rec.parent_asset_id and rec.parent_asset_id == rec:
                raise UserError(_("An asset cannot be its own component."))
            # A compound asset parent must have is_compound_asset = True
            if rec.parent_asset_id and not rec.parent_asset_id.is_compound_asset:
                raise UserError(_(
                    "Parent asset '%s' must be marked as a Compound Asset first."
                ) % rec.parent_asset_id.asset_name)

    # ─────────────────────────────────────────────────────────────
    # CRUD
    # ─────────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('qr_number', _('New')) == _('New'):
                vals['qr_number'] = (
                    self.env['ir.sequence'].next_by_code('asset.asset.sequence') or _('New')
                )
        records = super().create(vals_list)
        for record in records:
            record.generate_composite_qr_code()
        return records

    def write(self, vals):
        if 'asset_class' in vals:
            for rec in self:
                if rec.asset_class and rec.asset_class.id != vals.get('asset_class'):
                    raise UserError(_(
                        "You cannot change the Asset Class after the asset has been created."
                    ))
        return super().write(vals)

    # ─────────────────────────────────────────────────────────────
    # QR CODE
    # ─────────────────────────────────────────────────────────────
    def generate_composite_qr_code(self):
        """
        Generates an image: Logo → QR Code → Category → QR Number.
        Canvas height computed after measuring every element (nothing clipped).
        """
        for record in self:
            if not record.qr_number:
                continue

            # 1. QR image
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=8, border=2,
            )
            qr.add_data(record.qr_number)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            qr_w, qr_h = qr_img.size

            PADDING = 20; GAP = 10; TOP_PAD = 10; BOTTOM_PAD = 14
            canvas_w = max(qr_w + PADDING * 2, 300)

            # 2. Logo
            logo_bg = None; logo_w = logo_h = 0
            logo_data = False
            if record.company and hasattr(record.company, 'logo') and record.company.logo:
                logo_data = base64.b64decode(record.company.logo)
            elif self.env.company and self.env.company.logo:
                logo_data = base64.b64decode(self.env.company.logo)
            if logo_data:
                try:
                    logo_img = Image.open(BytesIO(logo_data)).convert('RGBA')
                    logo_img.thumbnail((canvas_w - PADDING * 2, 60))
                    logo_w, logo_h = logo_img.size
                    logo_bg = Image.new('RGB', logo_img.size, (255, 255, 255))
                    logo_bg.paste(logo_img, mask=logo_img.split()[3])
                except Exception:
                    logo_bg = None; logo_w = logo_h = 0

            # 3. Fonts
            try:
                font      = ImageFont.truetype("arial.ttf",   20)
                font_bold = ImageFont.truetype("arialbd.ttf", 24)
            except IOError:
                font = font_bold = ImageFont.load_default()

            # 4. Measure text on throw-away surface
            category_name  = record.asset_category.name if record.asset_category else "Uncategorized"
            qr_number_text = record.qr_number
            _tmp  = Image.new('RGB', (canvas_w, 200))
            _draw = ImageDraw.Draw(_tmp)
            cat_bbox = _draw.textbbox((0, 0), category_name,  font=font)
            num_bbox = _draw.textbbox((0, 0), qr_number_text, font=font_bold)
            cat_h = cat_bbox[3] - cat_bbox[1]; cat_w = cat_bbox[2] - cat_bbox[0]
            num_h = num_bbox[3] - num_bbox[1]; num_w = num_bbox[2] - num_bbox[0]

            # 5. Exact canvas height
            canvas_h = TOP_PAD
            if logo_bg: canvas_h += logo_h + GAP
            canvas_h += qr_h + GAP + cat_h + GAP + num_h + BOTTOM_PAD

            # 6. Draw
            canvas    = Image.new('RGB', (canvas_w, canvas_h), 'white')
            draw      = ImageDraw.Draw(canvas)
            current_y = TOP_PAD
            if logo_bg:
                canvas.paste(logo_bg, ((canvas_w - logo_w) // 2, current_y))
                current_y += logo_h + GAP
            canvas.paste(qr_img, ((canvas_w - qr_w) // 2, current_y))
            current_y += qr_h + GAP
            draw.text(((canvas_w - cat_w) // 2, current_y), category_name,  font=font,      fill="black")
            current_y += cat_h + GAP
            draw.text(((canvas_w - num_w) // 2, current_y), qr_number_text, font=font_bold, fill="black")

            buf = BytesIO()
            canvas.save(buf, format="PNG")
            record.qr_code_image = base64.b64encode(buf.getvalue())

    # # ─────────────────────────────────────────────────────────────
    # # ODOO 18 — Thread access hook (required by discuss controller)
    # # ─────────────────────────────────────────────────────────────
    # @classmethod
    # def _get_thread_with_access(cls, thread_id, mode='read', **kwargs):
    #     return super()._get_thread_with_access(thread_id, mode=mode, **kwargs)
