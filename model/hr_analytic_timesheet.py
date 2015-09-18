from openerp import models, fields, api
from datetime import datetime, timedelta
from openerp.osv import osv
from openerp.tools.translate import _

class hr_analytic_timesheet_improvements(models.Model):
    _inherit = ['hr.analytic.timesheet']
    
    def check_and_correct_date_in_fifteen_step(self, date):
        newdate = date
        newhour = newdate.hour
        step = 0
        round = False
        minute_under_fifteen = newdate.minute
        while (minute_under_fifteen > 15):
           minute_under_fifteen = minute_under_fifteen - 15
           step+=1
        if(minute_under_fifteen>=(15/2)):
            round = True
        if round:
            newminute = (step*15)+15
            if newminute==60:
                newdate = newdate + timedelta(hours=1)
                newminute = 0
        else:
            newminute = step*15
        
        newdate = newdate.replace(minute=newminute, second=0)
        return newdate
    
    def _get_default_date(self):
        return datetime.strftime(self.check_and_correct_date_in_fifteen_step(datetime.now()), '%Y-%m-%d %H:%M:%S')
    
    date_begin = fields.Datetime(string='Start Date', default=_get_default_date)

    # set the date of date_begin to "date" to avoid consistency problems
    @api.onchange('date_begin')
    def copy_dates(self):
        self.write({'date' : self.date_begin})
        self.date = self.date_begin
    
    def create(self, cr, uid, vals, *args, **kwargs):
        hr_analytic_timesheet_id = super(hr_analytic_timesheet_improvements,self).create(cr, uid, vals, *args, **kwargs)
        hr_analytic_timesheet = self.browse(cr, uid, hr_analytic_timesheet_id)
        if hr_analytic_timesheet.date_begin:
            start_date = datetime.strptime(hr_analytic_timesheet.date_begin, '%Y-%m-%d %H:%M:%S')
            newdate = self.check_and_correct_date_in_fifteen_step(start_date)
            if start_date.minute != newdate.minute or start_date.second != newdate.second:
                hr_analytic_timesheet.date_begin = datetime.strftime(self.check_and_correct_date_in_fifteen_step(start_date), '%Y-%m-%d %H:%M:%S')
        else:
            hr_analytic_timesheet.date_begin = datetime.strftime(self.check_and_correct_date_in_fifteen_step(datetime.now()), '%Y-%m-%d %H:%M:%S')
        return hr_analytic_timesheet_id

    def write(self, cr, uid, ids, vals, context=None):
        result = super(hr_analytic_timesheet_improvements,self).write(cr, uid, ids, vals, context)
        for timesheet in self.browse(cr, uid, ids, context=context):
            if timesheet.date_begin:
                start_date = datetime.strptime(timesheet.date_begin, '%Y-%m-%d %H:%M:%S')
                newdate = self.check_and_correct_date_in_fifteen_step(start_date)
                if start_date.minute != newdate.minute or start_date.second != newdate.second:
                    timesheet.date_begin = datetime.strftime(newdate, '%Y-%m-%d %H:%M:%S')
            else:
                timesheet.date_begin = datetime.strftime(self.check_and_correct_date_in_fifteen_step(datetime.now()), '%Y-%m-%d %H:%M:%S')
        return result
    
    def _set_date_begin_if_date_exits(self, cr, uid, ids=None, context=None):
        hr_analytic_timesheet_obj = self.pool.get('hr.analytic.timesheet')
        hr_analytic_timesheets = hr_analytic_timesheet_obj.search(cr, uid, [('date', 'like', '-')])
        if hr_analytic_timesheets:
            for hr_analytic_timesheet in hr_analytic_timesheet_obj.browse(cr, uid, hr_analytic_timesheets):
                if hr_analytic_timesheet.date:
                    begin_date = datetime.strftime(datetime.strptime(hr_analytic_timesheet.date, '%Y-%m-%d').replace(hour=0,minute=0, second=0), '%Y-%m-%d %H:%M:%S')
                    query = """
                            UPDATE hr_analytic_timesheet
                            SET date_begin=%s
                            WHERE id=%s
                            """
                    cr.execute(query, (begin_date,hr_analytic_timesheet.id))
