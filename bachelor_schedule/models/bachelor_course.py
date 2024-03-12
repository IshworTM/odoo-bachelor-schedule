from odoo import fields, models, api


class BachelorsCourse(models.Model):
    _name = "bachelor.course"
    _description = "A model for all bachelor courses."

    name = fields.Char(
        required=True,
        string="Course Name*"
    )

    alias = fields.Char(
        required=True,
        string="Course Alias*",
    )

    course_duration = fields.Selection(
        required=True,
        string="Duration*",
        selection=[
            ("sem", "Semester Wise"),
            ("year", "Yearly")
        ],
    )

    subject_ids = fields.One2many(
        "bachelor.subject",
        "course_id",
        string="Subjects",
    )
