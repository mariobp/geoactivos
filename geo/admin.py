from django.contrib import admin
from geo import models as geo
from geo import forms as form


# Register your models here.

class DireAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'zona')
    list_filter = ('zona',)
    search_fields = ('nombre',)


# end  class

class NoSerialStack(admin.StackedInline):
    model = geo.GeoNoSerial
    form = form.NoSerialForm
    extra = 1

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('noserial', 'cantidad')
        return self.readonly_fields

    # end def


# end class

class GeoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'zona', 'direccion', 'activo', 'descripcion', 'lon', 'lat')
    list_filter = ('zona', 'direccion')
    search_fields = ('nombre', 'descripcion')
    form = form.GeoActivoForm
    inlines = [NoSerialStack, ]

    class Media:
        js = ('geo/js/mapa.js', 'https://maps.googleapis.com/maps/api/js?key=AIzaSyBKW2rPTyey18du2v87J8WYMMlICYhYLg8')
        css = {
            "all": ('geo/css/style.css',)
        }

    # end class
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('nombre', 'zona', 'direccion', 'activo', 'descripcion', 'lon', 'lat')
        return self.readonly_fields

    # end def


# end class

admin.site.register(geo.Direccion, DireAdmin)
admin.site.register(geo.Zona)
admin.site.register(geo.GeoActivo, GeoAdmin)
