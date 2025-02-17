from odoo import models, fields, api


class donationWizard(models.TransientModel):
    _name = 'iscapop.donation_wizard'
    _description = 'iscapop.donation_wizard'


    name = fields.Char(string="Name",help="This is where you put the name of the item.",
        compute='_compute_name',store=True)
    
    item_id = fields.Many2one(
        string='Item',
        comodel_name='iscapop.item_details_model',
        ondelete='restrict',
    )
    
    photo = fields.Binary(
        string='Photo',help="Here you put a photo of the item"
    )
    
    donator = fields.Many2one('res.users', 'Donator', default=lambda self: self.env.user,readonly=True)
    
    receiver =  fields.Many2one('res.users', 'Donator',readonly=True)

    @api.depends('item_id')
    def _compute_name(self):
        for record in self:
            for item in record.item_id:
                name=item.item_id.name
                record.name=name

