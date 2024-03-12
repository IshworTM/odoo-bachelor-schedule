{
    'name': 'Schedule',
    'version': '1.20.5',
    'description': 'A bachelor schedule management module.',
    'summary': 'Bachelor Schedule manager',
    'author': 'Siwhro',
    'website': 'https://www.facebook.com',
    'license': 'LGPL-3',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/bachelor_subject_views.xml',
        'views/bachelor_teacher_views.xml',
        'views/bachelor_course_views.xml',
        'views/bachelor_schedule_views.xml',
    ],
    'auto_install': False,
    'installable':True,
    'application': True,
}