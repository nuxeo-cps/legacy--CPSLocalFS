from Products.CPSSchemas.Widget import CPSWidget
from Products.CPSSchemas.BasicWidgets import CPSStringWidget,\
     CPSStringWidgetType
from Globals import InitializeClass
from Products.CPSSchemas.WidgetTypesTool import WidgetTypeRegistry
from Products.CPSSchemas.BasicWidgets import renderHtmlTag
from Products.LocalFS.LocalFS import LocalFS
from Products.CPSLocalFS.CPSLocalFS import CPSLocalFS
from os.path import exists, isdir
from os import access, W_OK, R_OK, listdir
from zLOG import LOG, ERROR


class PathWidget(CPSStringWidget):
    """ Path Widget class, used to get the user inputs in order to
    create an instance of CPSLocalFS. Its main purpose it to validate
    the basepath input.
    """

    meta_type = "Path Widget"
    field_types = ('CPS String Field', )
    display_width = 20
    size_max = 100
    _properties = CPSStringWidget._properties
    
    def prepare(self, datastructure, **kw):
        """Prepare datastructure from datamodel."""
        datamodel = datastructure.getDataModel()
        datastructure[self.getWidgetId()] = datamodel[self.fields[0]]
     

    def validate(self, datastructure, **kw):
        """Update datamodel from user data in datastructure.
        Only path listed in the var/localfs_dirs.txt can be
        acceded, moreover CPSLocalFS will only display files
        on which the Zope process has read and write access
        rights."""
        widget_id = self.getWidgetId()
        datamodel = datastructure.getDataModel()
        field_id = self.fields[0]
        path = datastructure.get(widget_id, '')

        # provide path : '/home/monrep' must match
        # the line '/home/monrep/' in the config file,
        # so we add an extra '/' to path if needed.
        if path[-1]!='/':
            path+='/'

        # Make sure path doesn't feature any '..'
        if path.find("..") != -1:
            datastructure.setError(widget_id, 
                "psm_cpslocalfs_invalid_basepath_message")
            return 0
        
        # Checks if the configuration file is accessible.
        f_path = CLIENT_HOME + "/localfs_dirs.txt"
        if not exists(f_path):
            LOG("PathWidget: ", ERROR,
                "missing localfs_dirs.txt configuration file")
            datastructure.setError(widget_id, 
                "psm_cpslocalfs_missing_config_file_message")
            return 0
        
        # checks if the provided path has been authorized.
        f = open('localfs_dirs.txt')
        authorized = 0
        for line in f.readlines():
            if line == "":
                break
            line = line[:-1]

            # allowing access to '/home/auser/content'
            # must not allow access to '/home/auser/content1'       
            if not line.startswith('#'):
                if line[-1]!='/':
                    line+='/'
                if path.startswith(line):
                    authorized = 1
                
        if not authorized:
            LOG("PathWidget: ", ERROR, "\n Provided path '" +path+ 
               "'is unauthorized, must match a prefix in var/localfs_dirs.txt")
            datastructure.setError(widget_id, 
                "psm_cpslocalfs_unauthorized_basepath_message")
            return 0
          
        # we consider the path to be valid
        ok = 1
        if not exists(path):
            LOG("PathWidget: ", ERROR, "Path doesn't exist")
            datastructure.setError(widget_id, 
                "psm_cpslocalfs_invalid_basepath_message")
            ok = 0
        else:
            if not isdir(path):
                LOG("PathWidget: ", ERROR, "Path is not a directory")
                datastructure.setError(widget_id, 
                    "psm_cpslocalfs_unknown_basepath_message")
                ok = 0
            else:
                datamodel.set(field_id, path)
                if not access(path, R_OK and W_OK):
                    LOG("PathWidget: ", ERROR, "Insufficient Rights")
                    datastructure.setError(widget_id, 
                        "psm_cpslocalfs_insufficients_rights_message")
                    ok = 0     
        return ok

    
    def _getFunction(self):
        """Return the name of the function to call."""
        raise NotImplementedError
    
    def render(self, mode, datastructure, **kw):
        """Render this widget from the datastructure or datamodel."""
        value = datastructure[self.getWidgetId()]
        if mode in ['view', 'edit', 'create']:
            desc = {
                  'id': self.getHtmlWidgetId(),
                  'name': self.getHtmlWidgetId(),
                  'value': value,
                  'size': self.display_width,
                  }
            if self.size_max:
                desc['maxlength'] = self.size_max
            return renderHtmlTag('input', **desc)
    

InitializeClass(PathWidget)


class PathWidgetType(CPSStringWidgetType):
    """Function Select widget type."""
    meta_type = "Path Widget Type"
    cls = PathWidget

InitializeClass(PathWidgetType)



# Register widget types.
WidgetTypeRegistry.register(PathWidgetType,PathWidget)
