from odoo import models, fields, api


class MaterialRequisition(models.Model):
    _name = 'material.requisition'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', 'Employee')
    branch_id = fields.Many2one('branch', 'Branch')
    department_id = fields.Many2one('hr.department', 'Department')
    company_id = fields.Many2one('res.company', 'Company')
    request_warehouse_id = fields.Many2one('stock.warehouse', 'Request Warehouse')
    destination_warehouse_id = fields.Many2one('stock.warehouse', 'Destination Warehouse')
    date = fields.Date('Scheduled Date')
    remark = fields.Text('Remark')
    material_requisition_line = fields.One2many('material.requisition.line', 'material_requisition_ids', 'Requisition Line')
    state = fields.Selection(
        selection=[
            ('draft', "draft"),
            ('submit', "Waiting Approval"),
            ('approve', "Approved"),
            ('reject', "Rejected"),
            ('cancel', "Canceled"),
        ],
        string="Status",
        readonly=True, copy=False, index=True,
        default='draft', tracking=True
    )
    issued_status = fields.Selection([('waiting', 'Waiting'),
                                     ('partial_issued', 'Partial Issued'),
                                     ('issued', 'Issued')])
    is_dept_manager = fields.Boolean('Is Department Manager', compute='_compute_is_dept_manager')

    @api.depends('employee_id', 'department_id')
    def _compute_is_dept_manager(self):
        for record in self:
            record.is_dept_manager = False
            if self.env.user.employee_id == self.employee_id.department_id.manager_id:
                record.is_dept_manager = True

    def action_submit(self):
        self.write({'state': 'submit'})

    def action_approve(self):
        self.write({'state': 'approve'})

    def action_reject(self):
        self.write({'state': 'reject'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})


class MaterialRequisitionLine(models.Model):
    _name = 'material.requisition.line'
    _description = 'Material Requisition Line'

    product_id = fields.Many2one(comodel_name='product.product', string="Product",)
    code = fields.Char('Item Code')
    quantity = fields.Float('Quantity')
    uom_id = fields.Many2one('uom.uom', 'UOM')
    material_requisition_ids = fields.Many2one('material.requisition','Material Requisition')

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id
        else:
            self.uom_id = False