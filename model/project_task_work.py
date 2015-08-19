from openerp import models, fields, api

class project_task_work_improvements(models.Model):
    _inherit = ['project.task.work']

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