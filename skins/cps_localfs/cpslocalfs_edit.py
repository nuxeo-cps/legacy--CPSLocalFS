##parameters=title='', path='', description='', REQUEST=None
# $Id$

"""
Edit the CPSLocalFS properties
"""

# converts CMFDefault/RegistrationTool.py sentences into msgids
conversion = {
  
    'Base path is not valide':
        'invalide_basepath_message',
}



fs = context.getContent()
bck_title = fs.getTitle()
bck_path = fs.getPath()
bck_description = fs.getDescription()

try:
    fs.editProperties(title, path, description)

except OSError:
    fs.editProperties(bck_title, bck_path, bck_description)
    REQUEST.set('portal_status_message','stm_cpslocalfs_unknown_basepath_message')
    return context.cpslocalfs_edit_form(context, REQUEST)

except TypeError:
    fs.editProperties(bck_title, bck_path, bck_description)
    REQUEST.set('portal_status_message','stm_cpslocalfs_insufficients_rights_message')
    return context.cpslocalfs_edit_form(context, REQUEST)

except AttributeError:
    fs.editProperties(bck_title, bck_path, bck_description)
    REQUEST.set('portal_status_message','stm_cpslocalfs_invalid_content_in_folder_message')
    return context.cpslocalfs_edit_form(context, REQUEST)

except NameError:
    fs.editProperties(bck_title, bck_path, bck_description)
    REQUEST.set('portal_status_message','stm_cpslocalfs_invalid_basepath_message')
    return context.cpslocalfs_edit_form(context, REQUEST)




context.REQUEST.RESPONSE.redirect('./cpslocalfs_folder_contents')
    




