from odoo import _, fields, models, api
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError, ValidationError
import calendar


class BachelorSubjectSchedule(models.Model):
    _name = "bachelor.subject.schedule"
    _description = "Bachelor Subject Schedule model"

    name = fields.Char(string="Name")

    display_name = fields.Char(
        string="Schedule Name",
        compute="_compute_display_name",
    )

    subject_id = fields.Many2one(
        "bachelor.subject", string="Subject Name", readonly=True
    )

    schedule_id = fields.Many2one("bachelor.schedule")

    schedule_from_date = fields.Datetime(
        string="Starts At", required=True, default=fields.Datetime.now
    )

    schedule_to_date = fields.Datetime(
        string="Ends At", readonly=True, compute="_compute_schedule_to_date"
    )

    period_duration = fields.Selection(
        selection=[
            ("forty_five_mins", "45 mins"),
            ("one_hour", "1 hr"),
            ("two_hours", "2 hrs"),
            ("three_hours", "3 hrs"),
        ],
        string="Duration",
        default="one_hour",
    )

    @api.depends("subject_id", "schedule_from_date")
    def _compute_display_name(self):
        for schedule in self:
            available_subject = schedule.subject_id.subject_name
            schedule_start_date = schedule.schedule_from_date
            if schedule_start_date and available_subject:
                schedule.display_name = f"{available_subject} || {schedule_start_date}"
            else:
                schedule.display_name = None

    @api.depends("schedule_from_date", "period_duration")
    def _compute_schedule_to_date(self):
        for period in self:
            period_duration_time = period.period_duration
            period_start_time = period.schedule_from_date
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
                    period.schedule_to_date = period_start_time + timedelta(
                        minutes=duration
                    )
                else:
                    period.schedule_to_date = period_start_time + timedelta(minutes=60)
            else:
                period.schedule_to_date = datetime.now() + timedelta(minutes=60)

    def _create_schedules_in_calendar(self, schedule):
        list_of_days = self._get_all_possible_dates_between_range(schedule)

        for days in list_of_days:
            for key, value in days.items():
                time_map = {
                    0 : 'forty_five_mins',
                    1 : 'one_hour',
                    2 : 'two_hours',
                    3 : 'three_hours'
                }
                calculate_duration = (value - key).seconds // 3600
                self.env["bachelor.schedule"].create({
                    'subject_id' : schedule.subject_id.id,
                    'period_start': key,
                    'period_stop': value,
                    'period_duration' : time_map.get(calculate_duration, False)
                })
            

    def _get_all_possible_dates_between_range(self, schedules):
        for schedule in schedules:
            if schedule.schedule_from_date:
                period_start = schedule.schedule_from_date
                period_stop = schedule.schedule_to_date
                year = period_start.year
                start_hour = period_start.hour
                start_minute = period_start.minute
                start_second = period_start.second

                stop_hour = period_stop.hour
                stop_minute = period_stop.minute
                stop_second = period_stop.second
                week_day = period_start.strftime("%A").upper()
                start_date = datetime(year, 1, 1, 00, 00, 00)
                days = []
                while start_date.year == year:
                    if start_date.weekday() == calendar.weekday(year, 1, 1) + (getattr(calendar, week_day)):
                        days.append(
                            {
                                start_date + timedelta(hours=start_hour, minutes=start_minute, seconds=start_second) : start_date + timedelta(hours=stop_hour, minutes=stop_minute, seconds=stop_second) 
                            }
                        )
                        start_date += timedelta(days=7)
                    else:
                        start_date += timedelta(days=1)
                return days
            return False

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        self._create_schedules_in_calendar(res)
        return res

    @api.constrains("schedule_from_date", "schedule_to_date")
    def _check_dates(self):
        for schedule in self:
            if schedule.schedule_from_date > schedule.schedule_to_date:
                raise ValidationError(_("The offer value must be greater than 90% of Expected Price!!"))
