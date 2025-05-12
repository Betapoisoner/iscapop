from odoo import models, fields, api


class itemModel(models.Model):
    _name = "iscapop.item_model"
    _description = "iscapop.item_model"
    _rec_name = "name"

    photo = fields.Binary(string="Photo", help="Here you put a photo of the item")
    name = fields.Char(
        string="Name",
        default="Item",
        help="This is where you put the name of the item.",
        required=True,
    )

    description = fields.Html(
        string="Description", help="This is where you put the description of the item."
    )
    stock_full = fields.Integer(
        string="Full Stock",
        help="Here you put see many items of this kind you have in total ",
        compute="_compute_stock_total",
        store=True,
    )

    details_ids = fields.One2many(
        string="Details",
        comodel_name="iscapop.item_details_model",
        inverse_name="item_id",
    )

    category_id = fields.Many2one(
        string="Category",
        comodel_name="iscapop.category_model",
        ondelete="restrict",
    )

    def open_transfer_wizard(self):
        return {
            "name": "Transfer Items",
            "type": "ir.actions.act_window",
            "res_model": "iscapop.transfer_wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_item_id": self.id},
        }

    def open_donation_wizard(self):
        return {
        "name": "Donate Items",
        "type": "ir.actions.act_window",
        "res_model": "iscapop.donation_wizard",
        "view_mode": "form",
        "target": "new",
        "context": {"default_item_id": self.id},
    }

    @api.depends("details_ids")
    def _compute_stock_total(self):
        for record in self:
            total = 0
            for detail in record.details_ids:
                # Exclude donating items from stock count
                if detail.state != "donating" and detail.condition != "bad":
                    total += detail.stock
            record.stock_full = total
