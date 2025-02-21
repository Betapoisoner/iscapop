# -*- coding: utf-8 -*-
import datetime
from odoo import http
from odoo.http import request
import json

import requests


class LocationController(http.Controller):
    #Get locations
    @http.route(['/iscapop/get_locations/','/iscapop/get_locations/<int:locationId>'],methods=["GET"], auth='user')
    def getLocations(self,locationId=None,**kw):
        try:
            uid = request.env.user.id
            if uid == None and locationId==None:
                data={
                    "status":400,
                    "error":'User Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
            elif uid != None  and locationId==None:
                domain=[("create_uid","=",uid)]
            elif uid != None  and locationId!=None:
                domain=[("id","=",locationId),("create_uid","=",uid)]
            locations = http.request.env['iscapop.location_model'].search_read(domain,['id','name','description','loc_type','stock_full','details_ids'])
            for location in locations:
                details_list = []
                for detail_id in location.get('details_ids', []):
                    detail = http.request.env['iscapop.item_details_model'].search_read([("id", "=", detail_id)], ['id', 'condition', 'state', 'reserved', 'location_id', 'donation_id', 'stock'])
                    if detail:
                        detail_data=detail[0]
                        # Convert IDs to names for related fields within details

                        details_list.append(detail_data)  # Append the modified detail dictionary

                location['details_ids'] = details_list
                # Convert date fields
                for name, value in location.items():
                    if isinstance(value, datetime.date):
                        location[name] = value.strftime('%Y-%m-%d')

            data=location
            result = {
                "status": 200,
                "data": data
                }
            json_data = http.Response(json.dumps(result),mimetype="application/json")
            return json_data
        except Exception as e:
            data={
                "status":400,
                "error":"Exception"
                }
            json_data = http.Response(json.dumps(data),mimetype="application/json")
            return json_data
    
    #Post Locations
    @http.route(['/iscapop/add_location/'],methods=["POST"], auth='user')
    def addLocation(self,):
        try:
            
            uid = request.env.user.id
            if uid == None :
                data={
                    "status":400,
                    "error":'User Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
                
            location = http.request.httprequest.json
            result= http.request.env['iscapop.location_model'].create(location)
            data={
                    "status":201,
                    "data":result
                    }
            return http.Response(json.dumps(data),mimetype="application/json")
        except Exception as e:
            data={
                "status":400,
                "error":"Exception"
                }
            json_data = http.Response(json.dumps(data),mimetype="application/json")
            return json_data