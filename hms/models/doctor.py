from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_doctor = fields.Boolean(string='Is a Doctor')
    specialty = fields.Char(string='Specialty')
    license_number = fields.Char(string='Medical License Number')
    biography = fields.Text(string='Biography')
    consultation_fee = fields.Float(string='Consultation Fee')