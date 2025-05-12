from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TransferWizard(models.TransientModel):
    _name = "iscapop.transfer_wizard"
    _description = "Item Transfer Wizard"

    state = fields.Selection(
        [
            ("select_source", "Select Source"),
            ("select_destination", "Select Destination"),
        ],
        default="select_source",
    )

    # Step 1 Fields
    item_id = fields.Many2one(
        "iscapop.item_model",
        string="Item",
        required=True,
        default=lambda self: self.env.context.get("active_id"),
    )
    condition = fields.Selection(
        selection=[("new", "New"), ("good", "Good"), ("bad", "Bad")],
        string="Condition",
        required=True,
    )
    source_location_id = fields.Many2one(
        "iscapop.location_model",
        string="From Location",
        required=True,
        domain="[('create_uid', '=', uid), ('loc_type', '!=', 'retire')]",
    )

    # Step 2 Fields
    destination_location_id = fields.Many2one(
        "iscapop.location_model",
        string="To Location",
        domain="[('create_uid', '=', uid), ('id', '!=', source_location_id)]",
    )
    quantity = fields.Integer(string="Quantity to Transfer", required=True, default=1)
    available_stock = fields.Integer(
        string="Available Stock", compute="_compute_available_stock", readonly=True
    )

    source_current_stock = fields.Integer(
        "Current Source Stock",
        compute="_compute_stock_values",
        help="Current stock in source location",
    )

    destination_current_stock = fields.Integer(
        "Current Destination Stock",
        compute="_compute_stock_values",
        help="Current stock in destination location",
    )

    projected_source_stock = fields.Integer(
        "Projected Source Stock",
        compute="_compute_stock_values",
        help="Source stock after transfer",
    )

    projected_destination_stock = fields.Integer(
        "Projected Destination Stock",
        compute="_compute_stock_values",
        help="Destination stock after transfer",
    )

    @api.depends(
        "source_location_id", "destination_location_id", "quantity", "condition"
    )
    def _compute_stock_values(self):
        for record in self:
            # Source calculations
            source_details = self.env["iscapop.item_details_model"].search(
                [
                    ("item_id", "=", record.item_id.id),
                    ("location_id", "=", record.source_location_id.id),
                    ("condition", "=", record.condition),
                ]
            )
            record.source_current_stock = sum(source_details.mapped("stock"))
            record.projected_source_stock = max(
                record.source_current_stock - record.quantity, 0
            )

            # Destination calculations
            dest_details = self.env["iscapop.item_details_model"].search(
                [
                    ("item_id", "=", record.item_id.id),
                    ("location_id", "=", record.destination_location_id.id),
                    ("condition", "=", record.condition),
                ]
            )
            record.destination_current_stock = sum(dest_details.mapped("stock"))
            record.projected_destination_stock = (
                record.destination_current_stock + record.quantity
            )

    @api.depends("item_id", "source_location_id", "condition")
    def _compute_available_stock(self):
        for record in self:
            if all([record.item_id, record.source_location_id, record.condition]):
                details = self.env["iscapop.item_details_model"].search(
                    [
                        ("item_id", "=", record.item_id.id),
                        ("location_id", "=", record.source_location_id.id),
                        ("condition", "=", record.condition),
                    ]
                )
                record.available_stock = sum(details.mapped("stock"))
            else:
                record.available_stock = 0

    def action_next(self):
        self.ensure_one()
        if self.available_stock < 1:
            raise ValidationError(
                _("No available stock for this condition in selected location!")
            )
        self.state = "select_destination"
        return self._reopen_wizard()

    def action_back(self):
        self.ensure_one()
        self.state = "select_source"
        return self._reopen_wizard()

    def _reopen_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

    @api.constrains("source_location_id", "destination_location_id")
    def _check_locations(self):
        for record in self:
            if record.source_location_id == record.destination_location_id:
                raise ValidationError(
                    _("Source and destination locations cannot be the same!")
                )

    @api.constrains("quantity")
    def _check_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError(_("Quantity must be greater than zero!"))
            if record.quantity > record.available_stock:
                raise ValidationError(_("Not enough stock available!"))

    def action_transfer(self):
        self.ensure_one()
        # Get all matching details in source location
        source_details = self.env["iscapop.item_details_model"].search(
            [
                ("item_id", "=", self.item_id.id),
                ("location_id", "=", self.source_location_id.id),
                ("condition", "=", self.condition),
            ]
        )

        remaining_qty = self.quantity

        for detail in source_details:
            if remaining_qty <= 0:
                break

            transfer_qty = min(remaining_qty, detail.stock)

            # Find existing detail in destination with same condition
            destination_detail = self.env["iscapop.item_details_model"].search(
                [
                    ("item_id", "=", self.item_id.id),
                    ("condition", "=", self.condition),
                    ("location_id", "=", self.destination_location_id.id),
                ],
                limit=1,
            )

            if destination_detail:
                # Add to existing detail
                destination_detail.stock += transfer_qty
            else:
                # Create new detail
                self.env["iscapop.item_details_model"].create(
                    {
                        "item_id": self.item_id.id,
                        "condition": self.condition,
                        "location_id": self.destination_location_id.id,
                        "stock": transfer_qty,
                        "warranty": detail.warranty,
                    }
                )

            # Update source detail
            detail.stock -= transfer_qty
            if detail.stock <= 0:
                detail.unlink()

            remaining_qty -= transfer_qty

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Transfer Complete"),
                "message": _("Moved %(qty)s units from %(src)s to %(dest)s")
                % {
                    "qty": self.quantity,
                    "src": self.source_location_id.name,
                    "dest": self.destination_location_id.name,
                },
                "sticky": False,
                "next": {"type": "ir.actions.act_window_close"},
            },
        }
