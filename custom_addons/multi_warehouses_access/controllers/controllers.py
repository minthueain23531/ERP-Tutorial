# -*- coding: utf-8 -*-
# from odoo import http


# class MultiWarehousesAccess(http.Controller):
#     @http.route('/multi_warehouses_access/multi_warehouses_access', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/multi_warehouses_access/multi_warehouses_access/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('multi_warehouses_access.listing', {
#             'root': '/multi_warehouses_access/multi_warehouses_access',
#             'objects': http.request.env['multi_warehouses_access.multi_warehouses_access'].search([]),
#         })

#     @http.route('/multi_warehouses_access/multi_warehouses_access/objects/<model("multi_warehouses_access.multi_warehouses_access"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('multi_warehouses_access.object', {
#             'object': obj
#         })
