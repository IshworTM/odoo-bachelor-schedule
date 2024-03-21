from odoo import fields, models, api
from datetime import datetime, timedelta, date
import calendar


class BachelorSchedule(models.Model):
    _name = "bachelor.schedule"
    _description = "A schedule model"
    _rec_name = "subject_id"

    subject_id = fields.Many2one("bachelor.subject", string="Subject Name")

    color = fields.Integer("Color", default=0)

    period_start = fields.Datetime(required=True, string="Period Starts")

    period_stop = fields.Datetime(
        string="Period Stops",
        readonly=True,
    )

    period_duration = fields.Selection(
        selection=[
            ("forty_five_mins", "45 mins"),
            ("one_hour", "1 hr"),
            ("two_hours", "2 hrs"),
            ("three_hours", "3 hrs"),
        ],
        string="Duration",
    )

    subject_schedule_ids = fields.One2many(
        "bachelor.subject.schedule", "schedule_id", string="Schedules"
    )

    @api.depends("period_start", "period_duration")
    def _compute_period_stop(self):
        for period in self:
            period_duration_time = period.period_duration
            period_start_time = period.period_start
            if period_start_time:
                if period_duration_time:
                    if period_duration_time == "forty_five_mins":
                        duration = 45
                    elif period_duration_time == "one_hour":
                        duration = 60
                    elif period_duration_time == "two_hours":
                        duration = 120
                    else:
                        duration = 180
                    period.period_stop = period_start_time + timedelta(minutes=duration)
                else:
                    period.period_stop = period_start_time + timedelta(minutes=60)
            else:
                period.period_stop = datetime.now() + timedelta(minutes=60)
