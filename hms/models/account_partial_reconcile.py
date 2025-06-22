from odoo import models

class AccountPartialReconcile(models.Model):
    _inherit = 'account.partial.reconcile'

    def create(self, vals_list):
        records = super().create(vals_list)

        for rec in records:
            # Find the move lines that are being reconciled
            debit_move = rec.debit_move_id.move_id
            credit_move = rec.credit_move_id.move_id

            # Check both sides in case payment is on either
            for move in [debit_move, credit_move]:
                if move.move_type == 'out_invoice' and move.payment_state == 'paid':
                    appointment = self.env['hms.appointment'].search([
                        ('invoice_id', '=', move.id),
                        ('state', '=', 'waiting_payment')
                    ])
                    if appointment:
                        appointment.write({'state': 'confirmed'})
        return records
