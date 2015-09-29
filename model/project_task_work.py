from openerp import models, fields, api
from datetime import datetime, date, timedelta
import logging
import math
_logger = logging.getLogger(__name__)

class project_task_work_improvements(models.Model):
    _inherit = ['project.task.work']

    @api.onchange('hours')
    def set_date_as_end(self):
        if (not self.id):
            date_to_change = datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S')
            minutes = math.ceil(self.hours * 60)

            nb_hours = math.trunc(minutes / 60)
            nb_minutes = math.ceil(minutes % 60)
            delta = timedelta(hours = nb_hours, minutes = nb_minutes)

            date_to_change = date_to_change - delta
            self.write({'date' : date_to_change})
            self.date = date_to_change.strftime('%Y-%m-%d %H:%M:%S')

    def create(self, cr, uid, vals, *args, **kwargs):
        project_task_work_id = super(project_task_work_improvements,self).create(cr, uid, vals, *args, **kwargs)
        project_task_work = self.browse(cr, uid, project_task_work_id)
        if project_task_work.date and project_task_work.hr_analytic_timesheet_id:
            project_task_work.hr_analytic_timesheet_id.date_begin = project_task_work.date
        return project_task_work_id

    def write(self, cr, uid, ids, vals, context=None):
        result = super(project_task_work_improvements,self).write(cr, uid, ids, vals, context)
        for task in self.browse(cr, uid, ids, context=context):
            if task.date and task.hr_analytic_timesheet_id:
                task.hr_analytic_timesheet_id.date_begin = task.date
        return result
