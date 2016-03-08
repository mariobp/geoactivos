from django import forms
from geo import models as geo
from inventario import models as inv
from cuser.middleware import CuserMiddleware
from django_select2.forms import (
	HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
	ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
	Select2Widget
)
from django.db.utils import IntegrityError, DatabaseError, NotSupportedError


class GeoEditForm(forms.ModelForm):

	class Meta:
		model = geo.GeoActivo
		exclude = ()
		#exclude = ('nombre','zona','direccion','activo','descripcion')
	#end class
#end class

class GeoActivoForm(forms.ModelForm):

	class Meta:
		model = geo.GeoActivo
		exclude = ()
		widgets = {
			'zona':Select2Widget,
			'direccion':Select2Widget,
			'activo':Select2Widget
		}
	#end class

	def __init__(self, *args, **kwargs):
		super(GeoActivoForm, self).__init__(*args, **kwargs)
		user = CuserMiddleware.get_user()
		cuenta = inv.Cuenta.objects.filter(pk = user.pk).first()
		if self.instance.pk == None:
			if cuenta:
				self.fields['activo'].queryset = inv.Activo.objects.filter(instalado=False, activado=True, bodega=cuenta.bodega)
			else:
				self.fields['activo'].queryset = inv.Activo.objects.filter(instalado=False, activado=True)
		#end if
	#end def

	def clean(self):
		if self.instance.pk == None:
			user = CuserMiddleware.get_user()
			cuenta = inv.Cuenta.objects.filter(pk = user.pk).first()
			if cuenta:
				self.instance.creado_por = cuenta
				return super(GeoActivoForm, self).clean()
			else:
				raise forms.ValidationError("Necesita tener una cuenta para crear el Apta de Salida")
			#end def
		#end if
	#end def

	def save(self, commit=True):
		geo = super(GeoActivoForm, self).save(commit)
		activo = inv.Activo.objects.filter(id=geo.activo.id).first()
		activo.instalado = True
		activo.save()
		return geo
#end class


class NoSerialForm(forms.ModelForm):

	class Meta:
		model = geo.GeoNoSerial
		exclude = ()
	#end class

	def __init__(self, *args, **kwargs):
		super(NoSerialForm, self).__init__(*args, **kwargs)
		user = CuserMiddleware.get_user()
		cuenta = inv.Cuenta.objects.filter(pk = user.pk).first()
		if cuenta and self.fields.has_key('noserial'):
			self.fields['noserial'].queryset = inv.ActivoNoSerial.objects.filter(bodega=cuenta.bodega)
		#end if

		def clean(self):
			data = self.cleaned_data
			noserial = geo.GeoNoSerial.objects.filter(geoactivo=data['geoactivo'],noserial=data['noserial']).first()
			if noserial:
				raise forms.ValidationError("Ya tiene asignado/a una %s"%(data['noserial'].nombre))
			else:
				return data
			#end if
		#end def

		def clean_cantidad(self):
			if self.cleaned_data['cantidad']:
				cantidad = self.cleaned_data['cantidad']
				noserial = self.cleaned_data['noserial']
				if noserial:
					if noserial.cantidad - cantidad < 0:
						raise forms.ValidationError("La cantidad maxima disponible es %d"%(cantidad))
					#end if
					return cantidad
				#end if
				return forms.ValidationError("Seleccione un activo no serial")
			#end if
			return forms.ValidationError("Este campo es requerido")
		#end def

	def save(self, commit=True):
		try:
			noserial = super(NoSerialForm, self).save(commit)
			resta = inv.ActivoNoSerial.objects.filter(id=noserial.noserial.id).first()
			resta.cantidad = resta.cantidad - noserial.cantidad
			resta.save()
			return noserial
		except NotSupportedError as e:
			print "####### entro except", e
			print "#####################"
			raise forms.ValidationError(e)
		#end def
	#end def
#end class
