from email.policy import default
import odoo.exceptions
from odoo import fields, models, api

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Descriptions"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Datetime.today())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()  
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="orientation",
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=False)
    state = fields.Selection(
        string="state",
        selection=[('new', 'New'), ('offer recieved', 'Offer Recieved'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    salesperson = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area", inverse="_inverse_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _sql_constraints = [
        ('positive_price', 'CHECK (price > 0)',
        'price should be positive.')
    ]
    _sql_constraints = [
        ('positive_price', 'CHECK (selling_price > 0)',
        'selling price should be positive.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def _inverse_total_area(self):
        for record in self:
            record.garden_area = record.total_area - record.living_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            max = 0
            for offer in record.offer_ids:
                if offer.price > max:
                    max = offer.price
            record.best_price = max

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_do_cancel(self):
        if self.state != "sold":
            self.state = 'canceled'
        else:
            raise odoo.exceptions.UserError('Sold Properties cannot be Canceled!')
        return True

    def action_do_sold(self):
        if self.state != "canceled":
            self.state = 'sold'
        else:
            raise odoo.exceptions.UserError('Canceled Properties cannot be Sold!')
        return True