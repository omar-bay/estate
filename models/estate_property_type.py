from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "type of the property"
    _order = "sequence"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.Many2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute="_compute_offer_count")
    sequence = fields.Integer()

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('unique_name', 'UNIQUE (name)',
        'type name should be unique.')
    ]