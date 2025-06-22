from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean(string="Is a Patient", default=False)
    dob = fields.Date(string="Date of Birth")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")
    blood_type = fields.Selection([
        ('a+', 'A+'), ('a-', 'A-'),
        ('b+', 'B+'), ('b-', 'B-'),
        ('ab+', 'AB+'), ('ab-', 'AB-'),
        ('o+', 'O+'), ('o-', 'O-')
    ], string="Blood Type")
    medical_history = fields.Text(string="Medical History")

    
    appointment_count = fields.Integer(string="Appointments", compute="_compute_appointment_count")
    appointment_history_ids = fields.One2many(
    'hms.appointment',
    'patient_id',
    string='Appointment History'
)

    def _compute_appointment_count(self):
        for patient in self:
            patient.appointment_count = self.env['hms.appointment'].search_count([('patient_id', '=', patient.id)])

   
