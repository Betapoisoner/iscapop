from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class donationModel(models.Model):
    _name = "iscapop.donation_model"
    _description = "Donation Management"

    name = fields.Char(
        string="Donation Reference",
        readonly=True,
        default=lambda self: _("New"),
        compute="_compute_donation_name",
        store=True,
    )

    state = fields.Selection(
        [
            ("available", "Available"),
            ("reserved", "Reserved"),
            ("completed", "Completed"),
        ],
        string="Status",
        default="available",
        tracking=True,
    )
    item_id = fields.Many2one("iscapop.item_details_model", required=True)
    donator = fields.Many2one(
        "res.users", "Donator", default=lambda self: self.env.user
    )
    receiver = fields.Many2one("res.users", "Receiver")
    active = fields.Boolean(default=True)
    create_date = fields.Datetime(default=lambda self: fields.Datetime.now())
    target_location_id = fields.Many2one(
        "iscapop.location_model", string="Destination Location"
    )

    def action_claim_donation(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Claim Donation",
            "res_model": "iscapop.claim_wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_donation_id": self.id},
        }

    def action_complete_donation(self):
        self.ensure_one()
        if self.donator != self.env.user:
            raise ValidationError(
                _("Only the donation creator can complete this donation!")
            )

        if not self.target_location_id:
            raise ValidationError(
                _("Target location must be set to complete the donation.")
            )

        # Bypass security checks for location access
        target_location = self.target_location_id.sudo()

        # Check if receiver already has this item in target location
        existing_detail = (
            self.env["iscapop.item_details_model"]
            .sudo()
            .search(
                [
                    ("item_id", "=", self.item_id.item_id.id),
                    ("location_id", "=", target_location.id),
                    ("condition", "=", self.item_id.condition),
                    ("create_uid", "=", self.receiver.id),
                ],
                limit=1,
            )
        )

        if existing_detail:
            # Increment existing stock
            existing_detail.stock += self.item_id.stock
            self.item_id.sudo().unlink()  # Remove donor's copy
        else:
            # Create new receiver-owned item detail
            new_detail = self.item_id.copy(
                {
                    "location_id": target_location.id,
                    "create_uid": self.receiver.id,
                    "reserved": False,
                    "active": True,
                }
            )
            self.item_id.sudo().write({"active": False})  # Archive donor's copy

        self.write({"state": "completed"})
        return {
            "type": "ir.actions.report",
            "report_name": "iscapop.report_donation_completion",
            "report_type": "qweb-pdf",
            "docs": self,
            "context": {"discard_logo_check": True},
        }

    @api.depends("item_id")
    def _compute_donation_name(self):
        for record in self:
            if record.item_id:
                record.name = f"DON-{record.item_id.item_id.name}-{record.id}"
            else:
                record.name = _("New")
