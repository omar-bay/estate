import datetime
from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "selling offers given to a property"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            interval = datetime.timedelta(seconds=(self.validity * 3600))
            record.date_deadline = fields.Datetime.to_string(record.create_date + interval)

    def _inverse_date_deadline(self):
        for record in self:
            fmt = '%Y-%m-%d'
            start_date = record.create_date
            end_date = record.date_deadline
            d1 = datetime.datetime.strptime(str(start_date)[:10], fmt)
            d2 = datetime.datetime.strptime(str(end_date)[:10], fmt)
            date_difference = d2 - d1
            record.validity = float(str(date_difference.days))

