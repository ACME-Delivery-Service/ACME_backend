from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from enum import Enum

from web_app.managers import UserManager


class Contact(models.Model):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    additional_info = models.TextField(null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, null=True)
    company = models.CharField(max_length=255, null=True)

    def __str__(self):
        return '(%s) %s %s - contact' % (self.pk, self.first_name, self.last_name)


class AcmeCustomer(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)

    @property
    def customer_contact_id(self):
        return self.contact.id

    def __str__(self):
        return '(%s) %s %s - contact' % (self.pk, self.contact.first_name, self.contact.last_name)


class Location(models.Model):
    address = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()


'''class DeliveryPeriod(models.Field):
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False) '''


class AcmeOrder(models.Model):
    created_on = models.DateTimeField()
    comment = models.TextField(null=True)
    customer = models.ForeignKey(AcmeCustomer, on_delete=models.PROTECT)
    priority = models.IntegerField()
    start_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="acme_order_start_location")
    end_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="acme_order_end_location")
    scheduled_time_start_time = models.DateTimeField()  # Custom Type DeliveryPeriod
    scheduled_time_end_time = models.DateTimeField()  # Custom Type DeliveryPeriod

    @property
    def customer_id_fkey(self):
        return self.customer.id

    '''@property
    def acme_order_start_location_id(self):
        return self.start_location.id

    @property
    def acme_order_end_location_id(self):
        return self.end_location.id 
    '''


class ShapeTypes(Enum):
    POSTCARD = 'postcard'
    LETTER = 'letter'
    LARGE_ENVELOPE = 'large_envelope'
    PARCEL = 'parcel'

    @classmethod
    def all(self):
        return [ShapeTypes.POSTCARD, ShapeTypes.LETTER, ShapeTypes.LARGE_ENVELOPE, ShapeTypes.PARCEL]


class Parcel(models.Model):
    weight = models.FloatField()
    dimension = ArrayField(models.FloatField(), size=3, null=True)
    shape = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in ShapeTypes.all()])
    order = models.ForeignKey(AcmeOrder, on_delete=models.CASCADE, null=True)

    @property
    def order_id_fkey(self):
        return self.order.id


class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=255, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.DO_NOTHING, null=True)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, null=True)
    max_capacity = models.FloatField()
    is_active = models.BooleanField(default=True)

    @property
    def warehouses_contact_id(self):
        return self.contact.id


class OrderStatusType(Enum):
    CREATED = 'created'
    APPROVED = 'approved'
    EN_ROUTE = 'en_route'
    STORED = 'stored'
    DELIVERED = 'delivered'

    @classmethod
    def all(self):
        return [OrderStatusType.CREATED, OrderStatusType.APPROVED, OrderStatusType.EN_ROUTE,
                OrderStatusType.STORED, OrderStatusType.DELIVERED]


class AcmeOrderStatus(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in OrderStatusType.all()])
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, null=True, blank=True)
    order = models.ForeignKey(AcmeOrder, on_delete=models.CASCADE, related_name="order_status")

    class Meta:
        unique_together = (('order', 'created_on'),)

    @property
    def orders_warehouse_id(self):
        return self.warehouse.id

    @property
    def orders_order_id(self):
        return self.order.id


class AcmeRegions(Enum):
    EU = 'EU'
    RU = 'RU'
    CH = 'CH'
    UK = 'UK'

    @classmethod
    def all(self):
        return [AcmeRegions.EU, AcmeRegions.RU, AcmeRegions.CH, AcmeRegions.UK]


class AcmeRoles(Enum):
    CEO = 'CEO'
    DO = 'DO'
    CO = 'CO'
    CS = 'CS'
    CD = 'CD'

    @classmethod
    def all(self):
        return [AcmeRoles.CEO, AcmeRoles.DO, AcmeRoles.CO, AcmeRoles.CS, AcmeRoles.CD]


class AcmeUser(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(max_length=128)
    region = models.CharField(max_length=5, choices=[(tag.value, tag.name) for tag in AcmeRegions.all()])
    email = models.EmailField(max_length=255, unique=True)
    contacts = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=255, unique=True)
    avatar = models.CharField(max_length=255, null=True)

    groups = None
    user_permissions = None

    is_staff = True

    objects = UserManager()

    DEFAULT_AVATAR = 'https://backend.acme-company.site/static/uploads/ava1.jpg'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['region', 'contacts_id']

    @property
    def users_contact_id(self):
        return self.contacts.id

    @property
    def is_superuser(self):
        return self.get_role() == AcmeRoles.CEO.value

    @property
    def get_avatar(self):
        if self.avatar:
            return self.avatar
        return self.DEFAULT_AVATAR

    def get_full_name(self):
        return self.get_short_name() + ' (' + self.email + ')'

    def get_short_name(self):
        return self.contacts.first_name + ' ' + self.contacts.last_name

    def get_role(self):
        try:
            role_obj = UserRole.objects.get(pk=self.id)
        except UserRole.DoesNotExist:
            pass
        else:
            return role_obj.role

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class UserRole(models.Model):
    user = models.ForeignKey(AcmeUser, on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in AcmeRoles.all()])

    @property
    def roles_users_id(self):
        return self.user.id


class DeliveryStatusTypes(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

    @classmethod
    def all(self):
        return [DeliveryStatusTypes.PENDING, DeliveryStatusTypes.IN_PROGRESS, DeliveryStatusTypes.COMPLETED]


class DeliveryOperator(models.Model):
    operator = models.ForeignKey(AcmeUser, on_delete=models.PROTECT, null=True)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, null=True)
    location_last_updated = models.DateTimeField(null=True)

    @property
    def users_id(self):
        return self.operator.id

    @property
    def users_location_id(self):
        return self.location.id


class OrderDelivery(models.Model):
    order = models.ForeignKey(AcmeOrder, on_delete=models.CASCADE, related_name="order_deliveries")
    delivery_operator = models.ForeignKey(DeliveryOperator, on_delete=models.CASCADE, related_name="delivery_operator")
    delivery_status = models.CharField(max_length=20,
                                       choices=[(tag.value, tag.name) for tag in DeliveryStatusTypes.all()])
    start_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="order_delivery_start_location")
    end_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="order_delivery_end_location")
    active_time_period = JSONField(default=list)  # Customtype Array of DeliveryPeriod

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
