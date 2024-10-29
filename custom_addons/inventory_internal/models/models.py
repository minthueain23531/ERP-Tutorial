from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.onchange('picking_type_id')
    def _onchange_picking_type_id(self):
        if self.picking_type_id.code == 'internal':
            self.location_id = False
            self.location_dest_id = False
            return {
                'domain': {
                    'location_id': [('usage', '=', 'internal')],
                    'location_dest_id': [('usage', '=', 'internal')]
                }
            }
        else:
            self.location_id = False
            self.location_dest_id = False
            return {
                'domain': {
                    'location_id': [],
                    'location_dest_id': []
                }
            }
