"""Local File System product

$Id$"""
__version__='$Revision$'


from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.CPSCore.CPSBase import CPSBase_adder
from Products.CMFCore import CMFCorePermissions
from Products.LocalFS.LocalFS import LocalFS
from Products.CPSDefault.Folder import Folder
from AccessControl import ClassSecurityInfo
from Products.PortalTransforms.MimeTypesRegistry import MimeTypesRegistry
from Globals import InitializeClass

from zLOG import LOG, INFO, DEBUG
    
factory_type_information = ({
      'id': 'CPS Local File System',
      'title': 'portal_type_CPSLocalFS_title',
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
                  {'id': 'new_content',  #sas
                  'name': 'action_new_content',
                  'action': 'folder_factories',
                  'permissions': (ModifyPortalContent,),
                  'visible': 0},
            ),
     'cps_proxy_type': 'document',
     'cps_is_searchable': 0,

      },
  )

class CPSLocalFS(LocalFS, Folder):
    """Object that creates Zope objects from files in the
       local file system."""
    
    meta_type = 'CPSLocalFS'
    portal_type = meta_type
    # _type_map = [] # TODO
    _properties = LocalFS._properties

    security = ClassSecurityInfo()

    def __init__(self, id, **kw):
        LOG("********** INIT *****2***",INFO,"")
        datamodel = kw.get('datamodel')
        self.title = datamodel['Title']
        self.basepath = datamodel['Basepath']
        self.description = datamodel['Description']
        

        LOG("*__init__* datamodel ==> ",INFO,self.datamodel)
        LOG("*__init__* title ==> ",INFO,self.title)
        LOG("*__init__* descrip ==>", INFO,self.description)
        LocalFS.__init__(self, self.title, self.basepath, None, None)
        Folder.__init__(self, id, **kw)

        
   
     
    security.declareProtected(ModifyPortalContent, 'edit')
    def edit(self, *args, **kw):
        print args
        print kw

   
        
        
   # security.declareProtected(ModifyPortalContent, 'editProperties')
    def editProperties(self, title='', description='', basepath=''):
        """ Edit CPSLocalFS object properties."""
        self.description = description
        self.title = title
        self.basepath = basepath

        LOG("*editProp* id  ==> ",INFO,id)
        LOG("*editProp* kw ==> ",INFO,kw)
        LOG("*editProp* basepath ==>", INFO, basepath)
        LOG("*editProp* title ==>",INFO,title)
        
        
        self.manage_changeProperties(title=title, description=description,\
                                     basepath=basepath)
        
    #security.declareProtected(ModifyPortalContent, 'getIconPath')
    def getIconPath(self, type):
        """ Return the icon registered fo a given type."""
        types_registry = MimeTypesRegistry()
        mimetypes = types_registry.lookup(type)
        for type in mimetypes:
            return type.icon_path
        return atype

#InitializeClass(Folder) #sas

def addCPSLocalFS(container, id, REQUEST=None, **kw):
       #, basepath, username=None, password=None, REQUEST=None):
    """Add a local file system object to a folder
  
    In addition to the standard Zope object-creation arguments,
    'id' and 'title', the following arguments are defined:

        basepath -- The base path of the local files.
        username -- Username for a network share (win32 only).
        password -- Password for a network share (win32 only).
    """
    LOG("*addCPSLocalFS* --- appel a init",INFO,"")
    ob = CPSLocalFS(id, **kw)   
    LOG("*addCPSLocalFS* REQUEST => ", INFO, REQUEST)
    LOG("*addCPSLocalFS* kw => ", INFO, kw)
    return CPSBase_adder(container, ob, REQUEST=REQUEST) #sas
 
