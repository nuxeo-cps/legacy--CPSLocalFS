# (C) Copyright 2004 Nuxeo SARL <http://nuxeo.com>
# Author: Sylvain Astier <sastier@nuxeo.com>
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

"""
CPSLocalFS Installer

HOWTO USE THAT ?
 - Make sure you have LocalFS-1-1-0 in your Products field.
 - Log into the ZMI as manager
 - Go to your CPS root directory
 - Create an External Method with the following parameters:

     id    : CPSLocalFS INSTALLER (or whatever)
     title : CPSLocalFS INSTALLER (or whatever)
     Module Name   :  CPSLocalFS.install
     Function Name : install
 - save it
 - click now the test tab of this external method.
"""

from Products.CPSInstaller.CPSInstaller import CPSInstaller
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression

class ProductInstaller(CPSInstaller):
    product_name = 'CPSLocalFS'

    SKINS = {'cps_localfs': 'Products/CPSLocalFS/skins/cps_localfs'}

    def install(self):
        self.log("Starting CPSLocalFS install.")

        # Portal CPS Update.
        self.updateCPS()
        
        # Portal Skins.
        self.verifySkins(self.SKINS)
        self.resetSkinCache()

        # Portal Translation 
        self.setupTranslations('CPSLocalFS')
        
        # Portal Workflow.
        self.allowContentTypes('CPSLocalFS', ('Workspace', 'Section'))
        ws_chains = {'CPSLocalFS': 'workspace_folder_wf',}
        se_chains = {'CPSLocalFS': 'workspace_folder_wf',}
        self.verifyLocalWorkflowChains(self.portal['workspaces'],
                                        ws_chains)
        self.verifyLocalWorkflowChains(self.portal['sections'],
                                        se_chains)
        
        # Portal Types.
        lfs_types = self.portal.getCPSLocalFSDocumentTypes()
        self.verifyFlexibleTypes(lfs_types)
        #self.log(str(lfs_types))
        self.allowContentTypes('CPSLocalFS', ('Workspace', 'Section'))
        ptypes = {
            'CPSLocalFS' : {
                'allowed_content_types': (),
                'typeinfo_name': 'CPSLocalFS: CPSLocalFS',
                'add_meta_type': 'Factory-based Type Information',
             },
        }
        self.verifyContentTypes(ptypes)
        # Portal Schemas.
        lfs_schemas = self.portal.getCPSLocalFSDocumentSchemas()
        self.verifySchemas(lfs_schemas)
        #self.log(str(lfs_schemas))

        # Portal Layouts.
        lfs_layouts = self.portal.getCPSLocalFSDocumentLayouts()
        self.verifyLayouts(lfs_layouts)
        #self.log(str(lfs_layouts))

        # Portal Actions :
        #self.updateActions()
        
        self.log("End of CPSLocalFS install.")
        self.finalize()
        
    def updateCPS(self):
        """Update CPS
        """
        return self.portal.cpsupdate(self.portal)
    
    def updateActions(self):
        """ Remove action_status_history, should not be done in \
        CPSLocalFS but in the product using it.
        """
        wftool = getToolByName(self.portal,'portal_actions')
        self.log("les actions du portail : ")
        for action in wftool._actions:
            if action.Title() == 'action_status_history':
                action.condition = Expression("python:getattr(object, \
                'portal_type', None) not in ('CPSLocalFS','Section', \
                'Workspace', 'Portal', 'Calendar', 'Event')")


def install(self):
    installer = ProductInstaller(self)
    installer.install()
    return installer.logResult()



