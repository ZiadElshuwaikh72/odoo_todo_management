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
    ref=fields.Char(default='New',readonly=True)

    @api.constrains('estimated_time','line_ids')
    def check_total_time(self):
        for rec in self:
            total=sum(rec.line_ids.mapped('hours'))
            if total>rec.estimated_time:
                raise ValidationError(f"total time in lines : {total}" f" cannot exceed Total Hours{rec.estimated_time}")



    def action_new(self):
        for rec in self:
            print("status in new")
            rec.status = 'new'


    def action_in_progress(self):
        for rec in self:
            print("status in in_progress")
            rec.status = 'in_progress'

    def action_completed(self):
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

        # Override method create with sequence
    def create(self,vals):
        res=super(TodoTask,self).create(vals)
        if res.ref =='New':
            res.ref=self.env['ir.sequence'].next_by_code('todo_seq')
            return res

    # method relation wizard assign
    def action_open_change_assign_wizard(self):
         # نجمع كل السجلات الغير مسموح بها
         invalid_tasks = self.filtered(lambda rec: rec.status not in ('new', 'in_progress'))
         if invalid_tasks:
             raise ValidationError(
                 "You can't do this action. Only tasks with status 'New' or 'In Progress' can be changed.")
         else:
             action=self.env['ir.actions.actions']._for_xml_id('todo_management.change_assign_wizard_action')
             action['context']={'default_task_ids':self.ids}
             return action



class TodoTaskLine(models.Model):
    _name='todo.task.line'

    description=fields.Text()
    date=fields.Date(tracking=True)
    hours=fields.Float(string='Hours')
    todo_id=fields.Many2one('todo.task')