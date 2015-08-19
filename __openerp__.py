{
    'name': "Worklog management improvements",
    'version': '1.0',
    'depends': ['hr_timesheet','project_timesheet','contract_timesheet_activities_on_site_management'],
    'author': "Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Humain Resources',
    'description': 
    """
    Worklog management improvements
        
        - It add a calendar view for the worklogs.
        - date_begin is a new datetime field used to order the worklogs in the calendar. This field is created because the date field from the worklog is a standard date type and we need hours and minutes.
        

    This module has been developed by Bernard DELHEZ @ AbAKUS it-solution.
    """,
    'data': ['view/hr_analytic_timesheet_view.xml',
             'view/project_issue_view.xml',
             'view/hr_timesheet_sheet_view.xml',
             'hr_analytic_timesheet_data.xml',
            ],
}
