from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "tag titles a property keywords"
    _order = "name"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE (name)',
        'tag name should be unique.')
    ]