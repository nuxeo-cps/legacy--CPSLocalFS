##parameters=description='', basepath='', title='',
# $Id$

"""
Edit the CPSLocalFS properties
"""
context.editProperties(title=title, basepath=basepath, description=description)
context.REQUEST.RESPONSE.redirect('./cpslocalfs_folder_contents')

