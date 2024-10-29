# -*- coding: utf-8 -*-
import base64
import io
import logging
import os

from odoo import models, fields, api, tools, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.modules.module import get_resource_path
from random import randrange
from PIL import Image



class Branch(models.Model):
    _name = 'branch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'branch'

    def _get_logo(self):
        return base64.b64encode(open(os.path.join(tools.config['root_path'], 'addons', 'base', 'static', 'img', 'res_company_logo.png'), 'rb') .read())

    def _get_fav_icon(self, original=False):
        img_path = get_resource_path('web', 'static/img/favicon.ico')
        with tools.file_open(img_path, 'rb') as f:
            if original:
                return base64.b64encode(f.read())
            # Modify the source image to add a colored bar on the bottom
            # This could seem overkill to modify the pixels 1 by 1, but
            # Pillow doesn't provide an easy way to do it, and this
            # is acceptable for a 16x16 image.
            color = (randrange(32, 224, 24), randrange(32, 224, 24), randrange(32, 224, 24))
            original = Image.open(f)
            new_image = Image.new('RGBA', original.size)
            height = original.size[1]
            width = original.size[0]
            bar_size = 1
            for y in range(height):
                for x in range(width):
                    pixel = original.getpixel((x, y))
                    if height - bar_size <= y + 1 <= height:
                        new_image.putpixel((x, y), (color[0], color[1], color[2], 255))
                    else:
                        new_image.putpixel((x, y), (pixel[0], pixel[1], pixel[2], pixel[3]))
            stream = io.BytesIO()
            new_image.save(stream, format="ICO")
            return base64.b64encode(stream.getvalue())

    name = fields.Char('Name', tracking=True)
    code = fields.Char('Code', tracking=True)
    logo = fields.Binary(default=_get_logo, string='Branch Logo')
    favicon = fields.Binary(string='Branch Favicon', default=_get_fav_icon)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    street = fields.Char('street')
    street2 = fields.Char('street2')
    zip = fields.Char('zip')
    city = fields.Char('city')
    state_id = fields.Many2one('res.country.state', string="Fed. State")
    phone = fields.Char('Phone')
    mobile = fields.Char('Mobile')
    email = fields.Char('Email')

    @api.constrains('name', 'code')
    def _check_uniqueness(self):
        for record in self:
            existing_branch_name = self.search([('id', '!=', record.id), ('name', '=ilike', record.name)])
            if existing_branch_name:
                raise ValidationError(_('Branch Name %s already exist.Please use a different name.' % record.name))

            existing_branch_code = self.search([('id', '!=', record.id), ('code', '=ilike', record.code)])
            if existing_branch_code:
                raise ValidationError(_('Branch Code %s already exist.Please use a different name.' % record.code))

    @api.model
    def create(self, vals):
        if not vals.get('favicon'):
            vals['favicon'] = self._get_fav_icon()

        branch = super(Branch, self).create(vals)

        analytic_plan = self.env['account.analytic.plan'].create({'name': branch.name})

        analytic_account_vals = {
            'name': branch.name,
            'plan_id': analytic_plan.id
        }

        analytic_account = self.env['account.analytic.account'].create(analytic_account_vals)

        branch.write({'analytic_account_id': analytic_account.id})

        return branch


class ResUsers(models.Model):

    _inherit = "res.users"

    branch_ids = fields.Many2many('branch', 'branch_rel', 'user_id', 'branch_id', string="Allowed Branches")
    branch_id = fields.Many2one('branch','Default Branch')

    @api.constrains('branch_ids', 'branch_id')
    def _check_branch(self):
        for record in self:
            if record.branch_id not in record.branch_ids:
                raise ValidationError(_('Branch %(branch_name)s is not in the allowed branch for user %(user_name)s (%(branch_allowed)s).',
                    branch_name=record.branch_id.name,
                    user_name=record.name,
                    branch_allowed=', '.join(record.mapped('branch_ids.name')))
                )


