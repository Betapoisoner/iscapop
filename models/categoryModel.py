from odoo import models, fields, api


class categoryModel(models.Model):
    _name = 'iscapop.category_model'
    _description = 'iscapop.category_model'
    _rec_name="name"
    
    name = fields.Char(
        string='Name',required=True
    )
    
    description = fields.Html(
        string='Description',help="This is where you put the description of the item."
    )
    
    category_parent_id = fields.Many2one(
        string='Parent category',
        comodel_name='iscapop.category_model',
        ondelete='restrict',
    )
    
    category_son_ids = fields.One2many(
        string='Sub categories',
        comodel_name='iscapop.category_model',
        inverse_name='category_parent_id',
    )
    
    
    item_ids = fields.Many2many(
        string='Items',
        comodel_name='iscapop.item_model',
    )
    
    
    