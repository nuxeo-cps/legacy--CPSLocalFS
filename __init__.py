"""CPS Local File System product initialization

$Id$"""


from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.CMFCorePermissions import AddPortalContent
from zLOG import LOG, INFO, ERROR, DEBUG

import CPSLocalFS

contentClasses = ()
contentConstructors = ()
contentClasses += (CPSLocalFS.CPSLocalFS,)
contentConstructors += (CPSLocalFS.addCPSLocalFS,)
fti = ()
fti += CPSLocalFS.factory_type_information

registerDirectory('skins/cps_localfs', globals())

def initialize(registrar):
    LOG("*sas* ===> ",INFO," __init__.py : initialize")
    
    utils.ContentInit('CPS Local File System',
                      content_types=contentClasses,
                      permission=AddPortalContent,
                      extra_constructors=contentConstructors,
                      fti=fti,
                      ).initialize(registrar)

