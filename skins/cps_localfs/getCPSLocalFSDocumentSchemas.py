##parameters=
# $Id$
"""Return custom document schemas."""
########################################################
# Image SCHEMA
########################################################
cpslocalfs_schema = {
       'Basepath': {
                  'type': 'CPS String Field',
                  'data': {'is_searchabletext': 0,}
                },
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
