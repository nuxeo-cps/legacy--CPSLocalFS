##parameters=title='', basepath='', description='',
# $Id$

"""
Edit the CPSLocalFS properties
"""

fs = context.getContent()
fs.editProperties(title, basepath, description)

context.REQUEST.RESPONSE.redirect('./cpslocalfs_folder_contents')

