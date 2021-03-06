##parameters=
# $Id$
"""Return custom document layout."""


cpslocalfs_layout = {
    'widgets': {
        'basepath': {
            'type': 'Path Widget',
            'data': {
    
                'fields': ['basepath'],
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'label_basepath',
                'label': 'label_basepath',
                'display_width': 72,
                'size_max': 100,
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
        'ncols': 1,
        'rows': [[{'widget_id': 'basepath'},],],
        },
    }








###########################################################
# END OF LAYOUTS DEFINITIONS
###########################################################

layouts = {}

#
# Building the dictionnary of layouts for the installer
#
layouts['CPSLocalFS'] = cpslocalfs_layout

return layouts
