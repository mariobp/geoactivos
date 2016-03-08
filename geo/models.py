# encoding:utf-8
from __future__ import unicode_literals

from django.db import models
from inventario import models as inventario


# Create your models here.

class Zona(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nombre

    # end def


# end class

class Direccion(models.Model):
    nombre = models.CharField(max_length=50)
    zona = models.ForeignKey(Zona)

    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'

    # end class

    def __unicode__(self):
        return self.nombre

    # end def


# end class

class GeoActivo(models.Model):
    nombre = models.CharField(max_length=50)
    zona = models.ForeignKey(Zona)
    direccion = models.ForeignKey(Direccion, verbose_name="Dirección")
    activo = models.ForeignKey(inventario.Activo)
    descripcion = models.TextField("Descripción", max_length=400)
    lon = models.FloatField("Longitud", blank=True, null=True)
    lat = models.FloatField("Latitud", blank=True, null=True)

    def __unicode__(self):
        return self.nombre

    # end def


# end class

class GeoNoSerial(models.Model):
    geoactivo = models.ForeignKey(GeoActivo)
    noserial = models.ForeignKey(inventario.ActivoNoSerial, verbose_name="Activo no serial")
    cantidad = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Geo activo no-serial"
        verbose_name_plural = "Geo activos no-seriales"
        unique_together = ('geoactivo', 'noserial')

    # end class

    def __unicode__(self):
        return self.geoactivo.nombre
        # end def
# end class
