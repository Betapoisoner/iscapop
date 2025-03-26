from odoo import models, fields, api


class itemDetailsModel(models.Model):
    _name = 'iscapop.item_details_model'
    _description = 'iscapop.item_details_model'

    
    condition = fields.Selection(
        selection=[('new','New'),('good', 'Good'), ('bad', 'Bad')],
        string="Condition",
        required=True,
        default='good',
        tracking=True  # Changed from track_visibility='onchange'
    )
    
    state = fields.Selection(
        selection=[('stored','Stored'),('in_class','In Class'),('donating', 'Donating'),('retired','Retired')],
        string="State",
        required=True,
        default='in_class',
        compute='_compute_state',
        store=True,
        tracking=True  # Changed from track_visibility='onchange'
    )
    
    
    reserved = fields.Boolean(
        string='Reserved',
        readonly=True
    )
    
    
    item_id = fields.Many2one(
        string='Item',
        comodel_name='iscapop.item_model',
        ondelete='cascade',
    )
    
    location_id = fields.Many2one(
        string='Location',
        comodel_name='iscapop.location_model',
        ondelete='restrict',
    )
    
    donation_id = fields.Many2one(
        string='Donation',
        comodel_name='iscapop.donation_model',
        ondelete='restrict',
    )
    
    stock = fields.Integer(
        string='Stock',help="Here you put see many items of this condition you have in total "   )
    
    warranty = fields.Binary(string='Warranty',help="Here you out any warranty related files", attachment=True,required=True)
    
    additional_files=fields.Binary(string='Additional files', help="Here you put any file thet you think it's necessary",attachment=True)
        
        
    def action_mark_reserved(self):
        """Mark item as reserved"""
        for record in self:
            if record.state == 'in_class' and not record.reserved:
                record.reserved = True

    def action_unreserve(self):
        """Remove reservation"""
        for record in self:
            if record.reserved:
                record.reserved = False    
    @api.depends('location_id')
    def _compute_state(self):
        for record in self:
            if record.location_id.loc_type == 'warehouse':
                record.state = 'stored'
            elif record.location_id.loc_type == 'retire':
                record.state = 'retired'
            elif record.donation_id:
                record.state = 'donating'
            else:
                record.state = 'in_class'

