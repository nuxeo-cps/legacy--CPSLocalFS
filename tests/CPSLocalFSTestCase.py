
from Testing import ZopeTestCase
from Products.CPSDefault.tests import CPSTestCase

ZopeTestCase.installProduct('CPSDocument')
ZopeTestCase.installProduct('CPSSchemas')
ZopeTestCase.installProduct('LocalFS')
ZopeTestCase.installProduct('CPSLocalFS')

CPSTestCase.setupPortal()

class CPSLocalFSTestCase(CPSTestCase.CPSTestCase):
    pass

class CPSLocalFSInstaller(CPSTestCase.CPSInstaller):
    def addPortal(self,id):
        print "Adding CPSLocalFS product"
        # First add a CPS Default Site
        factory = self.app.manage_addProduct['CPSDefault']
        factory.manage_addCPSDefaultSite(id,
            root_password1="passwd", root_password2="passwd",
            langs_list=['en'])
        portal = getattr(self.app, id)
        # Then call CPSLocalFS updater
        cpslocalfs_installer = ExternalMethod('cpslocalfs_installer',
            'cpslocalfs_installer','CPSLocalFS.install','install')
        portal._setObject('cpslocalfs_installer',cpslocalfs_installer)
        portal.cpslocalfs_installer()

CPSTestCase.setupPortal(CPSLocalFSInstaller)


