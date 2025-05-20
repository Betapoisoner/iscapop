from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RetirementWizard(models.TransientModel):
    _name = "iscapop.retirement_wizard"
    _description = "Retire Item Wizard"

    item_detail_id = fields.Many2one("iscapop.item_details_model", required=True)
    option = fields.Selection(
        [
            ("existing", "Select Existing Retire Location"),
            ("new", "Create New Retire Location"),
        ],
        default="existing",
        required=True,
    )
    retire_location_id = fields.Many2one(
        "iscapop.location_model",
        string="Retire Location",
        domain="[('loc_type', '=', 'retire')]",
    )
    new_location_name = fields.Char(string="New Retire Location Name")

    def action_retire(self):
        self.ensure_one()
        if self.option == "new":
            if not self.new_location_name:
                raise ValidationError(
                    _("Please enter a name for the new retire location.")
                )
            location = self.env["iscapop.location_model"].create(
                {
                    "name": self.new_location_name,
                    "loc_type": "retire",
                }
            )
        else:
            if not self.retire_location_id:
                raise ValidationError(_("Please select a retire location."))
            location = self.retire_location_id

        # Update item detail's location
        self.item_detail_id.location_id = location

        # Return the report action
        return {
            "type": "ir.actions.report",
            "report_name": "iscapop.report_retirement_completion",
            "report_type": "qweb-pdf",
            "docs": self,
            "context": {"discard_logo_check": True},
        }
