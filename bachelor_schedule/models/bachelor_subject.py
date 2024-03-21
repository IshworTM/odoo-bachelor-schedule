from odoo import fields, models, api


class BachelorSubject(models.Model):
    _name = "bachelor.subject"
    _description = "A model for all subjects."
    _rec_name = "display_name"

    display_name = fields.Char(compute="_compute_subject_name", string="Display Name")

    subject_name = fields.Char(string="Subject*", required=True)

    credit_hours = fields.Integer(string="Credit Hours*", required=True)

    color = fields.Integer("Color")

    subject_code = fields.Char(string="Subject Code")

    course_id = fields.Many2one("bachelor.course", required=True, string="Course Name*")

    teacher_id = fields.Many2one("bachelor.teacher", required=True, string="Teacher*")

    subject_schedule_ids = fields.One2many("bachelor.subject.schedule", "subject_id")

    @api.depends("course_id", "subject_name")
    def _compute_subject_name(self):
        for subject in self:
            subject_name = subject.subject_name
            c_alias = subject.course_id.alias
            if subject_name and c_alias:
                subject.display_name = f"[{c_alias}] {subject_name}"
            else:
                subject.display_name = subject_name
