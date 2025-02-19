# -*- coding: utf-8 -*-
import datetime
from odoo import http
import json

import requests


class Iscapop(http.Controller):

    #Get items
    @http.route(['/iscapop/get_items/','/iscapop/get_items/<int:itemId>'],methods=["GET"], auth='user')
    def getItems(self,itemId=None,uid=None, **kw):
        try:
            response = http.request.httprequest.json
            uid = response.uid
            if uid == None and itemId==None:
                domain=[]
                data={
                    "status":400,
                    "error":'User Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
                
            elif uid != None  and itemId==None:
                domain=[("create_uid","=",uid)]
            elif uid != None  and itemId!=None:
                domain=[("id","=",itemId),("create_uid","=",uid)]
            items = http.request.env['iscapop.item_model'].sudo().search_read(domain,['id','name','description','stock_full','details_ids','category_id'])
            for item in items:
                details_list = []
                for detail_id in item.get('details_ids', []):
                    detail = http.request.env['iscapop.item_details_model'].sudo().search_read([("id", "=", detail_id)], ['id', 'condition', 'state', 'reserved', 'location_id', 'donation_id', 'stock'])
                    if detail:
                        detail_data=detail[0]
                        # Convert IDs to names for related fields within details

                        details_list.append(detail_data)  # Append the modified detail dictionary

                item['details_ids'] = details_list  # Assign the list of details back to the item

                # Convert date fields
                for name, value in item.items():
                    if isinstance(value, datetime.date):
                        item[name] = value.strftime('%Y-%m-%d')

            data=items
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
            donations = http.request.env['iscapop.donation_model'].sudo().search_read(domain,['id','name','item_id','donator','receiver'])
            for donation in donations:
                # Convert date fields
                for name, value in donation.items():
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
    
    #Get locations
    @http.route(['/iscapop/get_locations/','/iscapop/get_locations/<int:locationId>'],methods=["GET"], auth='user')
    def getLocations(self,locationId=None,uid=None, **kw):
        try:
            response = http.request.httprequest.json
            uid = response.uid
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
            locations = http.request.env['iscapop.location_model'].sudo().search_read(domain,['id','name','description','loc_type','stock_full','details_ids'])
            for location in locations:
                details_list = []
                for detail_id in location.get('details_ids', []):
                    detail = http.request.env['iscapop.item_details_model'].sudo().search_read([("id", "=", detail_id)], ['id', 'condition', 'state', 'reserved', 'item_id', 'donation_id', 'stock'])
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
                "error":e
                }
            json_data = http.Response(json.dumps(data),mimetype="application/json")
            return json_data
    
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
            categories = http.request.env['iscapop.category_model'].sudo().search_read(domain,['id','name','complete_name','description','item_ids'])
            for category in categories:
                items_list=[]
                for item_id in category['item_ids']:
                    item = http.request.env['iscapop.item_model'].sudo().search_read([("id", "=", item_id)], ['id','name','description','stock_full','details_ids'])
                    if item:
                        item_data=item[0]
                        details_list = []
                        for detail_id in item_data.get('details_ids', []):
                            detail = http.request.env['iscapop.item_details_model'].sudo().search_read([("id", "=", detail_id)], ['id', 'condition', 'state', 'reserved', 'location_id', 'donation_id', 'stock'])
                            if detail:
                                detail_data=detail[0]
                            # Convert IDs to names for related fields within details

                            details_list.append(detail_data)  # Append the modified detail dictionary

                        item_data['details_ids'] = details_list  # Assign the list of details back to the item
                        items_list.append(item_data)  # Append the modified detail dictionary
                
                category['item_ids'] = items_list  # Assign the list of details back to the item

                
                # Convert date fields
                for name, value in category.items():
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
                "error":e
                }
            json_data = http.Response(json.dumps(data),mimetype="application/json")
            return json_data
        
    #Post items
    @http.route(['/iscapop/add_items/'],methods=["POST"], auth='user')
    def addProduct(self,uid=None):
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
                
            item = http.request.httprequest.json
            response['uid']=uid
            
            result= http.request.env['iscapop.item_model'].create(item)
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
    
    @http.route(['/iscapop/add_items_details/'],methods=["POST"], auth='user')
    def addProduct(self,uid=None):
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
                "error":e
                }
            json_data = http.Response(json.dumps(data),mimetype="application/json")
            return json_data
        
        
    #Post Locations
    #Post Donations
    
    #Put Items
    #Put item Change Location
    #Put Categories
    
    #Delete Items
    #Delete Categories