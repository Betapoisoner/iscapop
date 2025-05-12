from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class itemDetailsModel(models.Model):
    _name = "iscapop.item_details_model"
    _description = "iscapop.item_details_model"
    _rec_name = "name"

    name = fields.Char(
        string="Name", compute="_compute_name", store=True, readonly=True
    )

    condition = fields.Selection(
        selection=[("new", "New"), ("good", "Good"), ("bad", "Bad")],
        string="Condition",
        required=True,
        default="good",
        tracking=True,
    )

    state = fields.Selection(
        selection=[
            ("stored", "Stored"),
            ("in_class", "In Class"),
            ("donating", "Donating"),
            ("retired", "Retired"),
        ],
        string="State",
        required=True,
        default="stored",
        compute="_compute_state",
        store=True,
        tracking=True,
    )

    reserved = fields.Boolean(string="Reserved", readonly=True, default=False)

    item_id = fields.Many2one(
        string="Item",
        comodel_name="iscapop.item_model",
        ondelete="cascade",
    )

    location_id = fields.Many2one(
        string="Location",
        comodel_name="iscapop.location_model",
        ondelete="restrict",
    )

    donation_id = fields.Many2one(
        string="Donation",
        comodel_name="iscapop.donation_model",
        ondelete="restrict",
    )

    stock = fields.Integer(
        string="Stock",
        help="Here you put see many items of this condition you have in total ",
    )

    warranty = fields.Binary(
        string="Warranty",
        help="Here you out any warranty related files",
        attachment=True,
        required=True,
    )
    active = fields.Boolean(string="Active", default=True)  # Add this line
    additional_files = fields.Binary(
        string="Additional files",
        help="Here you put any file thet you think it's necessary",
        attachment=True,
    )

    def get_location_stock(self, item_id, condition, location_id):
        return self.search(
            [
                ("item_id", "=", item_id),
                ("condition", "=", condition),
                ("location_id", "=", location_id),
            ]
        ).mapped("stock")

    def action_mark_reserved(self):
        """Mark item as reserved"""
        for record in self:
            if record.state == "in_class" and not record.reserved:
                record.reserved = True

    def action_unreserve(self):
        """Remove reservation"""
        for record in self:
            if record.reserved:
                record.reserved = False

    @api.constrains("reserved")
    def _check_reserved_operations(self):
        for record in self:
            if record.reserved and record.state != "donating":
                raise ValidationError("Can only reserve donated items!")

    @api.depends("donation_id.state")
    def _compute_reserved(self):
        for record in self:
            record.reserved = bool(
                record.donation_id and record.donation_id.state == "reserved"
            )

    @api.depends("donation_id", "location_id")
    def _compute_state(self):
        for record in self:
            if record.donation_id:
                record.state = "donating"
            else:
                if record.location_id.loc_type == "warehouse":
                    record.state = "stored"
                elif record.location_id.loc_type == "retire":
                    record.state = "retired"
                else:
                    record.state = "in_class"

    @api.depends("item_id.name", "state", "condition")
    def _compute_name(self):
        for record in self:
            parts = []
            if record.item_id:
                parts.append(record.item_id.name)

            # Get human-readable state value
            state_dict = dict(self._fields["state"].selection)
            state = state_dict.get(record.state, "")

            # Ensure state is a string
            if not isinstance(state, str):
                state = ""

            # Get human-readable condition value
            condition_dict = dict(self._fields["condition"].selection)
            condition = condition_dict.get(record.condition, "").title()

            if state and condition:
                parts.append(f"({state} - {condition})")
            elif state:
                parts.append(f"({state})")
            elif condition:
                parts.append(f"({condition})")

            record.name = " ".join(parts) if parts else "Unnamed Detail"

    def open_retirement_wizard(self):
        return {
            "name": _("Retire Item"),
            "type": "ir.actions.act_window",
            "res_model": "iscapop.retirement_wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_item_detail_id": self.id},
        }

    @api.constrains("stock")
    def _check_stock(self):
        for record in self:
            if record.stock < 0:
                raise ValidationError("Stock cannot be negative.")

    @api.model
    def create(self, vals):
        if "active" not in vals:
            vals["active"] = True
        """Merge stock when adding to class location"""
        location = self.env["iscapop.location_model"].browse(vals.get("location_id"))
        if location.loc_type == "class":
            existing = self.search(
                [
                    ("item_id", "=", vals.get("item_id")),
                    ("condition", "=", vals.get("condition")),
                    ("location_id", "=", vals.get("location_id")),
                ],
                limit=1,
            )

            if existing:
                existing.stock += vals.get("stock", 1)
                return existing

        return super().create(vals)

    @api.model
    def write(self, vals):
        """Merge stock when moving to class location"""
        if "location_id" in vals:
            new_location = self.env["iscapop.location_model"].browse(
                vals["location_id"]
            )
            if new_location.loc_type == "class":
                for record in self:
                    existing = self.search(
                        [
                            ("item_id", "=", record.item_id.id),
                            ("condition", "=", record.condition),
                            ("location_id", "=", vals["location_id"]),
                            ("id", "!=", record.id),
                        ],
                        limit=1,
                    )

                    if existing:
                        existing.stock += record.stock
                        record.unlink()
                    else:
                        super(itemDetailsModel, record).write(vals)
                return True

        return super().write(vals)
