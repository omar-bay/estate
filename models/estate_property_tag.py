from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "tag titles a property keywords"

    name = fields.Char(required=True)