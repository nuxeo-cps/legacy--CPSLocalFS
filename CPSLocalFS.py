"""Local File System product

$Id$"""
__version__='$Revision$'

from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.CPSCore.CPSBase import CPSBase_adder
from Products.CMFCore import CMFCorePermissions
from Products.LocalFS.LocalFS import LocalFS
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.CPSDocument.CPSDocument import CPSDocument as BaseDocument
from os.path import exists, isdir
from os import access, X_OK, R_OK, W_OK, listdir
#from Products.PortalTransforms.MimeTypesRegistry import MimeTypesRegistry

factory_type_information = (
    {
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
                    'permissions': (View, )},
                   {'id': 'edit',
                    'name': 'action_modify',
                    'action': 'cpsdocument_edit_form',
                    'permissions': (ModifyPortalContent, ), },
                 ),
      'cps_proxy_type': '',
      'cps_is_searchable': 0,
    },
  )

class CPSLocalFS(LocalFS, BaseDocument):
    """
    Creat CPSLocalFS to edit objects
    on the file system.
    """
    
    meta_type = 'CPSLocalFS'
    portal_type = meta_type
    _properties = LocalFS._properties
    security = ClassSecurityInfo()

    def __init__(self, id, **kw):
        BaseDocument.__init__(self, id, **kw)
        datamodel = kw.get('datamodel')
        title = datamodel['Title']
        basepath = datamodel['basepath']
        LocalFS.__init__(self, id, title, basepath, None, None)
        
    security.declareProtected(ModifyPortalContent, 'edit')
    def edit(self, *args, **kw):
        print args
        print kw
        
    security.declareProtected(ModifyPortalContent, 'updateProperties')
    def updateProperties(self):
        """ Update CPSLocalFS object properties."""
        self.manage_changeProperties(title = self.getTitle(),
                                    description = self.getDescription(),
                                    basepath = self.getPath())

    security.declareProtected(ModifyPortalContent, 'isAccessible')
    def isAccessible(self,path):
        """ Check if a path points to a file or directory and if it has
        read or exec access rights."""
        if isdir(path):
            return access(path, R_OK and X_OK and W_OK)
        else:
            return access(path, R_OK)

    security.declarePrivate('postCommitHook')
    def postCommitHook(self, datamodel=None):
        """Called after the datamodel commit, its purpose is to
        update the basepath value of LocalFS."""
        self.updateProperties()
               
##    security.declareProtected(ModifyPortalContent, 'getIconPath')
##    def getIconPath(self, type):
##        """ Return the icon registered fo a given type."""
##        types_registry = MimeTypesRegistry()
##        mimetypes = types_registry.lookup(type)
##        for type in mimetypes:
##            return type.icon_path


    #
    # Getters and Setters
    #

    #--
    def getPath(self):
        return self.basepath

    def setPath(self, path):
        self.basepath= path

    #--
    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description

    #--
    def getTitle(self):
        return self.title

    def setTitle(self, titre):
        self.title = titre

    #
    # Helpers
    #

    #--
    def toString(self):
        """
        Returns a string of the instance attributes title,
        path and description.
        """
        st = " \n"
        st += "Title: " +self.getTitle()+ "\n"
        st += "Path: " +self.getPath()+ "\n"
        st += "Description: " +self.getDescription()+ "\n"
        return st
        
InitializeClass(CPSLocalFS)


def addCPSLocalFS(container, id, **kw):
    """
    Add a CPS local file system object to a folder
    """
    ob = CPSLocalFS(id, **kw)
    return CPSBase_adder(container, ob)
