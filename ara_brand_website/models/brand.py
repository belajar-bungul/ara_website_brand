from odoo import fields, models


class ProductBrand(models.Model):
    _inherit = "product.brand"
    
    highlight  = fields.Boolean()