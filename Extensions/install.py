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


def install(self):
    """
    CSPLocalFS Starting Point !
    """

    # CREATE THE INSTALLER
    installer = CPSInstaller(self, 'CPSLocalFS')
    installer.log("Starting CPSLocalFS Install")

    # PORTAL TYPES
    installer.allowContentTypes('CPSLocalFS', ('Workspace', 'Section'))
    ptypes = {
        'CPSLocalFS' : {
              'allowed_content_types': (),
              'typeinfo_name': 'CPSLocalFS: CPSLocalFS',
              'add_meta_type': 'Factory-based Type Information',
        },
    }
    installer.verifyContentTypes(ptypes)

    #   WORKFLOW ASSOCIATIONS
    ws_chains = {'CPSLocalFS': 'workspace_content_wf',}
    se_chains = {'CPSLocalFS': 'workspace_content_wf',}
    installer.verifyLocalWorkflowChains(installer.portal['workspaces'],
                                        ws_chains)
    installer.verifyLocalWorkflowChains(installer.portal['sections'],
                                        se_chains)

    # SKINS
    skins = {'cps_localfs': 'Products/CPSLocalFS/skins/cps_localfs'}
    installer.verifySkins(skins)


##    # Action
##    #############################################
##    installer.verifyAction('portal_actions',
##            id='status_history',
##            name='action_status_history',
##            action='string: ${object/absolute_url}/content_status_history',
##            # XXX: this is as messy as what is done in cpsinstall
##           # condition="python:getattr(object, 'portal_type', None) not in "
##            #          "('Section', 'Workspace', 'Portal', 'Calendar', 'Event', "
##             #         "'CPSForum', 'CPSChat',)",
##            permission='View',
##            category='workflow')

##    ##############################################
##    # i18n support
##    ##############################################
##    installer.verifyMessageCatalog('cpschat', 'CPSChat messages')
##    installer.setupTranslations(message_catalog='cpschat')

    # Finished!
    installer.finalize()
    installer.log("End of CPSLocalFS install")
    return installer.logResult()

