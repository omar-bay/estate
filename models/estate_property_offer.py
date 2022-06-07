from odoo.exceptions import ValidationError
import datetime
import odoo.exceptions
from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "selling offers given to a property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    partner_name = fields.Char(related="partner_id.name")
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one('estate.property.type', related="property_id.property_type_id", store=True, string="Property Type")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _sql_constraints = [
        ('positive_price', 'CHECK (price > 0)',
        'price should be positive.')
    ]

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < record.property_id.expected_price:
                raise ValidationError("Bidding price cannot be less than Expected price!")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date != False:
                interval = datetime.timedelta(seconds=(record.validity * 3600))
                record.date_deadline = fields.Datetime.to_string(record.create_date + interval)
            # d = datetime.datetime.strptime(str(record.create_date)[:10], '%Y-%m-%d')
            # delta = datetime.timedelta(days=record.validity)
            # record.date_deadline = d+delta

    def _inverse_date_deadline(self):
        for record in self:
            fmt = '%Y-%m-%d'
            start_date = record.create_date
            end_date = record.date_deadline
            d1 = datetime.datetime.strptime(str(start_date)[:10], fmt)
            d2 = datetime.datetime.strptime(str(end_date)[:10], fmt)
            date_difference = d2 - d1
            record.validity = float(str(date_difference.days))

    def action_accept(self):
        if self.property_id.state != 'sold':
            self.status = 'accepted'
            self.property_id.buyer = self.partner_id
            self.property_id.selling_price = self.price
            self.property_id.state = 'sold'
        else:
            raise odoo.exceptions.UserError('Property already sold!')
        return True

    def action_refuse(self):
        if self.status != 'accepted':
            self.status = 'refused'
        else:
            raise odoo.exceptions.UserError('Cannot refuse an accepted deal!')
        return True