import datetime
from odoo import http
from odoo.http import request
import json



class ItemController(http.Controller):
    #Get items
    @http.route(['/iscapop/get_items/','/iscapop/get_items/<int:itemId>'], auth='user',type="http")
    def getItems(self,itemId=None, **kw):
        try:
            uid = request.env.user.id
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
            items = http.request.env['iscapop.item_model'].search_read(domain,['id','name','description','stock_full','details_ids','category_id'])
            for item in items:
                details_list = []
                for detail_id in item.get('details_ids', []):
                    detail = http.request.env['iscapop.item_details_model'].search_read([("id", "=", detail_id)], ['id', 'condition', 'state', 'reserved', 'location_id', 'donation_id', 'stock'])
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
                "error":"Exception"
                }
            json_data = http.Response(json.dumps(data),mimetype="application/json")
            return json_data
        
        #Post items
    @http.route(['/iscapop/add_item/'],methods=["POST"], auth='user',type="json")
    def additem(self):
        try:
            uid = request.env.user.id
            if uid == None :
                data={
                    "status":400,
                    "error":'User Id not given'
                    }
                json_data = http.Response(json.dumps(data),mimetype="application/json")
                return json_data
                
            item = http.request.httprequest.json
            
            
            result= http.request.env['iscapop.item_model'].create(item)
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
    
    #Put Items
    @http.route('/iscapop/upd_item/<int:itemId>',type="json",methods=["PUT"], auth='user')
    def updItem(self,itemId=None, **kw):
        try:
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
            item= http.request.env['iscapop.item_model'].search(domain)
            if item:
                response = http.request.httprequest.json
                item.write(response)
                result={
                    "status":201,
                    "data":  item.id,
                            
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

#Delete Items
    @http.route('/iscapop/del_item/',type="json",methods=["DELETE"],auth='user')
    def delClients(self,itemId=None, **kw):
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

            if http.request.env['iscapop.item_model'].search(domain).unlink():
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