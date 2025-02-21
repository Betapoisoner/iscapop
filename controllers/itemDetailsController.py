# -*- coding: utf-8 -*-
import datetime
from odoo import http
from odoo.http import request
import json

import requests


class ItemDetailController(http.Controller):
    
    #Post Item Details
    @http.route(['/iscapop/add_item_details/'],methods=["POST"], auth='user',type="json")
    def addDetails(self,):
        try:
            uid = request.env.user.id
            if uid == None :
                data={
                    "status":400,
                    "error":'User Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
                
            item_details = http.request.httprequest.json
            
            
            result= http.request.env['iscapop.item_details_model'].create(item_details)
            data={
                    "status":201,
                    "data":result.id
                    }
            return http.Response(json.dumps(data),mimetype="application/json")
        except Exception as e:
            data={
                "status":400,
                "error":"Exception"
                }
            json_data = http.Response(json.dumps(data),mimetype="application/json")
            return json_data
        
    #Put Item Details
    @http.route('/iscapop/upd_item_details/<int:itemId>',methods=["PUT"], auth='user',type="json")
    def updItemDetails(self,itemId=None, **kw):
        try:
            response =         response = http.request.httprequest.json
            uid = request.env.user.id
            if uid == None :
                data={
                    "status":400,
                    "error":'User Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
            elif itemId == None:
                data={
                    "status":400,
                    "error":'Item Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
            elif itemId == None and uid ==None :
                data={
                    "status":400,
                    "error":'Item and user Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
            domain=[("id","=",itemId),("create_uid","=",uid)]
            item= http.request.env['iscapop.item_details_model'].search(domain)
            if item:
                item.write(response)
                result={
                    "status":201,
                    "data": item
                            
                    }
                json_data = http.Response(json.dumps(result),mimetype="application/json")
                return json_data
            else:
                data={
                "status":404,
                "error":"Item not found"
                }
            json_data = http.Response(json.dumps(data),mimetype="application/json")
            return json_data
        except Exception as e:
            data={
                "status":500,
                "error":"Exception"
                }
            json_data = http.Response(json.dumps(data),mimetype="application/json")
            return json_data
    #Delete Items Details
    @http.route('/iscapop/del_item_details/',methods=["DELETE"],auth='user',type="json")
    def delItemDetails(self,itemId=None, **kw):
        try:
            response = http.request.httprequest.json
            uid = request.env.user.id
            itemId=response['id']
            if uid == None :
                data={
                    "status":400,
                    "error":'User Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
            elif itemId == None:
                data={
                    "status":400,
                    "error":'Item Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
            elif itemId == None and uid ==None :
                data={
                    "status":400,
                    "error":'Item and user Id not given'
                    }
            domain=[("id","=",itemId),("create_uid","=",uid)]

            if http.request.env['iscapop.item_details_model'].search(domain).unlink():
                data={
                    "status":201,
                    "data":itemId
                }
            else:
                data={
                    "status":400,
                    "data":"Not Ereased"
                }
            json_data = http.Response(json.dumps(data),mimetype="application/json")
            return json_data
        except Exception as e:
            data={
                "status":400,
                "error":"Exception"
                }
            json_data = http.Response(json.dumps(data),mimetype="application/json")
            return json_data