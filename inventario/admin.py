# encoding:utf-8
from django.contrib import admin
from inventario.forms import (BodegaForm, ActaEntradaForm,
                              ActivoForm, ActaSalidaForm, ActaRequisicionForm, ActivoNoSerialForm, SalidaNoSerialForm,
                              CuentaForm, CompraForm, CompraActivoForm, ArticuloForm, RequisicionArticuloForm,
                              RequisicionNoForm, EntradaNoSerialForm, ArticuloNoSerialForm)
from inventario import models as inventario
from import_export.admin import ExportMixin
from import_export import resources


class ArticuloResource(resources.ModelResource):

    class Meta:
        model = inventario.Articulo
        fields = (
            'nombre', 'fabricante__nombre', 'cantidad_minima_en_bodega', 'cantidad_minima_de_compra', 'fecha_creacion',
            'tiempo_entrega')
        export_oder = (
            'nombre', 'fabricante__nombre', 'cantidad_minima_en_bodega', 'cantidad_minima_de_compra', 'fecha_creacion',
            'tiempo_entrega')
    # end class


# end class

class ArticuloAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        'nombre', 'thumbnail', 'fabricante', 'cantidad_minima_en_bodega', 'cantidad_minima_de_compra', 'fecha_creacion',
        'tiempo_entrega', 'precio_')
    search_fields = ('nombre', 'descripcion', 'fabricante')
    list_filter = ('activado', 'fabricante')
    resource_class = ArticuloResource
    form = ArticuloForm


# end class

class CuentaStaked(admin.StackedInline):
    model = inventario.Cuenta
    fields = ['username', 'first_name', 'last_name', 'email']
    readonly_fields = ('username', 'first_name', 'last_name', 'email')
    form = CuentaForm
    extra = 0
    suit_classes = 'suit-tab suit-tab-cuenta'


# end class

class BodegaResource(resources.ModelResource):

    class Meta:
        model = inventario.Bodega
        fields = ('nombre', 'identi', 'direccion', 'telefono')
        export_order = ('nombre', 'identi', 'direccion', 'telefono')
    # end class


# end class

class BodegaAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        'nombre', 'identi', 'direccion', 'telefono', 'precio_activos', 'precio_activos_no_serial', 'capital_en_bodega')
    search_fields = ('nombre', 'identi', 'direccion', 'telefono')
    form = BodegaForm
    inlines = (CuentaStaked,)
    fieldsets = [(None, {'classes': ('suit-tab', 'suit-tab-bodega'),
                         'fields': ['identi', 'nombre', 'direccion', 'telefono', 'valor_activo',
                                    'valor_activo_no_serial', 'valor_total', 'activos', 'noserial']})]
    suit_form_tabs = (('bodega', '1. Bodega'), ('cuenta', '2. Encargados'))
    resource_class = BodegaResource


# end class

class CentralAdmin(admin.ModelAdmin):
    list_display = ('bodega',)
    list_filter = ('bodega',)


# raw_id_fields = ('bodega',)


# end class


class ActivoNoSerialAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('articulo', 'bodega', 'cantidad')
    list_filter = ('articulo', 'bodega')
    form = ActivoNoSerialForm

    # resource_class = ArticuloNoResource

    def get_queryset(self, request):
        qs = super(ActivoNoSerialAdmin, self).get_queryset(request)
        cuenta = inventario.Cuenta.objects.filter(id=request.user.id).first()
        if cuenta:
            return qs.filter(bodega=cuenta.bodega)
        return qs

        # end if
    # end def


# end class

class ArticuloNoResource(resources.ModelResource):

    class Meta:
        model = inventario.ArticuloNoSerial
        fields = ('nombre', 'fabricante__nombre', 'unidad', 'cantidad_minima_en_bodega', 'cantidad_minima_de_compra',
                  'fecha_creacion', 'precio', 'tiempo_entrega')
        export_order = (
            'nombre', 'fabricante__nombre', 'unidad', 'cantidad_minima_en_bodega', 'cantidad_minima_de_compra',
            'fecha_creacion', 'precio', 'tiempo_entrega', 'activado')
    # end class


# end class


class ArticuloNoSerialAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        'nombre', 'thumbnail', 'fabricante', 'unidad', 'cantidad_minima_en_bodega', 'cantidad_minima_de_compra',
        'fecha_creacion', 'precio', 'tiempo_entrega', 'activado')
    search_fields = ('nombre', 'descripcion', 'fabricante')
    list_filter = ('fabricante',)
    form = ArticuloNoSerialForm
    resource_class = ArticuloNoResource


# end class

class LogNoSerialAdmin(admin.ModelAdmin):
    list_display = ('activo', 'fecha', 'cantidad')
    search_fields = ('activo__nombre',)
    list_filter = ('activo',)


# end class

class LogArticuloAdmin(admin.ModelAdmin):
    list_display = ('articulo', 'bodega', 'fecha', 'cantidad')
    search_fields = ('articulo__nombre',)
    list_filter = ('articulo',)


# end class

class TrazabilidadAdmin(admin.StackedInline):
    model = inventario.TrazabilidadActivo
    suit_classes = 'suit-tab suit-tab-trazabilidad'
    extra = 0
    readonly_fields = ('fecha', 'bodega', 'mensage')


# end class

class ActivoResource(resources.ModelResource):

    class Meta:
        model = inventario.Activo
        fields = ('articulo__nombre', 'tipo__nombre', 'bodega__nombre',
                  'serial', 'precio', 'activado', 'instalado')
        export_order = (
            'articulo__nombre', 'tipo__nombre', 'bodega__nombre', 'serial', 'precio', 'activado', 'instalado')
    # end class


# end class

class ActivoAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('articulo', 'tipo', 'bodega',
                    'serial', 'activado', 'instalado')
    search_fields = ('articulo__nombre', 'bodega__nombre')
    list_filter = ('articulo', 'bodega', 'tipo')
    inlines = (TrazabilidadAdmin,)
    form = ActivoForm
    fieldsets = [(None, {'classes': (
        'suit-tab', 'suit-tab-activo'), 'fields': ['articulo', 'tipo', 'serial']})]
    suit_form_tabs = (('activo', '1.Activo'), ('trazabilidad', 'Trazabilidad'))
    resource_class = ActivoResource

    def get_queryset(self, request):
        qs = super(ActivoAdmin, self).get_queryset(request)
        cuenta = inventario.Cuenta.objects.filter(id=request.user.id).first()
        if cuenta:
            return qs.filter(bodega=cuenta.bodega)
        return qs

        # end if
    # end def


# end class

class CustodioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'correo', 'identi')
    search_fields = ('nombre', 'correo', 'direccion')


# end class

class RequesicionNoSerialStaked(admin.StackedInline):
    model = inventario.RequisicionNoSerial
    form = RequisicionNoForm
    suit_classes = 'suit-tab suit-tab-requesicionnoserial'


# end class

class RequisionArticuloStaked(admin.StackedInline):
    model = inventario.RequisicionArticulo
    form = RequisicionArticuloForm
    suit_classes = 'suit-tab suit-tab-requesicionarticulo'


# end class

class ActaRequisionAdmin(admin.ModelAdmin):
    list_display = ('central', 'bodega', 'fecha', 'descripcion')
    list_filter = ('central', 'bodega')
    search_fields = ('bodega__nombre', 'central__bodega__nombre')
    # raw_id_fields = ('central','bodega')
    form = ActaRequisicionForm
    inlines = (RequisionArticuloStaked, RequesicionNoSerialStaked)
    fieldsets = [(None, {'classes': (
        'suit-tab', 'suit-tab-actarequisicion'), 'fields': ['central', 'descripcion']})]
    suit_form_tabs = (('actarequisicion', '1.Acta de requesición'), ('requesicionarticulo', '2.Activos'),
                      ('requesicionnoserial', '3.Activos no serial'))


# end class

class RequisionArticuloAdmin(admin.ModelAdmin):
    list_display = ('acta', 'articulo', 'cantidad')
    list_filter = ('acta', 'articulo')


# end class

class RequisionNoSerialAdmin(admin.ModelAdmin):
    list_display = ('acta', 'activo', 'cantidad')
    list_filter = ('acta', 'activo')

    class Media:
        js = ('inventario/js/jquery.form.min.js',
              'inventario/js/notificacion.js')
    # end class


# end class

class SalidaNoSerialStaked(admin.StackedInline):
    model = inventario.SalidaNoSerial
    form = SalidaNoSerialForm
    suit_classes = 'suit-tab suit-tab-salidanoserial'


# end class

class ActaSalidaResource(resources.ModelResource):

    class Meta:
        model = inventario.ActaSalida
        fields = ('custodio__nombre', 'salida__nombre',
                  'destino__nombre', 'creado_por', 'fecha', 'descripcion')
        export_order = ('custodio__nombre', 'salida__nombre',
                        'destino__nombre', 'creado_por', 'fecha', 'descripcion')
    # end class


# end class

class ActaSalidaAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('custodio', 'salida', 'destino',
                    'creado_por', 'fecha', 'descripcion', 'archivo_')
    list_filter = ('custodio', 'salida', 'destino', 'creado_por')
    search_fields = ('custodio__nombre', 'salida__nombre',
                     'destino__nombre', 'creado_por')
    inlines = (SalidaNoSerialStaked,)
    # raw_id_fields = ('custodio','destino')
    form = ActaSalidaForm
    fieldsets = [(None, {'classes': ('suit-tab', 'suit-tab-actasalida'),
                         'fields': ['custodio', 'destino', 'activos', 'descripcion', 'archivo']})]
    suit_form_tabs = (('actasalida', '1.Acta Salida'),
                      ('salidanoserial', '2.Salida no serial'))
    resource_class = ActaSalidaResource


# end class


class SalidaNoSerialAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('acta', 'activo', 'cantidad')
    list_filter = ('acta', 'activo')
    form = SalidaNoSerialForm

    class Media:
        js = ('inventario/js/jquery.form.min.js',
              'inventario/js/notificacion.js')
    # end class


# end class

class EntradaNoSerialStacked(admin.StackedInline):
    model = inventario.EntradaNoSerial
    form = EntradaNoSerialForm
    suit_classes = 'suit-tab suit-tab-entradanoserial'


# end class

class ActaEntradaResource(resources.ModelResource):

    class Meta:
        model = inventario.ActaEntrada
        fields = ('custodio__nombre', 'origen__nombre',
                  'destino__nombre', 'fecha')
        export_order = ('custodio__nombre', 'origen__nombre',
                        'destino__nombre', 'fecha')
    # end class


# end class

class ActaEntradaAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('custodio', 'thumbnail', 'origen', 'destino', 'fecha')
    list_filter = ('custodio', 'origen', 'destino')
    search_fields = ('custodio__nombre', 'origen__nombre')
    filter_horizontal = ('activos',)
    # raw_id_fields = ('custodio','origen')
    inlines = (EntradaNoSerialStacked,)
    form = ActaEntradaForm
    fieldsets = [(None, {'classes': ('suit-tab', 'suit-tab-actaentrada'),
                         'fields': ['custodio', 'origen', 'activos', 'descripcion', 'imagen']})]
    suit_form_tabs = (('actaentrada', '1.Acta Entrada'),
                      ('entradanoserial', '3.Activos no serial'))
    resource_class = ActaEntradaResource


# end class


class ActivoInline(admin.StackedInline):
    suit_classes = 'suit-tab suit-tab-activo'
    model = inventario.ActaEntrada.activos.through
    form = CompraActivoForm


# end class

class CompraAdmin(admin.ModelAdmin):
    list_display = ('custodio', 'thumbnail', 'destino', 'fecha')
    list_filter = ('custodio', 'destino')
    search_fields = ('custodio__nombre', 'origen__nombre')
    filter_horizontal = ('activos',)
    # raw_id_fields = ('custodio','origen')
    inlines = (EntradaNoSerialStacked, ActivoInline)
    form = CompraForm
    fieldsets = [
        (None, {'classes': ('suit-tab', 'suit-tab-actaentrada'), 'fields': ['custodio', 'descripcion', 'imagen']})]
    suit_form_tabs = (
        ('actaentrada', '1.Acta Entrada'), ('activo', '2.Activos'), ('entradanoserial', '3.Activos no serial'))


# end class


class FabricanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'thumbnail', 'fecha')
    search_fields = ('nombre',)


# end class


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'thumbnail', 'fecha')
    search_fields = ('nombre',)


# end class

class CuentaResource(resources.ModelResource):

    class Meta:
        model = inventario.Cuenta
        fields = ('username', 'first_name', 'last_name',
                  'email', 'date_joined', 'last_login')
        export_order = ('username', 'first_name', 'last_name',
                        'email', 'date_joined', 'last_login')
    # end class


# end class

class CuentaAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name',
                    'bodega', 'email', 'date_joined', 'last_login')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('bodega',)
    form = CuentaForm
    resource_class = CuentaResource


# end class

class TipoActivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'unidad', 'marker',
                    'marker_2', 'thumbnail', 'thumbnail2')
    list_editable = ('marker', 'marker_2')
    search_fields = ('nombre', 'unidad__nombre')


# end class

admin.site.register(inventario.Fabricante, FabricanteAdmin)
admin.site.register(inventario.Proveedor, ProveedorAdmin)
admin.site.register(inventario.Articulo, ArticuloAdmin)
admin.site.register(inventario.Bodega, BodegaAdmin)
admin.site.register(inventario.Central, CentralAdmin)
admin.site.register(inventario.ArticuloNoSerial, ArticuloNoSerialAdmin)
admin.site.register(inventario.ActivoNoSerial, ActivoNoSerialAdmin)
admin.site.register(inventario.LogNoSerial, LogNoSerialAdmin)
admin.site.register(inventario.LogArticulo, LogArticuloAdmin)
admin.site.register(inventario.Activo, ActivoAdmin)
admin.site.register(inventario.Custodio, CustodioAdmin)
admin.site.register(inventario.ActaRequisicion, ActaRequisionAdmin)
admin.site.register(inventario.Cuenta, CuentaAdmin)
admin.site.register(inventario.ActaSalida, ActaSalidaAdmin)
admin.site.register(inventario.ActaEntrada, ActaEntradaAdmin)
admin.site.register(inventario.TipoActivo, TipoActivoAdmin)
