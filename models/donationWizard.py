from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DonationWizard(models.TransientModel):
    _name = "iscapop.donation_wizard"
    _description = "Donation Wizard"

    item_id = fields.Many2one("iscapop.item_model", string="Item")

    quantity = fields.Integer(required=True, default=1)
    available_stock = fields.Integer(
        string="Available Stock", compute="_compute_available_stock", readonly=True
    )
    condition = fields.Selection(
        selection=[("new", "New"), ("good", "Good"), ("bad", "Bad")],
        string="Item Condition",
        required=True,
    )

    @api.depends("condition")
    def _compute_available_stock(self):
        for record in self:
            details = self.env["iscapop.item_details_model"].search(
                [
                    ("item_id", "=", record.item_id.id),
                    ("condition", "=", record.condition),
                    ("state", "=", "stored"),
                    ("reserved", "=", False),
                ]
            )
            record.available_stock = sum(details.mapped("stock"))

    def action_donate(self):
        self.ensure_one()
        if self.quantity <= 0:
            raise ValidationError(_("Quantity must be greater than zero!"))

        if self.available_stock < self.quantity:
            raise ValidationError(_("Not enough available items for this condition!"))
        available_details = self.env["iscapop.item_details_model"].search(
            [
                ("item_id", "=", self.item_id.id),
                ("condition", "=", self.condition),
                ("state", "=", "stored"),  
                ("reserved", "=", False),
            ],
            order="id",
        )
        remaining_qty = self.quantity
        for detail in available_details:
            if remaining_qty <= 0:
                break
            deduct_qty = min(remaining_qty, detail.stock)
            new_detail = self.env["iscapop.item_details_model"].create(
                {
                    "item_id": self.item_id.id,
                    "condition": self.condition,
                    "stock": deduct_qty,
                    "state": "donating",
                }
            )
            self.env["iscapop.donation_model"].create(
                {
                    "item_id": new_detail.id,
                    "donator": self.env.user.id,
                    "state": "available",
                }
            )
            detail.stock -= deduct_qty
            if detail.stock <= 0:
                detail.unlink()
            remaining_qty -= deduct_qty
        message = _("Successfully donated %s %s items!") % (
            self.quantity,
            self.condition,
        )
        return {
            "type": "ir.actions.act_window_close",
            "effect": {"type": "rainbow_man", "message": message},
        }
