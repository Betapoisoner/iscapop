# -*- coding: utf-8 -*-
# from odoo import http


# class Custom-addons/iscapop(http.Controller):
#     @http.route('/custom-addons/iscapop/custom-addons/iscapop', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom-addons/iscapop/custom-addons/iscapop/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom-addons/iscapop.listing', {
#             'root': '/custom-addons/iscapop/custom-addons/iscapop',
#             'objects': http.request.env['custom-addons/iscapop.custom-addons/iscapop'].search([]),
#         })

#     @http.route('/custom-addons/iscapop/custom-addons/iscapop/objects/<model("custom-addons/iscapop.custom-addons/iscapop"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom-addons/iscapop.object', {
#             'object': obj
#         })

