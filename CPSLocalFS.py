"""Local File System product

$Id$"""
__version__='$Revision$'[11:-2]

from zLOG import LOG, INFO, DEBUG
from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.CPSCore.CPSBase import CPSBaseDocument, CPSBase_adder
from Products.CMFCore import CMFCorePermissions
from Products.LocalFS.LocalFS import LocalFS
from Products.CPSDefault.Folder import Folder
from AccessControl import ClassSecurityInfo

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
      'immediate_view':'cpslocalfs_edit_form',
      'actions': (
                  {'id': 'edit',
                   'name': 'action_edit',
                   'action': 'cpslocalfs_folder_contents',
                   'permissions': (ModifyPortalContent,),
                   },
                  {'id': 'contents',
                   'name': 'action_folder_contents',
                   'action': 'cpslocalfs_folder_contents',
                   'permissions': (ModifyPortalContent,),
                   },
            ),
      },
  )

class CPSLocalFS(LocalFS, Folder):
    """Object that creates Zope objects from files in the local file system."""
    
    meta_type = 'CPS LocalFS'
    portal_type = meta_type
   # _type_map = [] # TODO
    _properties = LocalFS._properties

    security = ClassSecurityInfo()

   

    def __init__(self, id, **kw):                
        Folder.__init__(self, id, **kw)
        XXX_default_path = '/home/sastier/tmp/'
        LocalFS.__init__(self, id, XXX_default_path, None, None)
        LOG("*sas* ===> ", INFO, "CPSlocalFS : fin de __init__")

    security.declareProtected(ModifyPortalContent, 'edit')
    def edit(self, *args, **kw):
        print args
        print kw
        
    security.declareProtected(ModifyPortalContent, 'editProperties')
    def editProperties(self, title='', description='', basepath=''):
        """Edit chat object properties.
        """
        self.manage_changeProperties(title=title, description=description, basepath=basepath)
        

def addCPSLocalFS(self, id, **kw):
    #, basepath, username=None, password=None, REQUEST=None):
    """Add a local file system object to a folder
  
    In addition to the standard Zope object-creation arguments,
    'id' and 'title', the following arguments are defined:

        basepath -- The base path of the local files.
        username -- Username for a network share (win32 only).
        password -- Password for a network share (win32 only).
    """

    title = kw.get('title','Default Title')
    basepath = kw.get('basepath', '/home/sastier/tmp')
    
    
    LOG("*sas* ===> ",INFO,"CPSLocalFS: addCPSLocalFS()")
    LOG("*sas* ===> Title: ",INFO,title)
    LOG("*sas* ===> Basepath: ",INFO,basepath)
    ob = CPSLocalFS(id, **kw)
    LOG("*sas* ===> ",INFO,"avant CPSBase_adder")
    CPSBase_adder(self, ob)
    LOG("*sas* ===> ",INFO,"apres CPSBase_adder")

