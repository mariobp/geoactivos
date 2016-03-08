# encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from django.db.models import Count, F
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from cuser.middleware import CuserMiddleware
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.db.models import Q, Sum, F, DecimalField
from inventario.widgets import MoneyInput

class Proveedor(models.Model):
	nombre = models.CharField(max_length=45)
	logo = models.ImageField(upload_to='logo', null=True, blank=True)
	fecha = models.DateField(auto_now=True)

	def __unicode__(self):
		return self.nombre

	# end def

	class Meta:
		verbose_name = "Proveedor"
		verbose_name_plural = "Provedores"

	# end class

	def thumbnail(self):
		if self.logo:
			imagen = self.logo
		else:
			imagen = 'No-foto.png'
		# end if
		return '<img src="/media/%s" width=50px heigth=50px/>' % (imagen)

	# end def
	thumbnail.allow_tags = True


# end class

class Fabricante(models.Model):
	nombre = models.CharField(max_length=45)
	logo = models.ImageField(upload_to='logo', null=True, blank=True)
	fecha = models.DateField(auto_now=True)

	def __unicode__(self):
		return self.nombre

	# end def
	def thumbnail(self):
		if self.logo:
			imagen = self.logo
		else:
			imagen = 'No-foto.png'
		# end if
		return '<img src="/media/%s" width=50px heigth=50px/>' % (imagen)

	# end def

	thumbnail.allow_tags = True


# end class

class Articulo(models.Model):
	nombre = models.CharField(max_length=45)
	descripcion = models.TextField(max_length=500)  # NO
	fabricante = models.ForeignKey(Fabricante)
	cantidad_minima_en_bodega = models.IntegerField()
	cantidad_minima_de_compra = models.IntegerField()  # ROQ
	fecha_creacion = models.DateTimeField(auto_now=True)
	imagen = models.ImageField(upload_to='articulos', null=True, blank=True)  # NO
	tiempo_entrega = models.IntegerField('Tiempo de entrega(Dias)')
	activado = models.BooleanField(default=True)  # NO True
	precio = models.DecimalField(max_digits=19, decimal_places=2)

	def __unicode__(self):
		return self.nombre

	# end def

	def precio_(self):
		vals = str(self.precio).split('.')
		money = MoneyInput()
		value = money.intToStringWithCommas(int(vals[0])).replace(',', '.') + ',' + vals[1]
		return "$" + value

	# end def

	class Meta:
		verbose_name = "Articulo serial"
		verbose_name_plural = "Articulos seriales"

	# end class

	def thumbnail(self):
		if self.imagen:
			imagen = self.imagen
		else:
			imagen = 'No-foto.png'
		# end if
		return '<img src="/media/%s" width=50px heigth=50px/>' % (imagen)

	# end def

	thumbnail.allow_tags = True


# end Class


class Bodega(models.Model):
	identi = models.CharField('Identificación', max_length=45)
	nombre = models.CharField(max_length=45)
	direccion = models.CharField(max_length=100)
	telefono = models.CharField(max_length=10)

	@staticmethod
	def bodega_actual():
		user = CuserMiddleware.get_user()
		cuenta = Cuenta.objects.filter(pk=user.pk).first()
		if cuenta:
			return cuenta.bodega
		# end if
		return None

	# end def

	def precio_activos(self):
		activos = Activo.objects.filter(bodega=self).aggregate(total=Sum('articulo__precio'))
		if activos['total']:
			total = activos['total']
			vals = str(total).split('.')
			money = MoneyInput()
			value = money.intToStringWithCommas(int(vals[0])).replace(',', '.') + ',' + vals[1]
			return u"$ %s" % value
		# end if
		else:
			return u"$ %s" % 0
		# end if

	# end def

	def precio_activos_no_serial(self):
		agg = Sum(F('articulo__precio') * F('cantidad'))
		agg.output_field = DecimalField(max_digits=19, decimal_places=2)
		nserial = ActivoNoSerial.objects.filter(bodega=self).aggregate(total=agg)
		if nserial['total']:
			total = nserial['total']
			vals = str(total).split('.')
			money = MoneyInput()
			value = money.intToStringWithCommas(int(vals[0])).replace(',', '.') + ',' + vals[1]
			return u"$ %s" % value
		else:
			return u"$ %d" % 0
		# end if

	# end def

	def precio_total(self):
		activos = Activo.objects.filter(bodega=self).aggregate(total=Sum('articulo__precio'))
		agg = Sum(F('articulo__precio') * F('cantidad'))

		agg.output_field = DecimalField(max_digits=19, decimal_places=2)
		nserial = ActivoNoSerial.objects.filter(bodega=self).aggregate(total=agg)

		if activos['total']:
			total = activos['total']
		else:
			total = 0
		# end if
		if nserial['total']:
			total = total + nserial['total']
		# end if
		if total == 0:
			return total
		else:
			vals = str(total).split('.')
			money = MoneyInput()
			value = money.intToStringWithCommas(int(vals[0])).replace(',', '.') + ',' + vals[1]
			return value
		# end if

	# end def

	def capital_en_bodega(self):
		return u"$ %s" % (self.precio_total(),)

	# end def

	def __unicode__(self):
		return self.nombre

	# end def


# end calss



class Cuenta(User):
	bodega = models.ForeignKey(Bodega)

	class Meta:
		verbose_name = 'Cuenta'
		verbose_name_plural = "Cuentas"
	# end class


# end class

class Central(models.Model):
	bodega = models.ForeignKey(Bodega)

	class Meta:
		verbose_name = 'Central'
		verbose_name_plural = "Centrales"

	# end class

	def __unicode__(self):
		return u"Central %s" % (self.bodega.nombre,)

	# end def


# end class


class ArticuloNoSerial(models.Model):
	nombre = models.CharField(max_length=45)
	descripcion = models.TextField(max_length=500)  # NO
	fabricante = models.ForeignKey(Fabricante)
	cantidad_minima_en_bodega = models.IntegerField()
	cantidad_minima_de_compra = models.IntegerField()  # ROQ
	activado = models.BooleanField(default=True)  # NO True
	imagen = models.ImageField(upload_to='articulos', null=True, blank=True)  # NO
	unidad = models.CharField(max_length=10)
	precio = models.DecimalField(max_digits=19, decimal_places=2)
	fecha_creacion = models.DateTimeField(auto_now=True)
	tiempo_entrega = models.IntegerField('Tiempo de entrega(Dias)')

	class Meta:
		verbose_name = "Articulo no serial"
		verbose_name_plural = "Aticulos no seriales"

	# end class

	def __unicode__(self):
		return self.nombre

	# end def

	def thumbnail(self):
		if self.imagen:
			imagen = self.imagen
		else:
			imagen = 'No-foto.png'
		# end if
		return '<img src="/media/%s" width=50px heigth=50px/>' % (imagen)

	# end def

	thumbnail.allow_tags = True


# end class

class ActivoNoSerial(models.Model):
	articulo = models.ForeignKey(ArticuloNoSerial)
	cantidad = models.IntegerField()
	bodega = models.ForeignKey(Bodega)

	class Meta:
		verbose_name = "Activo no serial"
		verbose_name_plural = "Activo no seriales"

	# end class

	def __unicode__(self):
		return self.articulo.nombre

	# end def

	def save(self, *args, **kwargs):
		user = CuserMiddleware.get_user()
		cuenta = Cuenta.objects.filter(pk=user.pk).first()
		if cuenta:
			self.bodega = cuenta.bodega
			super(ActivoNoSerial, self).save(*args, **kwargs)
		# end if
		# end if
		# end def


# end def


class LogNoSerial(models.Model):
	activo = models.ForeignKey(ActivoNoSerial)
	fecha = models.DateTimeField(auto_now_add=True)
	cantidad = models.IntegerField()
	bodega = models.ForeignKey(Bodega)

	class Meta:
		verbose_name = 'Log no serial'
		verbose_name_plural = 'Logs no seriales'
	# end class


# end class

class LogArticulo(models.Model):
	articulo = models.ForeignKey(Articulo)
	fecha = models.DateTimeField(auto_now=True)
	cantidad = models.IntegerField()
	bodega = models.ForeignKey(Bodega, null=True)

	class Meta:
		verbose_name = 'Log de articulo'
		verbose_name_plural = "Logs de articulos"
	# end class


# end class


class TipoActivo(models.Model):
	nombre = models.CharField(max_length=200)
	unidad = models.CharField(max_length=200)
	marker = models.ImageField(upload_to='marker', verbose_name="Marcador", blank=True, null=True)
	marker_2 = models.ImageField(upload_to='marker2', verbose_name="Marcador seleccionado", blank=True, null=True)

	class Meta:
		verbose_name = 'Tipo de Activo'
		verbose_name_plural = "Tipos de Activos"

	# end class

	def __unicode__(self):
		return "%s" % (self.nombre,)

	# end def

	def thumbnail(self):
		if self.marker:
			imagen = self.marker
		else:
			imagen = 'No-foto.png'
		# end if
		return '<img src="/media/%s" width=50px heigth=50px/>' % (imagen)

	# end def

	def thumbnail2(self):
		if self.marker_2:
			imagen = self.marker_2
		else:
			imagen = 'No-foto.png'
		# end if
		return '<img src="/media/%s" width=50px heigth=50px/>' % (imagen)

	# end def

	thumbnail.allow_tags = True
	thumbnail2.allow_tags = True


# end class


class Activo(models.Model):
	articulo = models.ForeignKey(Articulo)
	bodega = models.ForeignKey(Bodega)
	serial = models.CharField(max_length=60)
	activado = models.BooleanField(default=True)
	instalado = models.BooleanField(default=False)
	tipo = models.ForeignKey(TipoActivo)

	def __unicode__(self):
		if self.bodega:
			bodega = self.bodega.nombre
		else:
			bodega = "Fuera de Bodega"
		# end if
		return u'%s - %s' % (unicode(self.articulo), bodega)

	# end def

	class Meta:
		verbose_name = "Activo Serial"
		verbose_name_plural = "Activos Seriales"

	# end class


	def save(self, *args, **kwargs):
		user = CuserMiddleware.get_user()
		cuenta = Cuenta.objects.filter(pk=user.pk).first()
		if cuenta:
			self.bodega = cuenta.bodega
			super(Activo, self).save(*args, **kwargs)
		# end if
		# end if
		# end def


# end class

class Custodio(models.Model):
	identi = models.CharField('Identificación', max_length=45)
	nombre = models.CharField(max_length=45)
	direccion = models.CharField(max_length=100)
	telefono = models.CharField(max_length=10)
	correo = models.CharField(max_length=45)

	def __unicode__(self):
		return self.nombre

	# end def


# end class

class ActaRequisicion(models.Model):
	central = models.ForeignKey(Central)
	bodega = models.ForeignKey(Bodega)
	fecha = models.DateTimeField(auto_now=True)
	descripcion = models.TextField(max_length=500)

	class Meta:
		verbose_name = 'Acta de requisición'
		verbose_name_plural = "Actas de requisición"
	# end class


# end class

class RequisicionArticulo(models.Model):
	acta = models.ForeignKey(ActaRequisicion)
	articulo = models.ForeignKey(Articulo)
	cantidad = models.IntegerField()

	class Meta:
		verbose_name = 'Activo'
		verbose_name_plural = 'Activos'
	# end class


# end class

class RequisicionNoSerial(models.Model):
	acta = models.ForeignKey(ActaRequisicion)
	activo = models.ForeignKey(ArticuloNoSerial)
	cantidad = models.IntegerField()

	class Meta:
		verbose_name = 'Activo no serial'
		verbose_name_plural = "Activos no seriales"
	# end class


# end class


class ActaSalida(models.Model):
	activos = models.ManyToManyField(Activo, blank=True)
	fecha = models.DateTimeField(auto_now=True)
	custodio = models.ForeignKey(Custodio)
	salida = models.ForeignKey(Bodega, related_name='salida')
	destino = models.ForeignKey(Bodega, null=True, related_name='destino')
	archivo = models.FileField('Acta', upload_to='actas_salida', null=True, blank=True)
	descripcion = models.TextField(max_length=500)
	creado_por = models.ForeignKey(Cuenta)

	class Meta:
		verbose_name = 'Acta de salida'
		verbose_name_plural = 'Actas de salidas'

	# end class

	def __unicode__(self):
		return 'Acta Salida: %s' % str(self.fecha)

	# end def

	def archivo_(self):
		if self.archivo:
			return "<a href='/media/%s'>Descargar</a>" % (self.archivo,)
		# end if
		return "Sin archivo"

	# end def

	archivo_.allow_tags = True

	def save(self, *args, **kwargs):
		user = CuserMiddleware.get_user()
		cuenta = Cuenta.objects.filter(pk=user.pk).first()
		if cuenta:
			self.creado_por = cuenta
			self.salida = cuenta.bodega
			super(ActaSalida, self).save(*args, **kwargs)
			self.activos.update(bodega=None)
		# end if
		# end def


# end class

@receiver(m2m_changed, sender=ActaSalida.activos.through)
def actaSalida_slot(sender, instance, action, **kwargs):
	"""
	Automaticamente guarda cuando el activo es agregado al acta de salida
	"""
	if action == 'post_add':
		instance.save()
		articulos = Articulo.objects.filter(activo__actasalida=instance).distinct('id')
		for a in articulos:
			cant = Activo.objects.filter(bodega=instance.salida, articulo=a).count()
			LogArticulo(articulo=a, cantidad=cant, bodega=instance.salida).save()
		# end for
		for activo in instance.activos.all():
			TrazabilidadActivo(activo=activo, mensage='salida de bodega').save()
		# end for
		# end if


# end def

class SalidaNoSerial(models.Model):
	acta = models.ForeignKey(ActaSalida)
	activo = models.ForeignKey(ActivoNoSerial)
	cantidad = models.IntegerField()
	fecha = models.DateField(auto_now_add=True)

	class Meta:
		verbose_name = 'Salida no serial'
		verbose_name_plural = 'Salidas no seriales'

	# end class

	def save(self, *args, **kwargs):
		salida = super(SalidaNoSerial, self).save(*args, **kwargs)
		ActivoNoSerial.objects.filter(pk=self.activo.pk).update(cantidad=F('cantidad') - self.cantidad)
		activo = ActivoNoSerial.objects.filter(pk=self.activo.pk).first()
		LogNoSerial(activo=activo, cantidad=activo.cantidad, bodega=activo.bodega).save()
		return salida

	# end def


# end class


class ActaEntrada(models.Model):
	activos = models.ManyToManyField(Activo, blank=True)
	custodio = models.ForeignKey(Custodio)
	fecha = models.DateTimeField(auto_now_add=True)
	origen = models.ForeignKey(Bodega, null=True, blank=True, related_name='origen_')
	destino = models.ForeignKey(Bodega, related_name='destino_')
	imagen = models.ImageField(upload_to='actas_entrada', null=True, blank=True)
	descripcion = models.TextField(max_length=500)

	class Meta:
		verbose_name = 'Acta de entrada'
		verbose_name_plural = 'Actas de entradas'

	# end class

	def thumbnail(self):
		if self.imagen:
			imagen = self.imagen
		else:
			imagen = 'No-foto.png'
		# end if
		return '<img src="/media/%s" width=50px heigth=50px/>' % (imagen)

	# end def

	thumbnail.allow_tags = True

	def __unicode__(self):
		return 'Acta Entrada: %s' % str(self.fecha)

	# end def

	def save(self, *args, **kwargs):
		user = CuserMiddleware.get_user()
		cuenta = Cuenta.objects.filter(pk=user.pk).first()
		if cuenta:
			self.destino = cuenta.bodega
			acta = super(ActaEntrada, self).save(*args, **kwargs)
			self.activos.update(bodega=self.destino)
			return acta
		# end if
		# end def


# end class

@receiver(m2m_changed, sender=ActaEntrada.activos.through)
def actaEntrada_slot(sender, instance, action, **kwargs):
	"""
	Automaticamente guarda cuando el activo es agregado al acta de salida
	"""
	if action == 'post_add':
		instance.save()
		articulos = Articulo.objects.filter(activo__actaentrada=instance).distinct('id')
		compra = Compra.objects.filter(pk=instance.pk).first()
		for a in articulos:
			cant = Activo.objects.filter(articulo=a).count()
			LogArticulo(articulo=a, cantidad=cant, bodega=instance.destino).save()
		# end for
		for activo in instance.activos.all():
			TrazabilidadActivo(activo=activo, bodega=instance.destino, mensage='entrada de bodega').save()
		# end for
		# end if


# end def

class EntradaNoSerial(models.Model):
	acta = models.ForeignKey(ActaEntrada)
	activo = models.ForeignKey(ActivoNoSerial)
	cantidad = models.IntegerField()

	class Meta:
		verbose_name = 'Activo no serial'
		verbose_name_plural = 'Activos no seriales'

	# end class

	def save(self, *args, **kwargs):
		super(EntradaNoSerial, self).save(*args, **kwargs)
		self.activo.cantidad = self.activo.cantidad + self.cantidad
		self.activo.save()
		LogNoSerial(activo=self.activo, cantidad=self.activo.cantidad, bodega=self.activo.bodega).save()
		compra = Compra.objects.filter(pk=self.acta.pk).first()

	# end def


# end class

class Compra(ActaEntrada):
	creado_por = models.ForeignKey(Cuenta)

	def save(self, *args, **kwargs):
		user = CuserMiddleware.get_user()
		cuenta = Cuenta.objects.filter(pk=user.pk).filterst()
		if cuenta:
			self.creado_por = cuenta
			super(Compra, self).save(*args, **kwargs)
		# end if
		# ens def


# end class

class TrazabilidadActivo(models.Model):
	activo = models.ForeignKey(Activo)
	fecha = models.DateTimeField(auto_now_add=True)
	bodega = models.ForeignKey(Bodega, null=True)
	mensage = models.CharField("Mensaje", max_length=150)

# end class
