from odoo import models, fields

class TodoTask(models.Model):
    _name='todo.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    task_name = fields.Char(required=True, tracking=True)
    description=fields.Text(tracking=True)
    due_date=fields.Date(tracking=1)
    status=fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
    ],tracking=True)
    assign_to = fields.Many2one('res.partner',required="1",tracking=True)

    _sql_constraints = [
        ('task_name_uniq', 'UNIQUE(task_name)','The task name is exists.'),
    ]