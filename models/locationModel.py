from asyncio import exceptions
from odoo import models, fields, api


class locationModel(models.Model):
    _name = 'iscapop.location_model'
    _description = 'iscapop.location_model'
    _rec_name="name"
        

    name = fields.Char(string="Name",default="Item",help="This is where you put the name of the location.",required=True)
    
    description = fields.Html(
        string='Description',help="This is where you put the description of the location."
    )
    
    loc_type = fields.Selection(
        selection=[('class','Class'),('warehouse', 'Warehouse'),('retire','Retire Room')],
        string="Type",
        required=True,
        default='class',
    )
    
    stock_full = fields.Integer(
        string='Full Stock',help="Here you put see many items of this you have in this location ",compute='_compute_stock_total',store=True
    )
    
    details_ids = fields.One2many(
        string='Items',
        comodel_name='iscapop.item_details_model',
        inverse_name='location_id',
        
        
        
    )
            
    @api.depends('details_ids')
    def _compute_stock_total(self):
        for record in self:
            temp=0
            for details in record.details_ids:
                if details.condition!='bad' :
                    temp+=details.stock
            if temp!=record.stock_full:
                record.stock_full=temp

