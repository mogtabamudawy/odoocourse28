from odoo import models, fields

class HmsAppointmentMedication(models.Model):
    _name = 'hms.appointment.medication'
    _description = 'Appointment Medication'

    appointment_id = fields.Many2one('hms.appointment', string='Appointment',)
    product_id = fields.Many2one('product.product', string='Medicine', domain="[('is_medicine', '=', True)]")
    dosage = fields.Text(string='Dosage')
    duration = fields.Char(string='Duration')
    instructions = fields.Text(string='Instructions')
