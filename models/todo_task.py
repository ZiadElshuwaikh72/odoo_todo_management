from odoo import models, fields,api
from odoo.exceptions import ValidationError

class TodoTask(models.Model):
    _name='todo.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'task_name'

    task_name = fields.Char(required=True, tracking=True)
    description=fields.Text(tracking=True)
    due_date=fields.Date(tracking=1)
    status=fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
        ('closed','Closed'),
    ],tracking=True)
    assign_to = fields.Many2one('res.partner',required="1",tracking=True)

    _sql_constraints = [
        ('task_name_uniq', 'UNIQUE(task_name)','The task name is exists.'),
    ]

    line_ids=fields.One2many('todo.task.line','todo_id')
    estimated_time=fields.Float(string='Estimated Time',required=True)

    active=fields.Boolean(default=True)
    is_late=fields.Boolean()


    @api.constrains('estimated_time','line_ids')
    def check_total_time(self):
        for rec in self:
            total=sum(rec.line_ids.mapped('hours'))
            if total>rec.estimated_time:
                raise ValidationError(f"total time in lines : {total}" f" cannot exceed Total Hours{rec.estimated_time}")



    def actoin_new(self):
        for rec in self:
            print("status in new")
            rec.status = 'new'


    def action_in_progress(self):
        for rec in self:
            print("status in in_progress")
            rec.status = 'in_progress'

    def actoin_completed(self):
        for rec in self:
            print("status in completed")
            rec.status = 'completed'

    def action_closed(self):
        for rec in self:
            print("status in closed")
            rec.status = 'closed'

    def check_due_date(self):
        tasks_ids=self.search([])
        for rec in tasks_ids:
            if rec.due_date and rec.due_date<fields.date.today() and rec.status in ('new','in_progress'):
                rec.is_late=True


class TodoTaskLine(models.Model):
    _name='todo.task.line'

    description=fields.Text()
    date=fields.Date(tracking=True)
    hours=fields.Float(string='Hours')
    todo_id=fields.Many2one('todo.task')