from odoo import models, fields, api


class itemDetailsModel(models.Model):
    _name = 'iscapop.item_details_model'
    _description = 'iscapop.item_details_model'

    condition = fields.Selection(
        selection=[('new','New'),('good', 'Good'), ('bad', 'Bad')],string="Condition",required=True,dafault='good'
    )
    
    item_id = fields.Many2one(
        string='Item',
        comodel_name='iscapop.item_model',
        ondelete='restrict',
    )
    
    stock = fields.Integer(
        string='Full Stock',help="Here you put see many items of this condition you have in total "   )
    
    warranty = fields.Binary(string='Warranty',help="Here you out any warranty related files", attachment=True,required=True)
    
    additional_files=fields.Binary(string='Additional files', help="Here you put any file thet you think it's necessary",attachment=True)