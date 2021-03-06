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
 - Make sure you have the right version of LocalFS in your
   'Products' field.
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
from os.path import exists, isdir
from sys import platform
from zLOG import LOG, INFO, DEBUG


class ProductInstaller(CPSInstaller):
    """ Installer for CPSLocalFS Product. """
    product_name = 'CPSLocalFS'
    SKINS = {'cps_localfs': 'Products/CPSLocalFS/skins/cps_localfs'}

    def install(self):
        self.log("Starting CPSLocalFS install.")

        # Make sure this install is run on a linux plateform
        if platform[:5]!='linux':
            self.log("CPSLocalFS can only be installed on a linux server")
            self.log("CPSLocalFS install aborted")
        self.log("Operating System: " + platform[:5])

        # Test if CPSLocalFS has all it needs.
        if not self.testVersionLocalFS():
            self.log("LocalFS-1.2-andreas or LocalFS-1.3-andreas not found")
            self.log("CPSLocalFS install aborted")
            return 0

        if not self.testReachConfigFile():
            self.log("'localfs_dirs.txt' not found in HOME_ZOPE/var/")
            self.log("CPSLocalFS install aborted")
            return 0

        # Portal Skins.
        self.verifySkins(self.SKINS)
        self.resetSkinCache()

        # Portal Translation .
        self.setupTranslations('CPSLocalFS')

        # Portal Workflow.
        self.allowContentTypes('CPSLocalFS', ('Workspace', 'Section'))
        ws_chains = {'CPSLocalFS': 'workspace_folder_wf',}
        se_chains = {'CPSLocalFS': 'section_folder_wf',}
        self.verifyLocalWorkflowChains(self.portal['workspaces'],
                                        ws_chains)
        self.verifyLocalWorkflowChains(self.portal['sections'],
                                        se_chains)

        # Portal Widgets.
        lfs_widgets = self.portal.getCPSLocalFSDocumentWidgets()
        self.verifyWidgets(lfs_widgets)
        #self.log(str(lfs_widgets))
        
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
        
        # Portal Actions :
        # call to updateActions removed, this method has been
        # wrote as an exemple of how to remove the 'action_status_history'
        # on CPSLocalFS but this should be done in the product using
        # CPSLocalFS, not here.

        #self.updateActions()

        self.log("End of CPSLocalFS install.")
        self.finalize()

    def updateActions(self):
        """ Remove action_status_history, should not be done in 
        CPSLocalFS but in the product using it.
        """
        actiontool = getToolByName(self.portal, 'portal_actions')
        self.log("les actions du portail : ")
        for action in actiontool._actions:
            if action.Title() == 'action_status_history':
                action.condition = Expression("python:getattr(object,\
                'portal_type', None) not in ('CPSLocalFS','Section',\
                'Workspace', 'Portal', 'Calendar', 'Event')")

    def testVersionLocalFS(self):
        required_version =('LocalFS-1-2-andreas', 'LocalFS-1-3-andreas')
        version_path = str(INSTANCE_HOME) + "/Products/LocalFS/version.txt"

        if not exists(version_path):
            return 0
        else:
            version_file= open(version_path)
            installed_version = version_file.readline()
            version_file.close()
            return installed_version in required_version
    
    def testReachConfigFile(self):
        config_file_path = str(INSTANCE_HOME) +"/var/localfs_dirs.txt"
        return exists(config_file_path)
        
def install(self):
    installer = ProductInstaller(self)
    installer.install()
    return installer.logResult()
