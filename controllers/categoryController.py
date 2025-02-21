# -*- coding: utf-8 -*-
import datetime
from odoo import http
import json

import requests


class CategoryController(http.Controller):
    #Get Categories
    @http.route(['/iscapop/get_categories/','/iscapop/get_categories/<int:categoryId>'],methods=["GET"], auth='user')
    def getCategories(self,categoryId=None,uid=None, **kw):
        try:
            response = http.request.httprequest.json
            uid = response.uid
            if uid == None and categoryId==None:
                data={
                    "status":400,
                    "error":'User Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
            elif uid != None  and categoryId==None:
                domain=[("create_uid","=",uid)]
            elif uid != None  and categoryId!=None:
                domain=[("id","=",categoryId),("create_uid","=",uid)]
            categories = http.request.env['iscapop.category_model'].search_read(domain,['id','name','complete_name','description','category_ids'])
            for category in categories:
                categorys_list=[]
                for category_id in category['category_ids']:
                    category = http.request.env['iscapop.category_model'].search_read([("id", "=", category_id)], ['id','name','description','stock_full','details_ids'])
                    if category:
                        category_data=category[0]
                        details_list = []
                        for detail_id in category_data.get('details_ids', []):
                            detail = http.request.env['iscapop.category_details_model'].search_read([("id", "=", detail_id)], ['id', 'condition', 'state', 'reserved', 'location_id', 'donation_id', 'stock'])
                            if detail:
                                detail_data=detail[0]
                            # Convert IDs to names for related fields within details

                            details_list.append(detail_data)  # Append the modified detail dictionary

                        category_data['details_ids'] = details_list  # Assign the list of details back to the category
                        categorys_list.append(category_data)  # Append the modified detail dictionary
                
                category['category_ids'] = categorys_list  # Assign the list of details back to the category

                
                # Convert date fields
                for name, value in category.categorys():
                    if isinstance(value, datetime.date):
                        category[name] = value.strftime('%Y-%m-%d')

            data=categories
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
        
    #Post Categories
    @http.route(['/iscapop/add_category/'],methods=["POST"], auth='user')
    def addCategory(self,uid=None):
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
                
            category = http.request.httprequest.json
            response['uid']=uid
            
            result= http.request.env['iscapop.category_model'].create(category)
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
        
    #Put Categories
    @http.route('/iscapop/upd_location/<int:locationId>',type="json",methods=["PUT"], auth='user')
    def updLocation(self,uid=None,categoryId=None, **kw):
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
            elif categoryId == None:
                data={
                    "status":400,
                    "error":'Category Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
            elif categoryId == None and uid ==None :
                data={
                    "status":400,
                    "error":'Category and user Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
            domain=[("id","=",categoryId),("create_uid","=",uid)]
            category= http.request.env['iscapop.category_details_model'].search(domain)
            if category:
                category.write(response)
                result={
                    "status":201,
                    "data":{
                            category,
                            }
                    }
                json_data = http.Response(json.dumps(result),mimetype="application/json")
                return json_data
            else:
                data={
                "status":404,
                "error":"Category not found"
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
    
    #Delete Categories
    @http.route('/iscapop/del_category/',type="json",methods=["DELETE"],auth='public')
    def delCategory(self,uid=None,categoryId=None, **kw):
        try:
            
            response = http.request.httprequest.json
            uid = response.uid
            categoryId=response['id']
            if uid == None :
                data={
                    "status":400,
                    "error":'User Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
            elif categoryId == None:
                data={
                    "status":400,
                    "error":'Category Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
            elif categoryId == None and uid ==None :
                data={
                    "status":400,
                    "error":'Category and user Id not given'
                    }
            domain=[("id","=",categoryId),("create_uid","=",uid)]

            if http.request.env['iscapop.category_model'].search(domain).unlink():
                data={
                    "status":201,
                    "data":categoryId
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