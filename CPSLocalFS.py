"""Local File System product

$Id$"""
__version__='$Revision$'


from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.CPSCore.CPSBase import CPSBase_adder
from Products.CPSDocument.CPSDocument import CPSDocument as BaseDocument


from Products.CMFCore import CMFCorePermissions
from Products.LocalFS.LocalFS import LocalFS
from Products.CPSDefault.Folder import Folder
from AccessControl import ClassSecurityInfo
from Products.PortalTransforms.MimeTypesRegistry import MimeTypesRegistry
from Globals import InitializeClass


    
factory_type_information = ({
      'id': 'CPS Local File System',
      'title': 'portal_type_CPSLocalFS_title',
      'icon': 'localfs_icon.gif',
      'product': 'CPSLocalFS',
      'meta_type': 'CPS Document',
      'factory': 'addCPSLocalFS',
      'filter_content_types': 0,
      'allowed_content_types': (),
      'immediate_view':'cpslocalfs_edit_form',
      'actions': (
                  {'id': 'view',
                  'name': 'action_view',
                  'action': 'cpslocalfs_folder_contents',
                  'permissions': (View,)},
                  {'id': 'edit',
                   'name': 'action_modify',
                   'action': 'cpslocalfs_edit_form',
                   'permissions': (ModifyPortalContent,),},
                            
                
            ),
     'cps_proxy_type': '',
     'cps_is_searchable': 0,
      },
  )

class CPSLocalFS(LocalFS, BaseDocument):
    """Object that creates Zope objects from files in the
       local file system."""
   
    meta_type = 'CPSLocalFS'
    portal_type = meta_type
    # _type_map = [] # TODO
    _properties = LocalFS._properties

    
    security = ClassSecurityInfo()

    def __init__(self, id, **kw):
        BaseDocument.__init__(self, id, **kw)
        self.datamodel = kw.get('datamodel')
        self.lfs_title = self.datamodel['Title']
        self.lfs_basepath = self.datamodel['Basepath']
        self.lfs_description = self.datamodel['Description']
        LocalFS.__init__(self, self.lfs_title, self.lfs_basepath, None, None)
    
            
    #    Folder.__init__(self, id, **kw)

     
    security.declareProtected(ModifyPortalContent, 'edit')
    def edit(self, *args, **kw):
        print args
        print kw
                
    security.declareProtected(ModifyPortalContent, 'editProperties')
    def editProperties(self, title, basepath, description):
        """ Edit CPSLocalFS object properties."""
        self.lfs_description = description
        self.lfs_title = title
        self.lfs_basepath = basepath

##        LOG("* editLFS * datamodel ==> ",INFO,self.datamodel)
##        LOG("* editLFS * title ==> ",INFO,self.lfs_title)
##        LOG("* editLFS * descrip ==>", INFO,self.lfs_description)
##        LOG("* editLFS * basepath ==>", INFO,self.lfs_basepath)
        self.manage_changeProperties(title=title, description=description,\
                                    basepath=basepath)
        
    security.declareProtected(ModifyPortalContent, 'getIconPath')
    def getIconPath(self, type):
        """ Return the icon registered fo a given type."""
        types_registry = MimeTypesRegistry()
        mimetypes = types_registry.lookup(type)
        for type in mimetypes:
            return type.icon_path
       

InitializeClass(CPSLocalFS)

def addCPSLocalFS(container, id, **kw):
    """Add a CPS local file system object to a folder
  
    In addition to the standard Zope object-creation arguments,
    'id' and 'title', the following arguments are defined:

        basepath -- The base path of the local files.
    """
    ob = CPSLocalFS(id, **kw)
    return CPSBase_adder(container, ob) 
 
