# (C) Copyright 2003 Nuxeo SARL <http://nuxeo.com>
# Author: 
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id$




from Products.CPSInstaller.CPSInstaller import CPSInstaller

class ProductInstaller(CPSInstaller):
    product_name = 'CPSLocalFS'

    SKINS = {'cps_localfs': 'Products/CPSLocalFS/skins/cps_localfs'}


    def install(self):
        self.log("Starting CPSLocalFS install.")     
        
        # Portal Workflow
        self.allowContentTypes('CPSLocalFS', ('Workspace', 'Section'))
        ws_chains = {'CPSLocalFS': 'workspace_content_wf',}
        se_chains = {'CPSLocalFS': 'workspace_content_wf',}
        self.verifyLocalWorkflowChains(self.portal['workspaces'],
                                        ws_chains)
        self.verifyLocalWorkflowChains(self.portal['sections'],
                                        se_chains)
        
        # Portal Types
        lfs_types = self.portal.getCPSLocalFSDocumentTypes()
        self.verifyFlexibleTypes(lfs_types)
        self.log(str(lfs_types))

        # Portal Schemas
        lfs_schemas = self.portal.getCPSLocalFSDocumentSchemas()
        self.verifySchemas(lfs_schemas)
        self.log(str(lfs_schemas))

        # Portal Layouts
        lfs_layouts = self.portal.getCPSLocalFSDocumentLayouts()
        self.verifyLayouts(lfs_layouts)
        self.log(str(lfs_layouts))
      
        # Portal Skins
        self.verifySkins(self.SKINS)

        self.log("End of CPSLocalFS install.")
        self.finalize()

def install(self):
    installer = ProductInstaller(self)
    installer.install()
    return installer.logResult()



