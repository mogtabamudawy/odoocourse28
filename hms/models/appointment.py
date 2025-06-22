from odoo import models, fields,api

class HmsAppointment(models.Model):
    _name = 'hms.appointment'
    _description = 'Patient Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    patient_id = fields.Many2one('res.partner', string='Patient', required=True , domain="[('is_patient','=',True)]")
    doctor_id = fields.Many2one('hr.employee', string='Doctor', domain="[('is_doctor','=',True)]", required=True)
    appointment_date = fields.Datetime(string='Appointment Date', required=True)
    notes = fields.Text(string='Notes')
    consultation_fee = fields.Float(string='Consultation Fee', readonly=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_payment', 'Waiting for Payment'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')

    appointment_count = fields.Integer(string="Appointments", compute="_compute_appointment_count")
    invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True)
    medication_ids = fields.One2many('hms.appointment.medication', 'appointment_id', string='Medications')
    diagnosis = fields.Text(string="Diagnosis")
    attachment_ids = fields.Many2many('ir.attachment', string="Attachments", 
                                  domain="[('res_model','=','hms.appointment'), ('res_id','=',id)]")
    
    def _compute_appointment_count(self):
        for patient in self:
            patient.appointment_count = self.env['hms.appointment'].search_count([('patient_id', '=', patient.id)])


    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hms.appointment') or 'New'
        

        doctor_id = vals.get('doctor_id')
        if doctor_id and not vals.get('consultation_fee'):
            doctor = self.env['hr.employee'].browse(doctor_id)
            vals['consultation_fee'] = doctor.consultation_fee

        return super().create(vals)

        

    def action_confirm(self):
        for rec in self:
            if rec.invoice_id:
                raise UserError("Invoice already exists.")

            if not rec.patient_id:
                raise UserError("Patient must be linked to a customer (partner).")

            # Create invoice
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': rec.patient_id.id,
                'invoice_origin': rec.name,
                'invoice_line_ids': [(0, 0, {
                    'name': f"Appointment with {rec.doctor_id.name}",
                    'quantity': 1,
                    'price_unit': rec.consultation_fee,  # Optional: appointment fee
                })],
            })

            rec.invoice_id = invoice.id
            rec.state = 'waiting_payment'
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",rec.invoice_id)
            # Show the invoice directly (optional)
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoice.id,
                'target': 'current',
            }


    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    @api.depends('invoice_id.payment_state')
    def _compute_state_from_invoice(self):
        for rec in self:
            if rec.invoice_id and rec.invoice_id.payment_state == 'paid':
                if rec.state == 'waiting_payment':
                    rec.state = 'confirmed'


    def action_open_invoice(self):
        self.ensure_one()
        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.invoice_id.id,
            'target': 'current',
        }

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):
        if self.doctor_id:
            self.consultation_fee = self.doctor_id.consultation_fee

    def action_print_prescription(self):
        self.ensure_one()
        if not self.id:
            raise UserError("Please save the record before printing the prescription.")
        return {
            'type': 'ir.actions.report',
            'report_name': 'hms.report_prescription_template',
            'report_type': 'qweb-pdf',
            'res_id': self.id
        }

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_medicine = fields.Boolean(string='Is a Medicine')

