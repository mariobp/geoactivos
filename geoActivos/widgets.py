from django.forms import widgets
from django.db.models import Model
from django.forms.utils import flatatt
from django.core.urlresolvers import reverse


class IFrame(widgets.Textarea):
    def render(self, name, value="#", attrs=None):
        if value:
            return '<iframe src="%(value)s" style="border:none" width="%(width)s" height="%(height)s" %(attrs)s></iframe>' % {
                'width': '100%',
                'height': '600',
                'value': value,
                'attrs': flatatt(attrs)
            }
        # end if
        return "No disponible"

    # end def


# end def

class IFrameToChangeList(IFrame):
    extra = ""

    def render(self, name, value="#", attrs=None):
        if value:
            value = reverse('%s_changelist' % (value,)) + "?_popup=1" + self.extra
            return super(IFrameToChangeList, self).render(name, value, attrs)
        # end if
        return "No disponible"

    # end def


# end def

class Link(widgets.Textarea):
    def __init__(self, label="", attrs=None):
        self.label = label
        super(Link, self).__init__(attrs)

    # end def

    def render(self, name, value="#", attrs=None):
        return '<a href="%(value)s" %(attrs)s>%(label)s</a>' % {
            'value': value,
            'label': self.label,
            'attrs': flatatt(attrs)
        }

    # end def


# end class

class LinkToChangeList(Link):
    extra = ""

    def render(self, name, value="#", attrs=None):
        if value:
            value = reverse('%s_changelist' % (value,)) + self.extra
            return super(LinkToChangeList, self).render(name, value, attrs)
        # end if
        return "No disponible"

    # end def


# end class

class LinkToChangeModel(Link):
    def render(self, name, value="#", attrs=None):
        if isinstance(value, Model):
            import importlib
            mdl = type(value).__module__
            mdl = importlib.import_module(mdl)
            app = str(mdl.__package__)
            cls = type(value).__name__.lower()
            value = reverse('admin:%s_%s_change' % (app, cls), args=(value.pk,))
        # end if
        return super(LinkToChangeModel, self).render(name, value, attrs)

    # end def

# end class
