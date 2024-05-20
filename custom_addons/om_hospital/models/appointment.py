# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _description = "Hospital Appintment"
    _order = "doctor_id,name,age"

    # Use Two method for field tracking [tracking=True, track_visibility='onchange']

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    patient_name_id = fields.Many2one('hospital.patient', string="Patient Name", required=True)
    age = fields.Integer(string='Age', related='patient_id.age',tracking=True, store=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ], string="Gender")
    state = fields.Selection([('draft','Draft'), ('confirm','Confirmd'), ('done','Done'), ('cancel','Cancelled')], default='draft', string="Status", tracking=True)
    note = fields.Text(string='Description')
    date_appointment = fields.Date(string="Date")
    date_checkup = fields.Datetime(string="Check Up Time")
    image = fields.Binary(string="Patient Image")
    prescription = fields.Text(string="Prescription")
    prescription_line_ids = fields.One2many('appointment.prescription.lines', 'appointment_id', string="Prescription Lines")

    # Add Actions
    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        # print("Clicked on button")
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Patient'
        if vals.get('name', _('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        return res

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        # print("OnChange Triggered")
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            if self.patient_id.note:
                self.note = self.patient_id.note

        else:
            self.gender = ''
            self.note = ''

    def unlink(self):
        # print("Deleting the Record")
        if self.state == 'done':
            raise ValidationError(_("You Cannot Delete %s as it is in Done Stage" % self.name))
        return super(HospitalAppointment, self).unlink()

    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.odoo.com/',
        }

class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"


    name = fields.Char(string="Medicine")
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
