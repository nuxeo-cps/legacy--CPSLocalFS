"""Local File System product

$Id$"""
__version__='$Revision$'[11:-2]

from zLOG import LOG, INFO, DEBUG
from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.CPSCore.CPSBase import CPSBaseDocument, CPSBase_adder
from Products.CMFCore import CMFCorePermissions
from Products.LocalFS.LocalFS import LocalFS
from Products.CPSDefault.Folder import Folder


LOG("*sas* ===> ",INFO,"CPSLocalFS: Definition de la factory_type_information")

factory_type_information = ({
      'id': 'CPSLocalFS',
      'title': 'portal_type_CPSLocalFS',
      'icon': 'localfs_icon.gif',
      'product': 'CPSLocalFS',
      'meta_type': 'CPSLocalFS',
      'factory': 'addCPSLocalFS',
      'filter_content_types': 0,
      'allowed_content_types': (),
      'immediate_view':'localfs_edit_form',
      'actions': ({'id': 'view',
                   'name': 'action_view',
                   'action': 'localfs_view',
                   'permissions': (View,),
                   },
                  {'id': 'edit',
                   'name': 'action_edit',
                   'action': 'localfs_edit_form',
                   'permissions': (ModifyPortalContent,),
                   },
                  {'id': 'contents',
                   'name': 'action_folder_contents',
                   'action': 'folder_contents',
                   'permissions': (ModifyPortalContent,),
                   },
            ),
      },
  )

class CPSLocalFS(LocalFS, Folder):
    """Object that creates Zope objects from files in the local file system."""
    
    meta_type = 'CPS LocalFS'
    portal_type = meta_type
    _type_map = [] # TODO
    _properties = LocalFS._properties

    def __init__(self, id, **kw):                
        Folder.__init__(self, id, **kw)
        LocalFS.__init__(self, id, '/home/sastier/tmp/', None, None)
        LOG("*sas* ===> ", INFO, "CPSlocalFS : fin de __init__")

    def edit(self, *args, **kw):
        print args
        print kw
        

def addCPSLocalFS(self, id, **kw):
    #, basepath, username=None, password=None, REQUEST=None):
    """Add a local file system object to a folder
  
    In addition to the standard Zope object-creation arguments,
    'id' and 'title', the following arguments are defined:

        basepath -- The base path of the local files.
        username -- Username for a network share (win32 only).
        password -- Password for a network share (win32 only).
    """ 
    LOG("*sas* ===> ",INFO,"CPSLocalFS: addCPSLocalFS()")
    ob = CPSLocalFS(id, **kw)
    LOG("*sas* ===> ",INFO,"avant CPSBase_adder")
    CPSBase_adder(self, ob)
    LOG("*sas* ===> ",INFO,"apres CPSBase_adder")


