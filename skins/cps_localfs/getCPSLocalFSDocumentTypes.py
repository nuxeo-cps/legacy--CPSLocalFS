##parameters=
# $Id$
"""Return custom document types."""


cpslocalfs_type = {
    'title': 'portal_type_CPSLocalFS_title',
    'description': '',
    'content_icon': 'localfs_icon.gif',
    'content_meta_type': 'CPS Document',
    'product': 'CPSLocalFS',
    'factory': 'addCPSLocalFS',
    'immediate_view': 'cpslocalfs_edit_form',
    'global_allow': 1,
    'filter_content_types': 0,
    'allowed_content_types': [],
    'allow_discussion': 0,
    'cps_is_searchable': 0,
    'cps_proxy_type': '',
    'cps_display_as_document_in_listing': 1,
    'schemas': ['common', 'metadata', 'CPSLocalFS'],
    'layouts': ['common', 'CPSLocalFS'],
    'flexible_layouts': [],
    'storage_methods': [],
    'actions': (
                {'id': 'view',
                  'name': 'action_view',
                  'action': 'cpslocalfs_folder_contents',
                  'permissions': ('View',)},
                  {'id': 'modify',
                   'name': 'action_modify',
                   'action': 'cpslocalfs_edit_form',
                   'permissions': ('ModifyPortalContent',),}, 
            ),
}


types = {}


types['CPSLocalFS'] = cpslocalfs_type


return types
