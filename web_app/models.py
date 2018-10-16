from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Create your models here.
class Parcel(models.Model):
    weight = models.FloatField()
    volume = models.FloatField()
    # TODO: define ENUM of standard shapes
    shape = models.CharField(max_length=100)


class IncomingOrder(models.Model):
    created_on = models.TimeField()
    priority = models.IntegerField()
    parcel_id = models.ForeignKey(Parcel, on_delete=models.CASCADE)

    @property
    def incoming_orders_order_id_fkey(self):
        return self.parcel_id.id


class DispatchOrder(models.Model):
    incoming_order_id = models.ForeignKey(IncomingOrder, on_delete=models.CASCADE)

    @property
    def dispatch_order_incoming_order_id_fkey(self):
        return self.incoming_order_id.id


class Contact(models.Model):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    additional_info = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)


class Warehouse(models.Model):
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    max_capacity = models.FloatField()
    is_active = models.BooleanField(default=True)

    @property
    def warehouses_contact_id(self):
        return self.contact_id.id


class DispatchStatus(models.Model):
    created_on = models.TimeField()
    status = models.CharField(max_length=20)
    # TODO: make ENUM of all possible statuses.
    warehouse_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE)  # OPTIONAL
    dispatch_order_id = models.ForeignKey(DispatchOrder, on_delete=models.CASCADE)

    @property
    def dispatch_status_warehouse_id_fkey(self):
        return self.warehouse_id.id

    @property
    def dispatch_status_pkey(self):
        return self.dispatch_order_id.id
    # TODO check if it is correct


# TODO: Add 'next_vector' parameter.
class TransportationVector(models.Model):
    weather = models.CharField(max_length=50)
    traffic = models.CharField(max_length=255)


# TODO: Fix relation between routes, vectors and operators.
class TransportationRoutes(models.Model):
    transport_type = models.CharField(max_length=50)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)


class DeliveryOperator(models.Model):
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)

    @property
    def delivery_operators_contact_id(self):
        return self.contact_id.id


class TransportationCompany(models.Model):
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    transportation_types = models.CharField(max_length=50)

    # TODO: Should we create separate table or enum for types?

    @property
    def transportation_companies_contact_id_fkey(self):
        return self.contact_id.id
