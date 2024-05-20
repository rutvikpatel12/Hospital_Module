from odoo import api, fields, models

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	type = fields.Selection(selection_add=[
		('test', 'Test'), ('consu',)
		], tracking=True, ondelete={'test': 'cascade'})