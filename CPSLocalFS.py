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
from zLOG import LOG, DEBUG

    
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
                   'action': 'cpsdocument_edit_form',
                   'permissions': (ModifyPortalContent,),},
                            
                
            ),
     'cps_proxy_type': '',
     'cps_is_searchable': 0,
      },
  )




class CPSLocalFS(Folder):
    """Object that creates Zope objects from files in the
       local file system."""
    meta_type = 'CPSLocalFS'
    portal_type = meta_type
    _properties = LocalFS._properties
    security = ClassSecurityInfo()


    def __init__(self, id, **kw):
        LOG("CPSLocalFS: ", DEBUG, "init")
        Folder.__init__(self, id, **kw)
        datamodel = kw.get('datamodel')
        self.setTitle(datamodel['Title'])
        # Warning : mother class LocalFS own a 'basepath'
        # attribut which must not be override
        self.setPath(datamodel['lfsbasepath'])
        self.setDescription(datamodel['Description'])
        lfs = LocalFS(self.getTitle(), self.getPath(), None, None)
       # lfs = LocalFS("aTitleForCPSLocalFS","/home/sastier/tmp",None,None)
        self.setLocalFS(lfs)


        
    security.declareProtected(ModifyPortalContent, 'edit')
    def edit(self, *args, **kw):
        print args
        print kw

    def getContent(self):
        """ returns a localFS contents"""
        return self.getLocalFS().getContent()

    def updateLocalFSAttributs(self):
        """ Add LocalFS attributs to CPSLocalFS """
        lfs_items = self.getLocalFS().getContent().getFolderContents()
        for item in lfs_items:
            setattr(self,item.getId(),item)
        return  "Attribut added !"

                
    security.declareProtected(ModifyPortalContent, 'editProperties')
    def editProperties(self):
        """ Edit CPSLocalFS object properties."""
        LOG("EditProperties: ", DEBUG, "init")
        lfs = self.getLocalFS()
        lfs.manage_changeProperties(title = self.getTitle(),\
                                    description = self.getDescription(),\
                                    basepath = self.getPath())
        
    security.declareProtected(ModifyPortalContent, 'getIconPath')
    def getIconPath(self, type):
        """ Return the icon registered fo a given type."""
        types_registry = MimeTypesRegistry()
        mimetypes = types_registry.lookup(type)
        for type in mimetypes:
            return type.icon_path

    security.declarePrivate('postCommitHook')
    def postCommitHook(self, datamodel=None):
        # this is called just after the dm commit
        self.editProperties()
      


    #
    # Getters and Setters
    #

    #--
    def getLocalFS(self):
        return self.localFS

    def setLocalFS(self, a_localFS):
        LOG("SetLocalFS: ", DEBUG, "init")
        self.localFS = a_localFS


    #--
    def getPath(self):
        return self.lfsbasepath

    def setPath(self, a_path):
        self.lfsbasepath= a_path

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
 
