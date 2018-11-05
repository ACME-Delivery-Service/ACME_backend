from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Contact)
admin.site.register(AcmeCustomer)

admin.site.register(Location)
admin.site.register(AcmeOrder)

admin.site.register(Parcel)
admin.site.register(Warehouse)
admin.site.register(AcmeOrderStatus)


admin.site.register(AcmeUser)
admin.site.register(UserRole)

admin.site.register(DeliveryOperator)
admin.site.register(OrderDelivery)

