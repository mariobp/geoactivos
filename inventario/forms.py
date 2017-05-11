from django import forms
from inventario.models import (ActaEntrada, ActaSalida, Activo, Bodega, ActivoNoSerial,
                               SalidaNoSerial, ActaRequisicion, Cuenta, Articulo,
                               RequisicionArticulo, RequisicionNoSerial, EntradaNoSerial, ArticuloNoSerial)
from django.contrib.admin.widgets import FilteredSelectMultiple
from cuser.middleware import CuserMiddleware
from inventario import models as inventario
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from geoActivos.widgets import LinkToChangeList, LinkToChangeModel, IFrameToChangeList
from django.db.models import Q
from django_select2.forms import Select2Widget


class EntradaNoSerialForm(forms.ModelForm):

    class Meta:
        model = EntradaNoSerial
        exclude = ()
        widgets = {
            'activo': Select2Widget
        }
    # end class
# end class


class ArticuloForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArticuloForm, self).__init__(*args, **kwargs)
    # self.fields['precio'].widget = MoneyInput()
    # end def

    class Meta:
        model = Articulo
        exclude = ('activado',)
    # end class
# end class


class ArticuloNoSerialForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArticuloNoSerialForm, self).__init__(*args, **kwargs)
    # self.fields['precio'].widget = MoneyInput()
    # end def

    class Meta:
        model = ArticuloNoSerial
        exclude = ('activado',)
    # end class
# end class


class CuentaForm(UserCreationForm):
    CHOICES = (
        ('Operativo', 'Operativo'),
        ('Compras', 'Compras'),
    )
    perfil = forms.ModelChoiceField(
        queryset=Group.objects.all(), required=True, label='Perfil')

    def __init__(self, *args, **kwargs):
        super(CuentaForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            tipo = Group.objects.filter(user=self.instance).first()
            if tipo:
                self.initial['perfil'] = tipo
            # end if
        # end if
    # end def

    class Meta:
        model = Cuenta
        exclude = (
            'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions', 'password')

    # end class

    def save(self, commit=True):
        cuenta = super(CuentaForm, self).save(False)
        cuenta.is_staff = True
        cuenta.save()
        cuenta.groups.add(self.cleaned_data['perfil'])
        return cuenta
    # end def


# end class


class ActaEntradaForm(forms.ModelForm):
    activos = forms.ModelMultipleChoiceField(queryset=Activo.objects.filter(bodega=None, instalado=False),
                                             label=('Activos'), required=False,
                                             widget=FilteredSelectMultiple('Activos', False))

    def __init__(self, *args, **kwargs):
        super(ActaEntradaForm, self).__init__(*args, **kwargs)
        user = CuserMiddleware.get_user()
        cuenta = inventario.Cuenta.objects.filter(pk=user.pk).first()
        if cuenta:
            if self.fields.has_key('activos'):
                if self.instance.pk:
                    self.fields['activos'].queryset = Activo.objects.filter(instalado=False).exclude(
                        bodega=cuenta.bodega) | Activo.objects.filter(actaentrada=self.instance)
                else:
                    self.fields['activos'].queryset = Activo.objects.filter(instalado=False).exclude(
                        bodega=cuenta.bodega)
                # end if
            if self.fields.has_key('origen'):
                self.fields['origen'].queryset = Bodega.objects.exclude(
                    pk=cuenta.bodega.pk)
            # end if
        # end if
    # end def

    class Meta:
        model = ActaEntrada
        exclude = ('destino',)
        widgets = {
            'custodio': Select2Widget,
            'origen': Select2Widget,
        }
    # end class

    def clean(self):
        if self.instance.pk == None:
            user = CuserMiddleware.get_user()
            cuenta = inventario.Cuenta.objects.filter(pk=user.pk).first()
            if cuenta:
                self.instance.creado_por = cuenta
                return super(ActaEntradaForm, self).clean()
            else:
                raise forms.ValidationError(
                    "Necesita tener una cuenta para crear el Apta de Salida")
            # end def
        # end if
    # end def
# end class


class CompraActivoForm(forms.ModelForm):
    serial = forms.CharField(max_length=60)
    alias = forms.CharField(max_length=60)
    articulo = forms.ModelChoiceField(queryset=Articulo.objects)
    precio = forms.DecimalField(max_digits=19, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super(CompraActivoForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            activo = Activo.objects.filter(pk=self.instance.activo_id).first()
            self.initial = {
                'serial': activo.serial,
                'alias': activo.alias,
                'articulo': activo.articulo,
                'precio': activo.precio
            }
        # end if
    # end def

    class Meta:
        model = ActaEntrada.activos.through
        exclude = ('destino', 'origen', 'activo')
    # end class

    def save(self, commit=True):
        super(CompraActivoForm, self).save(False)
        actaentrada = self.cleaned_data['actaentrada']
        articulo = self.cleaned_data['articulo']
        serial = self.cleaned_data['serial']
        alias = self.cleaned_data['alias']
        precio = self.cleaned_data['precio']

        if self.instance.pk:
            activo = Activo.objects.filter(pk=self.instance.activo_id).update(serial=serial, alias=alias, precio=precio,
                                                                              articulo=articulo)
            return self.instance
        else:
            activo = Activo(serial=serial, alias=alias,
                            precio=precio, articulo=articulo)
            activo.save()

            actaentrada.activos.add(activo)
            activos = ActaEntrada.activos.through.objects.filter(
                activo=activo, actaentrada=actaentrada).first()
            return activos
        # end if
    # end def
# end class


class CompraForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
    # end def

    class Meta:
        model = ActaEntrada
        exclude = ('destino', 'origen', 'activos')
    # end class
# end class


class ActaSalidaForm(forms.ModelForm):
    activos = forms.ModelMultipleChoiceField(queryset=Activo.objects.all(), label=('Activos'), required=False,
                                             widget=FilteredSelectMultiple('Activos', False))

    def __init__(self, *args, **kwargs):
        super(ActaSalidaForm, self).__init__(*args, **kwargs)
        user = CuserMiddleware.get_user()
        cuenta = inventario.Cuenta.objects.filter(pk=user.pk).first()
        if cuenta:
            self.fields['activos'].queryset = Activo.objects.filter(
                Q(bodega=cuenta.bodega, instalado=False) | Q(actasalida=self.instance))
            self.fields['destino'].queryset = Bodega.objects.all(
            ).exclude(id=cuenta.bodega.id)
        # end if
    # end def

    class Meta:
        model = ActaSalida
        exclude = ('salida', 'creado_por')
        widgets = {
            'custodio': Select2Widget,
            'destino': Select2Widget,
        }
    # end class

    def clean(self):
        if self.instance.pk == None:
            user = CuserMiddleware.get_user()
            cuenta = inventario.Cuenta.objects.filter(pk=user.pk).first()
            if cuenta:
                self.instance.creado_por = cuenta
                return super(ActaSalidaForm, self).clean()
            else:
                raise forms.ValidationError(
                    "Necesita tener una cuenta para crear el Apta de Salida")
            # end if
        # end if
    # end def
# end class


class ActaRequisicionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ActaRequisicionForm, self).__init__(*args, **kwargs)
    # end def

    class Meta:
        model = ActaRequisicion
        exclude = ('bodega',)
        widgets = {
            'central': Select2Widget
        }
    # end class

    def clean(self):
        if self.instance.pk == None:
            user = CuserMiddleware.get_user()
            cuenta = inventario.Cuenta.objects.filter(pk=user.pk).first()
            if cuenta:
                self.instance.bodega = cuenta.bodega
                return super(ActaRequisicionForm, self).clean()
            else:
                raise forms.ValidationError(
                    "Necesita tener una cuenta para crear el Apta de Requisicion")
            # end if
        # end if
    # end def
# end class


class ActivoForm(forms.ModelForm):

    class Meta:
        model = Activo
        exclude = ('bodega', 'activado')
        widgets = {
            'articulo': Select2Widget,
        }
    # end class

    def clean(self):
        if self.instance.pk == None:
            user = CuserMiddleware.get_user()
            cuenta = inventario.Cuenta.objects.filter(pk=user.pk).first()
            if cuenta:
                return super(ActivoForm, self).clean()
            else:
                raise forms.ValidationError(
                    "Necesita tener una cuenta para registrar el activo")
            # end def
            # end if
            # end def


# end class

class ActivoNoSerialForm(forms.ModelForm):

    class Meta:
        model = ActivoNoSerial
        exclude = ('bodega',)

    # end class

    def clean(self):
        if self.instance.pk == None:
            user = CuserMiddleware.get_user()
            cuenta = inventario.Cuenta.objects.filter(pk=user.pk).first()
            if cuenta:
                return super(ActivoNoSerialForm, self).clean()
            else:
                raise forms.ValidationError(
                    "Necesita tener una cuenta para registrar el activo no serial")
            # end if
        # end if
    # end def
# end class


class SalidaNoSerialForm(forms.ModelForm):

    class Meta:
        model = SalidaNoSerial
        exclude = ()
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s no se pueden repetir.",
            }
        }
    # end class
# end class


class RequisicionArticuloForm(forms.ModelForm):

    class Meta:
        model = RequisicionArticulo
        exclude = ()
        widgets = {
            'articulo': Select2Widget,
        }
    # end class
# end class


class RequisicionNoForm(forms.ModelForm):

    class Meta:
        model = RequisicionNoSerial
        exclude = ()
        widgets = {
            'activo': Select2Widget,
        }
    # end class
# end class


class BodegaForm(forms.ModelForm):
    valor_total = forms.CharField(max_length=60, widget=forms.TextInput(
        attrs={'readonly': 'readonly'}), required=False)
    valor_activo = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'readonly': 'readonly'}),
                                   required=False)
    valor_activo_no_serial = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'readonly': 'readonly'}),
                                             required=False)
    activos = forms.CharField(
        max_length=160, widget=IFrameToChangeList, required=False)
    noserial = forms.CharField(
        max_length=160, widget=IFrameToChangeList, required=False, label="Activos no serial")

    def __init__(self, *args, **kwargs):
        super(BodegaForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['valor_total'] = u"$ %s" % (
                self.instance.precio_total(),)
            self.initial['valor_activo'] = u"%s" % (
                self.instance.precio_activos(),)
            self.initial['valor_activo_no_serial'] = u"%s" % (
                self.instance.precio_activos_no_serial(),)
            # self.fields['valor_total'].widget = MoneyInput()
            self.initial['activos'] = 'admin:inventario_activo'
            self.initial['noserial'] = 'admin:inventario_activonoserial'
            self.fields[
                'activos'].widget.extra = "&bodega__id__exact=" + str(self.instance.pk)
            self.fields[
                'noserial'].widget.extra = "&bodega__id__exact=" + str(self.instance.pk)
        # end if

    # end def
    class Meta:
        model = Bodega
        exclude = ()
    # end class


# end class


class BodegaStackForm(forms.ModelForm):
    capital_en_bodega = forms.CharField(
        max_length=60, label="Capital en bodega", required=False)
    irbodega = forms.CharField(
        max_length=160, required=False, label="", widget=LinkToChangeModel())
    iractivos = forms.CharField(
        max_length=160, required=False, label="", widget=LinkToChangeList())
    irnserial = forms.CharField(
        max_length=160, required=False, label="", widget=LinkToChangeList())

    def __init__(self, *args, **kwargs):
        super(BodegaStackForm, self).__init__(*args, **kwargs)
        self.fields['capital_en_bodega'].widget.attrs['disabled'] = True
        if self.instance.pk:
            self.initial[
                'capital_en_bodega'] = self.instance.bodega.capital_en_bodega()
            self.initial['irbodega'] = self.instance.bodega
            self.initial['iractivos'] = 'admin:inventario_activo'
            self.initial['irnserial'] = 'admin:inventario_activonoserial'

            self.fields['irbodega'].widget.label = "Ir a la bodega"
            self.fields['iractivos'].widget.label = "Ver los activos"
            self.fields['iractivos'].widget.extra = "?bodega__id__exact=" + \
                str(self.instance.bodega.pk)
            self.fields[
                'irnserial'].widget.label = "Var los activos no seriales"
            self.fields['irnserial'].widget.extra = "?bodega__id__exact=" + \
                str(self.instance.bodega.pk)
        # end if

    # end def

    class Meta:
        model = Bodega
        exclude = ()
    # end class

# end class
