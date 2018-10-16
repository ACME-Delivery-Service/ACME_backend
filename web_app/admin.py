from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Parcel)
admin.site.register(IncomingOrder)
admin.site.register(Contact)
admin.site.register(Warehouse)
admin.site.register(DispatchStatus)
admin.site.register(TransportationVector)
admin.site.register(TransportationRoutes)
admin.site.register(DeliveryOperator)
admin.site.register(TransportationCompany)
admin.site.register(DispatchOrder)