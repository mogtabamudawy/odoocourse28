{
    'name': 'Hospital Management System',
    'version': '1.0',
    'category': 'Healthcare',
    'summary': 'Manage Patients, Doctors, Appointments, and Billing',
    'description': """
Hospital Management System (HMS) module for Odoo 18.
Features:
- Patient management
- Doctor HR
- Appointment scheduling
- Billing
- Bilingual support (Arabic & English)
""",
    'author': 'Harmony Global Technology',
    'depends': ['base', 'mail','hr','account'],  # We will add dependencies as needed
    'data': [
        # XML files for views and security will go here later
        'security/ir.model.access.csv',
        'data/appointment_sequence.xml',
        
        'reports/report.xml',
        'reports/appointment_prescription.xml',
        
        'views/appointment_view.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        
        
        'views/medicine_views.xml',




        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
