# -*- coding: utf-8 -*-
# from odoo import http


# class GvaSalud(http.Controller):
#     @http.route('/gva_salud/gva_salud', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gva_salud/gva_salud/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gva_salud.listing', {
#             'root': '/gva_salud/gva_salud',
#             'objects': http.request.env['gva_salud.gva_salud'].search([]),
#         })

#     @http.route('/gva_salud/gva_salud/objects/<model("gva_salud.gva_salud"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gva_salud.object', {
#             'object': obj
#         })
