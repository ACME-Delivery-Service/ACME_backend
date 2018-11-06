from django.db import models
from django.contrib.postgres.fields import ArrayField

from enum import Enum


class Contact(models.Model):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    additional_info = models.TextField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)


class AcmeCustomer(models.Model):
    contact_id = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)

    @property
    def customer_contact_id(self):
        return self.contact_id.id

class Coordinates(models.Field):
    x = models.FloatField()
    y = models.FloatField()

class Location(models.Model):
    location_address = models.CharField(max_length=255)
    lat_long = Coordinates()


class DeliveryPeriod(models.Field):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class AcmeOrder(models.Model):
    created_on = models.DateTimeField()
    comment = models.TextField()
    customer_id = models.ForeignKey(AcmeCustomer, on_delete=models.PROTECT)
    priority = models.IntegerField()
    start_location_id = models.ForeignKey(Location, on_delete=models.PROTECT,related_name="acme_order_start_location")
    end_location_id = models.ForeignKey(Location, on_delete=models.PROTECT,related_name="acme_order_end_location")
    scheduled_time = DeliveryPeriod()

    @property
    def acme_order_start_location_id(self):
        return self.start_location_id.id

    @property
    def acme_order_end_location_id(self):
        return self.end_location_id.id

    @property
    def customer_id_fkey(self):
        return self.customer_id.id


class ShapeTypes(Enum):
    POSTCARD = 'postcard'
    LETTER = 'letter'
    LARGE_ENVELOPE = 'large_envelope'
    PARCEL = 'parcel'


class Parcel(models.Model):
    weight = models.FloatField()
    dimension = ArrayField(models.FloatField(), size=3)
    shape = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in ShapeTypes])
    order_id = models.ForeignKey(AcmeOrder, on_delete=models.CASCADE)

    @property
    def order_id_fkey(self):
        return self.order_id.id


class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=255)
    contact_id = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)
    max_capacity = models.FloatField()
    is_active = models.BooleanField(default=True)

    @property
    def warehouses_contact_id(self):
        return self.contact_id.id


class OrderStatusType(Enum):
    CREATED = 'created'
    APPROVED = 'approved'
    EN_ROUT = 'en_rout'
    STORED = 'stored'
    DELIVERED = 'delivered'


class AcmeOrderStatus(models.Model):
    created_on = models.DateTimeField()
    status = models.CharField(max_length=20,choices=[(tag, tag.value) for tag in OrderStatusType])
    warehouse_id = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING)
    order_id = models.ForeignKey(AcmeOrder, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('order_id', 'created_on'),)

    @property
    def orders_warehouse_id(self):
        return self.warehouse_id.id

    @property
    def orders_order_id(self):
        return self.order_id.id


class AcmeLocations(Enum):
    EU = 'EU'
    RU = 'RU'
    CH = 'CH'
    UK = 'UK'


class AcmeRoles(Enum):
    CEO = 'CEO'
    DO = 'DO'
    CO = 'CO'
    CS = 'CS'
    CD = 'CD'


class AcmeUser(models.Model):
    password = models.CharField(max_length=16)
    user_location = models.CharField(max_length=5, choices=[(tag, tag.value) for tag in AcmeLocations])
    email = models.EmailField(max_length=255, unique=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=255, unique=True)
    file_url = models.CharField(max_length=255)

    @property
    def users_contact_id(self):
        return self.contact_id.id


class UserRole(models.Model):
    user_id = models.ForeignKey(AcmeUser, on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in AcmeRoles])

    @property
    def roles_users_id(self):
        return self.user_id.id


class DeliveryStatusTypes(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


class DeliveryOperator(models.Model):
    operator_id = models.ForeignKey(AcmeUser, on_delete=models.PROTECT)
    current_pos = models.ForeignKey(Location, on_delete=models.DO_NOTHING, null=True)
    pos_last_updated = models.DateTimeField()

    @property
    def users_id(self):
        return self.operator_id.id

    @property
    def users_location_id(self):
        return self.current_pos.id


class OrderDelivery(models.Model):
    order_id = models.ForeignKey(AcmeUser, on_delete=models.CASCADE)
    delivery_operator_id = models.ForeignKey(DeliveryOperator, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=20,choices=[(tag, tag.value) for tag in DeliveryStatusTypes])
    start_location_id = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="order_delivery_start_location")
    end_location_id = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="order_delivery_end_location")
    active_time_period = ArrayField(DeliveryPeriod())

    class Meta:
        unique_together = (('order_id', 'delivery_operator_id'))

    @property
    def orders_id_fkey(self):
        return self.order_id.id

    @property
    def orders_delivery_operator_id(self):
        return self.delivery_operator_id.id

    @property
    def acme_order_start_location_id(self):
        return self.start_location_id.id

    @property
    def acme_order_end_location_id(self):
        return self.end_location_id.id
