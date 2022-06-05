from odoo import fields, models

class EstateProperyType(models.Model):
    _name = "estate.property.type"
    _description = "type of the property"

    name = fields.Char(required=True)