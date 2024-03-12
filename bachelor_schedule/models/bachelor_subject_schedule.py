from odoo import fields, models, api
from datetime import datetime, timedelta, date

 
class BachelorSubjectSchedule(models.Model):
    _name = "bachelor.subject.schedule"
    _description =  "Bachelor Subject Schedule model"
    # _rec_name = "display_name"

    name = fields.Char(
        string="Name"
    )

    display_name = fields.Char(
        string="Schedule Name",
        compute="_compute_display_name",
    )

    subject_id = fields.Many2one('bachelor.subject', string='Subjects', required=True, readonly=True)

    schedule_id = fields.Many2one('bachelor.schedule')

    from_date = fields.Datetime(required=True)
    
    to_date = fields.Datetime(required=True)

    @api.depends('subject_id', 'from_date')
    def _compute_display_name(self):
        for subject in self:
            available_subject = subject.subject_id.subject_name
            subject_from_date = subject.from_date
            if subject_from_date and available_subject:
                subject.display_name = f"{available_subject} | {subject_from_date}"
                # import pdb; pdb.set_trace()
            else:
                subject.display_name = None