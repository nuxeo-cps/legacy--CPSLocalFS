from Products.CPSSchemas.Widget import CPSWidget
from Products.CPSSchemas.BasicWidgets import CPSStringWidget, CPSStringWidgetType
from Globals import InitializeClass
from Products.CPSSchemas.WidgetTypesTool import WidgetTypeRegistry
from Products.CPSSchemas.BasicWidgets import _isinstance, renderHtmlTag
from Products.LocalFS.LocalFS import LocalFS
from Products.CPSLocalFS.CPSLocalFS import CPSLocalFS
from Globals import InitializeClass
#from zLOG import LOG, DEBUG
from os.path import exists, isdir
from os import access, W_OK, listdir


class PathWidget(CPSStringWidget):
    """ Path Widget class, used to get the user inputs in order to create
        an instance of CPSLocalFS. Its main purpose it to validate the
        basepath input."""

    meta_type = "Path Widget"
    field_types = ('CPS String Field',)
    display_width = 20
    size_max = 100
    _properties = CPSStringWidget._properties
    
    def prepare(self, datastructure, **kw):
        """Prepare datastructure from datamodel."""
        datamodel = datastructure.getDataModel()
        datastructure[self.getWidgetId()] = datamodel[self.fields[0]]
     

    def validate(self, datastructure, **kw):
        """Update datamodel from user data in datastructure."""
        widget_id = self.getWidgetId()
        datamodel = datastructure.getDataModel()
        field_id = self.fields[0]
        a_path = datastructure.get(widget_id,'')
        
        ok = 1
        if not exists(a_path):
            #LOG("PathWidget: ", DEBUG, "Path doesn't exist")
            datastructure.setError(widget_id,"psm_cpslocalfs_invalid_basepath_message")
            ok = 0
        else:
            if not isdir(a_path):
                #LOG("PathWidget: ", DEBUG, "Path is not a directory")
                datastructure.setError(widget_id,"psm_cpslocalfs_unknown_basepath_message")
                ok = 0
            else:
                if not access(a_path,W_OK):
                    #LOG("PathWidget: ", DEBUG, "Insufficient Rights")
                    datastructure.setError(widget_id,"psm_cpslocalfs_insufficients_rights_message")
                    ok = 0
                else:
                    # Check if the folder contains won't crash LocalFS.
                    try:
                        lfs = LocalFS("tmplocalfsforcpslocalfs", a_path, None, None)
                        lfs_content = lfs.getFolderContents()
                    except  TypeError:
                        datastructure.setError(widget_id,"psm_cpslocalfs_insufficients_rights_message")
                        ok = 0
                    except  AttributeError:
                        datastructure.setError(widget_id,"psm_cpslocalfs_invalid_content_in_folder_message")
                        ok = 0       
                    datamodel.set(field_id,a_path)
        return ok

    
    def _getFunction(self):
        """Return the name of the function to call."""
        raise NotImplementedError
    
    def render(self, mode, datastructure, **kw):
        """Render this widget from the datastructure or datamodel."""
        value = datastructure[self.getWidgetId()]
        
        if mode in ['view','edit','create']:
            desc = {
                  'id'  : self.getHtmlWidgetId(),
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



#
# Register widget types.
#

WidgetTypeRegistry.register(PathWidgetType,PathWidget)
