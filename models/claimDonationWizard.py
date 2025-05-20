from odoo import models, fields, api
class ClaimDonationWizard(models.TransientModel):
    _name = "iscapop.claim_wizard"
    _description = "Claim Management"

    item_id = fields.Many2one("iscapop.item_model", string="Item")
    donation_id = fields.Many2one("iscapop.donation_model", required=True)
    target_location_id = fields.Many2one(
        "iscapop.location_model",
        "Destination Location",
        required=True,
        domain="[('loc_type', 'not in', ['retire'])]",
    )
    item_option = fields.Selection(
        [("existing", "Existing Item"), ("new", "New Item")],
        string="Item Option",
        default="existing",
        required=True,
    )
    new_item_name = fields.Char(string="New Item Name")
    new_item_description = fields.Html(string="Description")
    new_item_category_id = fields.Many2one("iscapop.category_model", string="Category")

    def action_confirm_claim(self):
        self.ensure_one()
        self.donation_id.write(
            {
                "state": "reserved",
                "receiver": self.env.user.id,
                "target_location_id": self.target_location_id.id,  # Store target location
            }
        )
        return {
            "type": "ir.actions.act_window",
            "res_model": "iscapop.donation_model",
            "view_mode": "form",
            "res_id": self.donation_id.id,
        }
