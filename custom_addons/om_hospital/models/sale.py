# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.addons.sale.models.sale import SaleOrder as OdooSaleOrder

class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_description = fields.Char(string='Sale Description')
    
# ----- FIRST METHOD ---------
    # def unlink(self):
    #     print("@@@@@@@@@@")
    #     return super(OdooSaleOrder, self).unlink()


# ----- SECOND METHOD ---------
def unlink(self):
    return super(OdooSaleOrder, self).unlink()

OdooSaleOrder.unlink = unlink