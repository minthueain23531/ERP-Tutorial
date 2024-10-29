# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):

    _inherit = "res.users"

    multi_warehouse_id = fields.Many2many('stock.warehouse', 'stock_warehouse_rel', 'user_id', 'warehouse_id', string="Warehouses")



