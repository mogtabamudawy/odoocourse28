# models/product_template.py

from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_medicine = fields.Boolean(string='Is a Medicine')
