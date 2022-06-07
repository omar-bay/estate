from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "type of the property"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')

    _sql_constraints = [
        ('unique_name', 'UNIQUE (name)',
        'type name should be unique.')
    ]