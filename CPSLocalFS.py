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
#from zLOG import LOG, DEBUG, INFO

    
factory_type_information = ({
      'id': 'CPS Local File System',
      'title': 'portal_type_CPSLocalFS_title',
      'description': 'portal_type_CPSLocalFS_description',
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




class CPSLocalFS(LocalFS, Folder):
    """Object that creates Zope objects from files in the
       local file system."""
    meta_type = 'CPSLocalFS'
    portal_type = meta_type
    _properties = LocalFS._properties
    security = ClassSecurityInfo()


    def __init__(self, id, **kw):
        Folder.__init__(self, id, **kw)
        datamodel = kw.get('datamodel')
        self.setTitle(datamodel['Title'])
        # Warning : mother class LocalFS own a 'basepath'
        # attribut that must not be override
        self.setPath(datamodel['Basepath'])
        self.setDescription(datamodel['Description'])
        LocalFS.__init__(self, self.getTitle(), self.getPath(), None, None)

        
    security.declareProtected(ModifyPortalContent, 'edit')
    def edit(self, *args, **kw):
        print args
        print kw

                
    security.declareProtected(ModifyPortalContent, 'editProperties')
    def editProperties(self, title, path, description):
        """ Edit CPSLocalFS object properties."""
        self.setPath(path)
        self.setDescription(description)
        self.setTitle(title)
        self.manage_changeProperties(title=title, description=description,\
                                    basepath=path)
        
    security.declareProtected(ModifyPortalContent, 'getIconPath')
    def getIconPath(self, type):
        """ Return the icon registered fo a given type."""
        types_registry = MimeTypesRegistry()
        mimetypes = types_registry.lookup(type)
        for type in mimetypes:
            return type.icon_path


    #
    # Getters and Setters
    #

    #--
    def getPath(self):
        return self.path

    def setPath(self, a_path):
        self.path = a_path

    #--
    def getDescription(self):
        return self.description

    def setDescription(self, a_description):
        self.description = a_description

    #--
    def getTitle(self):
        return self.title

    def setTitle(self, a_titre):
        self.title = a_titre

    #
    # Helpers
    #

    #--
    def toString(self):
        """ Returns a string of the instance attributes title,
            path and description. """
        st = " \n"
        st += "Title: "+self.getTitle()+"\n"
        st += "Path: "+self.getPath()+"\n"
        st += "Description: "+self.getDescription()+"\n"
        return st


        
InitializeClass(CPSLocalFS)

def addCPSLocalFS(container, id, **kw):
    """Add a CPS local file system object to a folder
  
    In addition to the standard Zope object-creation arguments,
    'id' and 'title', the following arguments are defined:

        basepath -- The base path of the local files.
    """
    ob = CPSLocalFS(id, **kw)
    return CPSBase_adder(container, ob) 
 
