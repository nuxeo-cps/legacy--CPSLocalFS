"""Local File System product

$Id$"""
__version__='$Revision$'


from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.CPSCore.CPSBase import CPSBaseDocument, CPSBase_adder
from Products.CMFCore import CMFCorePermissions
from Products.LocalFS.LocalFS import LocalFS
from Products.CPSDefault.Folder import Folder
from AccessControl import ClassSecurityInfo
from Products.PortalTransforms.MimeTypesRegistry import MimeTypesRegistry


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
               
                  {'id': 'modify',
                   'name': 'action_modify',
                   'action': 'cpslocalfs_edit_form',
                   'permissions': (ModifyPortalContent,),
                   },
            ),
      },
  )

class CPSLocalFS(LocalFS, Folder):
    """Object that creates Zope objects from files in the
       local file system."""
    
    meta_type = 'CPS LocalFS'
    portal_type = meta_type
    # _type_map = [] # TODO
    _properties = LocalFS._properties

    security = ClassSecurityInfo()

    def __init__(self, id, **kw):
        Folder.__init__(self, id, **kw)
        basepath = kw.get('basepath','/home/sastier/tmp')
        LocalFS.__init__(self, id, basepath, None, None)
     
    security.declareProtected(ModifyPortalContent, 'edit')
    def edit(self, *args, **kw):
        print args
        print kw
        
    security.declareProtected(ModifyPortalContent, 'editProperties')
    def editProperties(self, title='', description='', basepath=''):
        """ Edit CPSLocalFS object properties."""
        self.description = description
        self.manage_changeProperties(title=title, description=description,\
                                     basepath=basepath)
        
    security.declareProtected(ModifyPortalContent, 'getIconPath')
    def getIconPath(self, type):
        """ Return the icon registered fo a given type."""
        types_registry = MimeTypesRegistry()
        mimetypes = types_registry.lookup(type)
        for type in mimetypes:
            return type.icon_path
        return atype
        

def addCPSLocalFS(self, id, **kw):
       #, basepath, username=None, password=None, REQUEST=None):
    """Add a local file system object to a folder
  
    In addition to the standard Zope object-creation arguments,
    'id' and 'title', the following arguments are defined:

        basepath -- The base path of the local files.
        username -- Username for a network share (win32 only).
        password -- Password for a network share (win32 only).
    """
    ob = CPSLocalFS(id, **kw)   
    CPSBase_adder(self, ob)
   
 
