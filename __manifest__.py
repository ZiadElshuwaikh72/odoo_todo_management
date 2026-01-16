{
    'name': "To-Do APP",
    'version': '17.0.0.1.0',
    'summary': 'ToDo  List Module Management',
    'author': "Ziad Ahmed",
    'category': 'Custom',
    'license': 'LGPL-3',
    'depends': ['base','contacts','mail'

                ],
    'data':
        [
        'security/ir.model.access.csv',
         'views/base_menu.xml',
         'views/todo_view.xml',
        'reports/todo_task_report.xml'

    ],
    'assets':{
        'web.assets_backend':[

        ]
    },
    'application': True,
    'installable': True,
}
