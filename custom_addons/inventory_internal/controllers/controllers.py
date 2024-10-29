# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryInternal(http.Controller):
#     @http.route('/inventory_internal/inventory_internal', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_internal/inventory_internal/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_internal.listing', {
#             'root': '/inventory_internal/inventory_internal',
#             'objects': http.request.env['inventory_internal.inventory_internal'].search([]),
#         })

#     @http.route('/inventory_internal/inventory_internal/objects/<model("inventory_internal.inventory_internal"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_internal.object', {
#             'object': obj
#         })
