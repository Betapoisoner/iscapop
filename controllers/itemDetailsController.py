# -*- coding: utf-8 -*-
import datetime
from odoo import http
import json

import requests


class ItemDetailController(http.Controller):
    
    #Post Item Details
    @http.route(['/iscapop/add_item_details/'],methods=["POST"], auth='user')
    def addDetails(self,uid=None):
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
                
            item_details = http.request.httprequest.json
            response['uid']=uid
            
            result= http.request.env['iscapop.item_model'].create(item_details)
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
        
    #Put Item Details
    @http.route('/iscapop/upd_item/<int:itemId>',type="json",methods=["PUT"], auth='user')
    def updItemDetails(self,uid=None,itemId=None, **kw):
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
                    "data":{
                            item,
                            }
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
    @http.route('/iscapop/del_item_details/',type="json",methods=["DELETE"],auth='public')
    def delItemDetails(self,uid=None,itemId=None, **kw):
        try:
            
            response = http.request.httprequest.json
            uid = response.uid
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