from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class DonationModel(models.Model):
    _name = "iscapop.donation_model"
    _description = "Donation Management"
    _order = "create_date desc"

    name = fields.Char(
        string="Donation Reference",
        readonly=True,
        default=lambda self: _("New"),
        compute="_compute_donation_name",
        store=True,
        index=True,
    )
    receiver_item_id = fields.Many2one(
        "iscapop.item_details_model", string="Receiver's Item", tracking=True
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
        group_expand="_expand_states",
    )
    item_id = fields.Many2one(
        "iscapop.item_details_model",
        required=True,
        string="Donated Item",
        domain="[('state', '=', 'stored')]",
    )
    donator = fields.Many2one(
        "res.users", "Donator", default=lambda self: self.env.user, readonly=True
    )
    receiver = fields.Many2one("res.users", "Receiver", readonly=True)
    active = fields.Boolean(default=True)
    create_date = fields.Datetime(
        default=lambda self: fields.Datetime.now(), readonly=True
    )
    target_location_id = fields.Many2one(
        "iscapop.location_model",
        string="Destination Location",
        domain="[('loc_type', 'in', ['class', 'warehouse'])]",
    )

    def action_open_claim_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Claim Donation",
            "res_model": "iscapop.claim_wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_donation_id": self.id,
                "default_item_id": self.item_id.id,
            },
        }


    def action_complete_donation(self):
        self.ensure_one()
        if self.donator != self.env.user:
            raise UserError(_("Only the donation creator can complete this donation!"))
        if self.state != "reserved":
            raise UserError(_("Can only complete reserved donations!"))
        if not self.target_location_id:
            raise UserError(_("Target location must be set to complete the donation!"))

        # Clear donation reference from original item
        original_item = self.item_id
        original_item.write({'donation_id': False})  # Add this line

        # Transfer stock logic
        if self.receiver_item_id:
            self.receiver_item_id.write({
                "stock": self.receiver_item_id.stock + original_item.stock,
                "location_id": self.target_location_id.id,
            })
            original_item.write({'active': False})
        else:
            target_location = self.target_location_id
            existing_detail = self.env["iscapop.item_details_model"].search([
                ("item_id", "=", original_item.item_id.id),
                ("location_id", "=", target_location.id),
                ("condition", "=", original_item.condition),
            ], limit=1)

            if existing_detail:
                existing_detail.stock += original_item.stock
                original_item.write({'active': False})
            else:
                # Create new detail without donation reference
                original_item.copy({
                    "location_id": target_location.id,
                    "create_uid": self.receiver.id,
                    "donation_id": False  # Add this line
                })
                original_item.write({'active': False})

        self.write({"state": "completed"})
        return self._generate_donation_report()

    def _generate_donation_report(self):
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
                base_name = record.item_id.item_id.name or _("Unnamed Item")
                record.name = f"DON-{base_name}-{record.id}"
            else:
                record.name = _("New")

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]
