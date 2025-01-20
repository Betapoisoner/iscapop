from odoo import models, fields, api


class itemModel(models.Model):
    _name = 'iscapop.item_model'
    _description = 'iscapop.item_model'
    _rec_name="name"

    
    photo = fields.Binary(
        string='Photo',help="Here you put a photo of the item"
    )
    name = fields.Char(string="Name",default="Item",help="This is where you put the name of the item.",required=True)
    
    description = fields.Html(
        string='Description',help="This is where you put the description of the item."
    )
    stock_full = fields.Integer(
        string='Full Stock',help="Here you put see many items of this kind you have in total ",compute='_compute_stock_total',store=True
    )
    
    details_ids = fields.One2many(
        string='Details',
        comodel_name='iscapop.item_details_model',
        inverse_name='item_id',
    )
    
    category_ids = fields.Many2many(
        string='Categories',
        comodel_name='iscapop.category_model',
    )
    

    @api.depends('details_ids')
    def _compute_stock_total(self):
        temp=0
        for details in self.details_ids:
            if details.condition!='bad' :
                temp+=details.stock
        if temp!=self.stock_full:
            self.stock_full=temp
