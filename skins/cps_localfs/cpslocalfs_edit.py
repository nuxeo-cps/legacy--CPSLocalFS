##parameters=title='', basepath='', description='', REQUEST=None
# $Id$

"""
Edit the CPSLocalFS properties
"""

# converts CMFDefault/RegistrationTool.py sentences into msgids
conversion = {
  
    'Base path is not valide':
        'invalide_basepath_message',
}


try:
    fs = context.getContent()
    fs.editProperties(title, basepath, description)

except OSError:
    REQUEST.set('portal_status_message','cpslocalfs_unknown_basepath_message')
    return context.cpslocalfs_edit_form(context, REQUEST)

except TypeError:
    REQUEST.set('portal_status_message','cpslocalfs_insufficients_rights_message')
    return context.cpslocalfs_edit_form(context, REQUEST)

except AttributeError:
    REQUEST.set('portal_status_message','cpslocalfs_invalid_content_in_folder_message')
    return context.cpslocalfs_edit_form(context, REQUEST)

except NameError:
    REQUEST.set('portal_status_message','cpslocalfs_invalid_basepath_message')
    return context.cpslocalfs_edit_form(context, REQUEST)


context.REQUEST.RESPONSE.redirect('./cpslocalfs_folder_contents')

