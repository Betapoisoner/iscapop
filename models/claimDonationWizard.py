from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ClaimDonationWizard(models.TransientModel):
    _name = "iscapop.claim_wizard"
    _description = "Claim Donation Wizard"

    donation_id = fields.Many2one("iscapop.donation_model", required=True)
    item_id = fields.Many2one("iscapop.item_details_model", string="Item")
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

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if self.env.context.get("active_id"):
            donation = self.env["iscapop.donation_model"].browse(
                self.env.context["active_id"]
            )
            if donation.donator == self.env.user:
                raise UserError(_("You cannot claim your own donation!"))
            if donation.state != "available":
                raise UserError(_("Only available donations can be claimed!"))
        return res

    def action_confirm_claim(self):
        self.ensure_one()
        if self.item_option == "new":
            # Create new item and detail
            new_item = self.env["iscapop.item_model"].create(
                {
                    "name": self.new_item_name,
                    "description": self.new_item_description,
                    "category_id": self.new_item_category_id.id,
                }
            )
            new_detail = self.env["iscapop.item_details_model"].create(
                {
                    "item_id": new_item.id,
                    "condition": self.donation_id.item_id.condition,
                    "location_id": self.target_location_id.id,
                    "stock": 0,  # Stock will be added when donation is completed
                }
            )
            self.donation_id.receiver_item_id = new_detail.id
        elif self.item_option == "existing":
            # Assign selected item detail to the donation
            self.donation_id.receiver_item_id = self.item_id.id

        # Update donation state and receiver
        self.donation_id.write(
            {
                "state": "reserved",
                "receiver": self.env.user.id,
                "target_location_id": self.target_location_id.id,
            }
        )
        return {
            "type": "ir.actions.act_window",
            "res_model": "iscapop.donation_model",
            "view_mode": "form",
            "res_id": self.donation_id.id,
        }
