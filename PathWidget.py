from Products.CPSSchemas.Widget import CPSWidget
from Products.CPSSchemas.BasicWidgets import CPSStringWidget, CPSStringWidgetType
from Globals import InitializeClass
from Products.CPSSchemas.WidgetTypesTool import WidgetTypeRegistry
from Products.CPSSchemas.BasicWidgets import _isinstance, renderHtmlTag

from Products.LocalFS.LocalFS import LocalFS
from Products.CPSLocalFS.CPSLocalFS import CPSLocalFS
from cgi import escape
from Globals import InitializeClass
from zLOG import LOG, DEBUG, INFO


class PathWidget(CPSStringWidget):
    """Function String widget.

       String by calling the method specified in the _getFunction Method."""

    meta_type = "Path Widget"
    field_types = ('CPS String Field',)
    
    display_width = 20
    size_max = 100
    _properties = CPSStringWidget._properties
    
    def prepare(self, datastructure, **kw):
        """Prepare datastructure from datamodel."""
        LOG("*** PathWidget ***", INFO, " Prepare OK")
        datamodel = datastructure.getDataModel()
        datastructure[self.getWidgetId()] = datamodel[self.fields[0]]
        #pass


    def validate(self, datastructure, **kw):
        """Update datamodel from user data in datastructure."""
        LOG("*** PathWidget ***", INFO, "validate(datastructure)")
        widget_id = self.getWidgetId()
        datamodel = datastructure.getDataModel()
        field_id = self.fields[0]
        value = datastructure.get(widget_id,'')
        LOG("path: ",INFO,value)
        ok = 1
        #a = CPSLocalFS(self, Title='tmptitlelfs', lfsbasepath=value,Description='')
        try:
            LOG("Try de LFS avec path : ",INFO,value)
            a = LocalFS('tmptitlelfs', value, None, None)
            LOG("______Fin du Try_______",INFO," ")
            
        except OSError:
            LOG("PathWidget: ", INFO, "Unknown_basepath")
            datastructure.setError(widget_id,"Unknown base path")
            ok = 0
            
        except TypeError:
            LOG("PathWidget: ", INFO, "insufficient_rights_messages")
            datastructure.setError(widget_id,"Unknown base path")
            ok = 0

        except AttributeError:
            LOG("PathWidget: ", INFO, "invalid_content")
            datastructure.setError(widget_id,"Unknown base path")
            ok = 0

        except NameError:
            LOG("PathWidget: ", INFO, "Invalid_Path")
            datastructure.setError(widget_id,"Unknown base path")
            ok = 0
            
            
        except Exception, exception:
            LOG("Uncacthed exception: ", INFO, exception.args)
            datastructure.setError(widget_id,"Uncatch exception: "+str(exception.args))
            ok = 0

        datamodel.set(field_id,value)
        return ok

    
    def _getFunction(self):
        """Return the name of the function to call."""
        raise NotImplementedError
    
    def render(self, mode, datastructure, **kw):
        """Render this widget from the datastructure or datamodel."""
        LOG("*** PathWidget ***", INFO, " Render OK")
        value = datastructure[self.getWidgetId()]
        
        if mode in ['view','edit','create']:
            # XXX TODO should use an other name than kw !
            # XXX change this everywhere
            kw = {
                  'id'  : self.getHtmlWidgetId(),
                  'name': self.getHtmlWidgetId(),
                  'value': value,
                  'size': self.display_width,
                  }
            if self.size_max:
                kw['maxlength'] = self.size_max
            return renderHtmlTag('input', **kw) + escape(value)
    


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
