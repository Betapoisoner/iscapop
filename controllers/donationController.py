import datetime
from odoo import http
import json

import requests


class DonationController(http.Controller):
    #Get donaciones
    @http.route(['/iscapop/get_donations/','/iscapop/get_donations/<int:donationId>'],methods=["GET"], auth='user')
    def getDonaciones(self,donationId=None,uid=None, **kw):
        try:
            response = http.request.httprequest.json
            uid = response.uid
            if uid == None and donationId==None:
                data={
                    "status":400,
                    "error":'User Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
            elif uid != None  and donationId==None:
                domain=[("create_uid","=",uid)]
            elif uid != None  and donationId!=None:
                domain=[("id","=",donationId),("create_uid","=",uid)]
            donations = http.request.env['iscapop.donation_model'].sudo().search_read(domain,['id','name','donation_id','donator','receiver'])
            for donation in donations:
                # Convert date fields
                for name, value in donation.donations():
                    if isinstance(value, datetime.date):
                        donation[name] = value.strftime('%Y-%m-%d')

            data=donations
            result = {
                "status": 200,
                "data": data
                }
            json_data = http.Response(json.dumps(result),mimetype="application/json")
            return json_data
        except Exception as e:
            data={
                "status":400,
                "error":e
                }
            json_data = http.Response(json.dumps(data),mimetype="application/json")
            return json_data
        
    #Post Donations
    @http.route(['/iscapop/add_donation/'],methods=["POST"], auth='user')
    def addLocation(self,uid=None):
        try:
            response = http.request.httprequest.json
            uid = response.uid
            if uid == None :
                data={
                    "status":400,
                    "error":'User Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
                
            donation = http.request.httprequest.json
            response['uid']=uid
            
            result= http.request.env['iscapop.donation_model'].create(donation)
            data={
                    "status":201,
                    "data":result
                    }
            return http.Response(json.dumps(data),mimetype="application/json")
        except Exception as e:
            data={
                "status":400,
                "error":e
                }
            json_data = http.Response(json.dumps(data),mimetype="application/json")
            return json_data