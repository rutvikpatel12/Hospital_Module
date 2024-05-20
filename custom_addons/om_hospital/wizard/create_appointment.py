# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CreateAppointmentWizard, self).default_get(fields)
        # print(".....................",self._context)
        if self._context.get('active_id'):
            res['patient_id'] = self._context.get('active_id')
        return res

    date_appointment = fields.Date(string='Date', required=False)
    patient_id = fields.Many2one('hospital.patient', string="patient", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)

    def action_create_appointment(self):
        # print('Button is clicked!!')
        vals = {
            'patient_id': self.patient_id.id,
            'date_appointment': self.date_appointment,
            'doctor_id': self.doctor_id.id,
        }
        # print('Vals.......',vals)
        appointment_rec = self.env['hospital.appointment'].create(vals)
        # print("Appointment",appointment_rec.id)
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
        }

    def action_view_appointment(self):
        # Method -- 1
        action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action


        # Method -- 2
        # action = self.env['ir.actions.actions']._for_xml_id("om_hospital.action_hospital_appointment")
        # action['domain'] = [('patient_id', '=', self.patient_id.id)]
        # return action


        # Method -- 3
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Appointment',
        #     'res_model': 'hospital.appointment',
        #     'view_type': 'form',
        #     'domain': [('patient_id', '=', self.patient_id.id)],
        #     'view_mode': 'tree,form',
        #     'target': 'current',
        # }
        # return action