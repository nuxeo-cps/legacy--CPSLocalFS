##parameters=
# $Id$
"""Return custom document schemas."""
########################################################
# Image SCHEMA
########################################################
cpslocalfs_schema = {
    'basepath': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        }
    }


###########################################################
# END OF SCHEMAS DEFINITIONS
###########################################################

schemas = {}

#
# Building the dictionnary of schemas for the installer
#
schemas['CPSLocalFS'] = cpslocalfs_schema


return schemas
