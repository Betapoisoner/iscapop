from odoo import models, fields, api
class ClaimDonationWizard(models.TransientModel):
    _name = "iscapop.claim_wizard"
    _description = "Claim Management"

    donation_id = fields.Many2one("iscapop.donation_model", required=True)
    target_location_id = fields.Many2one(
        "iscapop.location_model",
        "Destination Location",
        required=True,
        domain="[('loc_type', 'not in', ['retire'])]",
    )

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
