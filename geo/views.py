from supra import views as supra

import models as geo
from geo.forms import GeoEditForm

# Create your views here.

supra.SupraConf.ACCECC_CONTROL["allow"] = True


class ListMap(supra.SupraListView):
    model = geo.GeoActivo
    list_display = ['lon', 'lat', 'nombre', 'id', 'descripcion']
    search_fields = ['nombre', 'activo__nombre']

    def get_queryset(self):
        queryset = super(ListMap, self).get_queryset()
        return queryset.filter(lat__isnull=False, lon__isnull=False)


# end class

class ListNull(supra.SupraListView):
    model = geo.GeoActivo
    list_display = ['lon', 'lat', 'nombre', 'id']
    search_fields = ['nombre', 'activo__nombre']

    def get_queryset(self):
        queryset = super(ListNull, self).get_queryset()
        return queryset.filter(lat__isnull=True, lon__isnull=True)


# end class

class GeoForm(supra.SupraFormView):
    model = geo.GeoActivo
    form_class = GeoEditForm
    template_name = 'geo/form.html'

# body = True

# end class
