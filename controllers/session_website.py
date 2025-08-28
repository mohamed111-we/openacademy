from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class CustomPortal(CustomerPortal):

    @http.route('/my/session', methods=['POST', 'GET'], type='http', auth='user', website=True)
    def class_session_form(self, **kw):
        print(kw)
        if request.httprequest.method == 'POST':
            request.env['openacademy.session'].sudo().create({
                'session_name': kw.get('session_name'),
                'seats': 10,
            })
            return request.render('openacademy.template_thank_you')
        else:
            return request.render('openacademy.session_form')
