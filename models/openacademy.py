from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Course(models.Model):
    _name = "openacademy.course"
    _description = "Open Academy Course"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'course_name'

    course_name = fields.Char(
        string='Course Name',
        required=True,
        translate=True,
        tracking=True
    )

    description = fields.Text(
        string="Description",
        tracking=True
    )

    responsible_id = fields.Many2one(
        'res.users',
        string="Responsible",
        ondelete='set null',
        index=True,
        default=lambda self: self.env.user,
        tracking=True
    )

    session_ids = fields.One2many(
        'openacademy.session',
        'course_id',
        string="Session",
        tracking=True
    )

    _sql_constraints = [
        ('unique_course_name', 'UNIQUE(course_name)', 'Only one service can exist with a specific course_name'),
    ]

    def action_test(self):
        for rec in self:
            create_by_orm = rec.env["openacademy.session"].create({
                "session_name": 'Test1',
                'course_id': rec.id
            })
            print(create_by_orm)

    @api.constrains("description")
    def name_description_check(self):
        for rec in self:
            if rec.description == rec.course_name:
                raise ValidationError(_("The course name and description cannot be the same."))

    def copy_data(self, default=None):
        default = dict(default or {})
        vals_list = super().copy_data(default=default)
        if 'course_name' not in default:
            for template, vals in zip(self, vals_list):
                vals['course_name'] = _("%s (copy)", template.course_name)
        return vals_list


class Session(models.Model):
    _name = "openacademy.session"
    _description = "Course Session"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "session_name"

    session_name = fields.Char(
        string="Session Title",
        required=True,
        tracking=True
    )

    start_date = fields.Date(
        string="Start Date",
        default=fields.Date.context_today,
        tracking=True
    )

    end_date = fields.Date(
        string="End Date",
        store=True,
        compute='_get_end_date',
        tracking=True
    )

    session_duration = fields.Float(
        string="Duration (Days)",
        digits=(6, 2),
        tracking=True
    )

    course_id = fields.Many2one(
        'openacademy.course',
        string='Course',
        ondelete='restrict',
        tracking=True
    )

    instructor_id = fields.Many2one(
        "res.partner",
        string="Instructor",
        domain=[('phone', '!=', False)],
        tracking=True
    )

    country_id = fields.Many2one(
        'res.country',
        related="instructor_id.country_id",
        tracking=True
    )

    attendees_ids = fields.Many2many(
        'res.partner',
        string='Attendees',
        tracking=True
    )

    attendees_count = fields.Integer(
        string="Attendees count",
        compute='_get_attendees_count',
        store=True,
        tracking=True
    )

    seats = fields.Integer(
        string="Seats",
        required=True,
        tracking=True
    )

    taken_seats = fields.Float(
        string="Taken Seats",
        compute="_compute_seats",
        default=0,
        tracking=True
    )

    active = fields.Boolean(
        'Active',
        default=True,
        tracking=True
    )

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        tracking=True
    )

    color = fields.Integer(
        'Color',
        tracking=True
    )

    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env.company.id
    )

    @api.depends('attendees_ids')
    def _get_attendees_count(self):
        for rec in self:
            rec.attendees_count = len(rec.attendees_ids)

    @api.depends('start_date', 'session_duration')
    def _get_end_date(self):
        for rec in self:
            if not (rec.start_date and rec.session_duration):
                rec.end_date = rec.start_date
                continue
            duration = timedelta(days=rec.session_duration, seconds=-1)
            rec.end_date = rec.start_date + duration

    @api.constrains('instructor_id', 'attendees_ids')
    def _check_instructor_not_in_attendees(self):
        for record in self:
            if record.instructor_id and record.instructor_id in record.attendees_ids:
                raise ValidationError(_("The lecturer cannot be one of the attendees."))

    @api.depends('seats', 'attendees_ids')
    def _compute_seats(self):
        for rec in self:
            if rec.seats:
                rec.taken_seats = len(rec.attendees_ids) / rec.seats * 100
            else:
                rec.taken_seats = 0.0

    @api.onchange('seats', 'attendees_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Seat value is incorrect",
                    'message': "The number of available seats may not be negative."
                },
            }
        if self.seats < len(self.attendees_ids):
            return {
                'warning': {
                    'title': "very large number of attendees",
                    'message': "Increase the number of seats or remove excess attendees",
                },
            }

    def action_open_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Openacademy Wizard'),
            'res_model': 'openacademy.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
