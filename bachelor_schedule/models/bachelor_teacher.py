from odoo import fields, models

class BachelorTeacher(models.Model):
    _name = "bachelor.teacher"
    _description = "Subject teacher model"

    name = fields.Char(
        string = "Teacher's Name",
        required=True
    )

    contact_number = fields.Text(
        string="Contact Number",
    )

    email_address = fields.Text(
        string="Email Address"
    )

    subject_ids = fields.One2many(
        'bachelor.subject',
        'teacher_id',
        string="Subjects",
    )