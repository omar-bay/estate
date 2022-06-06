from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "type of the property"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE (name)',
        'type name should be unique.')
    ]