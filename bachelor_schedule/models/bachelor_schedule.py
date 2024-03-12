from odoo import fields, models, api
from datetime import datetime, timedelta, date
import calendar


class BachelorSchedule(models.Model):
    _name = "bachelor.schedule"
    _description = "A schedule model"
    _rec_name = "subject_id"

    subject_id = fields.Many2one(
        "bachelor.subject",
        required=True,
        string="Subject Name"
    )

    color = fields.Integer("Color")

    period_start = fields.Datetime(required=True, string="Period Starts", default=fields.Datetime.now)

    period_duration = fields.Selection(
        selection=[
            ('forty_five_mins', '45 mins'),
            ('one_hour', '1 hr'),
            ('two_hours', '2 hrs'),
            ('three_hours', '3 hrs')
        ],
        string="Duration",
        default="one_hour"
    )

    period_stop = fields.Datetime(
        string="Period Stops",
        readonly=True,
        compute="_compute_period_stop_time"
    )

    period_end_time = fields.Datetime(
        string="Ends At",
        compute="_compute_period_end_time",
    )

    subject_schedule_ids = fields.One2many(
        'bachelor.subject.schedule',
        'schedule_id'
    )

    @api.depends('period_start', 'period_duration')
    def _compute_period_stop_time(self):
        for subject in self:
            period_duration_time = subject.period_duration
            period_start_time = subject.period_start
            if period_start_time:
                if period_duration_time == 'forty_five_mins':
                    duration = 45
                elif period_duration_time == 'one_hour':
                    duration = 60
                elif period_duration_time == 'two_hours':
                    duration = 120
                else:
                    duration = 180
                subject.period_stop = period_start_time + timedelta(minutes=duration)
            else:
                subject.period_stop = datetime.now() + timedelta(minutes=60)

    # @api.depends('period_start')
    # def _compute_period_end_time(self):
    #     for subject in self:
    #         start_date = subject.period_start
    #         day_of_week = start_date.weekday()
    #         days = (calendar.weekday(start_date.year, start_date.month, 1) - day_of_week) % 7 
    #         period_days = []
    #         current_date = start_date + timedelta(days=days)
    #         final_datetime = [datetime.strptime(date_str, '%Y-%m-%d-%h-%m-%s') for date_str in period_days]
    #         while current_date.month == start_date.month:
    #             period_days.append(current_date)
    #             current_date += timedelta(days=7)
    #         subject.period_end_time =  final_datetime