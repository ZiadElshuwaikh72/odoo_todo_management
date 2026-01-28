from odoo import api, fields, models

class ChangeAssignTo(models.TransientModel):
    _name = 'change.assign'

    task_ids = fields.Many2many('todo.task')
    assign_id=fields.Many2one('res.partner')

    def action_confirm(self):
        if not self.task_ids:
            return

        self.task_ids.write({
            'assign_to':self.assign_id.id
        })