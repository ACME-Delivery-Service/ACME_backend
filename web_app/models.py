from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
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
    contact = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)

    @property
    def customer_contact_id(self):
        return self.contact.id


class Coordinates(models.Field):
    x = models.FloatField()
    y = models.FloatField()


class Location(models.Model):
    location_address = models.CharField(max_length=255)
    lat_long = Coordinates()


class DeliveryPeriod(models.Field):
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 104
        super().__init__(*args, **kwargs)


class AcmeOrder(models.Model):
    created_on = models.DateTimeField()
    comment = models.TextField()
    customer = models.ForeignKey(AcmeCustomer, on_delete=models.PROTECT)
    priority = models.IntegerField()
    start_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="acme_order_start_location")
    end_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="acme_order_end_location")
    scheduled_time = DeliveryPeriod()

    @property
    def acme_order_start_location_id(self):
        return self.start_location.id

    @property
    def acme_order_end_location_id(self):
        return self.end_location.id

    @property
    def customer_id_fkey(self):
        return self.customer.id


class ShapeTypes(Enum):
    POSTCARD = 'postcard'
    LETTER = 'letter'
    LARGE_ENVELOPE = 'large_envelope'
    PARCEL = 'parcel'


class Parcel(models.Model):
    weight = models.FloatField()
    dimension = ArrayField(models.FloatField(), size=3, null=True)
    shape = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in ShapeTypes])
    order = models.ForeignKey(AcmeOrder, on_delete=models.CASCADE, null=True)

    @property
    def order_id_fkey(self):
        return self.order.id


class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=255, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.DO_NOTHING, null=True)
    max_capacity = models.FloatField()
    is_active = models.BooleanField(default=True)

    @property
    def warehouses_contact_id(self):
        return self.contact.id


class OrderStatusType(Enum):
    CREATED = 'created'
    APPROVED = 'approved'
    EN_ROUT = 'en_rout'
    STORED = 'stored'
    DELIVERED = 'delivered'


class AcmeOrderStatus(models.Model):
    created_on = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in OrderStatusType])
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(AcmeOrder, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('order', 'created_on'),)

    @property
    def orders_warehouse_id(self):
        return self.warehouse.id

    @property
    def orders_order_id(self):
        return self.order.id


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
    contact = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=255, unique=True)
    file_url = models.CharField(max_length=255)

    @property
    def users_contact_id(self):
        return self.contact.id


class UserRole(models.Model):
    user = models.ForeignKey(AcmeUser, on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in AcmeRoles])

    @property
    def roles_users_id(self):
        return self.user.id


class DeliveryStatusTypes(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


class DeliveryOperator(models.Model):
    operator = models.ForeignKey(AcmeUser, on_delete=models.PROTECT, null=True)
    current_pos = models.ForeignKey(Location, on_delete=models.DO_NOTHING, null=True)
    pos_last_updated = models.DateTimeField(null=True)

    @property
    def users_id(self):
        return self.operator.id

    @property
    def users_location_id(self):
        return self.current_pos.id


class OrderDelivery(models.Model):
    order = models.ForeignKey(AcmeOrder, on_delete=models.CASCADE)
    delivery_operator = models.ForeignKey(DeliveryOperator, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in DeliveryStatusTypes])
    start_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="order_delivery_start_location")
    end_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="order_delivery_end_location")
    active_time_period = JSONField()

    class Meta:
        unique_together = (('order', 'delivery_operator'))

    @property
    def orders_id_fkey(self):
        return self.order.id

    @property
    def orders_delivery_operator_id(self):
        return self.delivery_operator.id

    @property
    def acme_order_start_location_id(self):
        return self.start_location.id

    @property
    def acme_order_end_location_id(self):
        return self.end_location.id
