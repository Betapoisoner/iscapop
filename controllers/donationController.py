import datetime
from odoo import http
from odoo.http import request
import json

import requests


class DonationController(http.Controller):
    # Get donaciones
    @http.route(['/iscapop/get_donations/', '/iscapop/get_donations/<int:donationId>'], methods=["GET"], auth='user')
    def getDonaciones(self, donationId=None, **kw):
        try:
            uid = request.env.user.id
            if uid == None and donationId == None:
                data = {
                    "status": 400,
                    "error": 'User Id not given'
                }
                json_data = http.Response(json.dumps(
                    data), mimetype="application/json")
                return json_data
            elif uid != None and donationId == None:
                domain = [("create_uid", "=", uid)]
            elif uid != None and donationId != None:
                domain = [("id", "=", donationId), ("create_uid", "=", uid)]
            donations = http.request.env['iscapop.donation_model'].search_read(
                domain, ['id', 'name', 'item_id', 'donator', 'receiver'])
            for donation in donations:
                # Convert date fields
                for name, value in donation.items():
                    if isinstance(value, datetime.date):
                        donation[name] = value.strftime('%Y-%m-%d')

            data = donations
            result = {
                "status": 200,
                "data": data
            }
            json_data = http.Response(json.dumps(
                result), mimetype="application/json")
            return json_data
        except Exception as e:
            data = {
                "status": 400,
                "error": "Exception"
            }
            json_data = http.Response(json.dumps(
                data), mimetype="application/json")
            return json_data

    # Post Donations
    @http.route(['/iscapop/add_donation/'], methods=["POST"], auth='user', type="json")
    def addLocation(self,):
        try:
            uid = request.env.user.id
            if uid == None:
                data = {
                    "status": 400,
                    "error": 'User Id not given'
                }
                json_data = http.Response(json.dumps(
                    data), mimetype="application/json")
                return json_data

            donation = http.request.httprequest.json

            result = http.request.env['iscapop.donation_model'].create(
                donation)
            data = {
                "status": 201,
                "data": result.id
            }
            return http.Response(json.dumps(data), mimetype="application/json")
        except Exception as e:
            data = {
                "status": 400,
                "error": "Exception"
            }
            json_data = http.Response(json.dumps(
                data), mimetype="application/json")
            return json_data
