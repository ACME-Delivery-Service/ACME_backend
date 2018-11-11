# Generated by Django 2.1.2 on 2018-11-08 09:26

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcmeCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='AcmeOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField()),
                ('comment', models.TextField()),
                ('priority', models.IntegerField()),
                ('scheduled_time_start_time', models.DateTimeField()),
                ('scheduled_time_end_time', models.DateTimeField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='web_app.AcmeCustomer')),
            ],
        ),
        migrations.CreateModel(
            name='AcmeOrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField()),
                ('status', models.CharField(choices=[('created', 'CREATED'), ('approved', 'APPROVED'), ('en_route', 'EN_ROUTE'), ('stored', 'STORED'), ('delivered', 'DELIVERED')], max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='web_app.AcmeOrder')),
            ],
        ),
        migrations.CreateModel(
            name='AcmeUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=16)),
                ('region', models.CharField(choices=[('EU', 'EU'), ('RU', 'RU'), ('CH', 'CH'), ('UK', 'UK')], max_length=5)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('token', models.CharField(max_length=255, unique=True)),
                ('avatar_url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('additional_info', models.TextField()),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryOperator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_last_updated', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_status', models.CharField(choices=[('pending', 'PENDING'), ('in_progress', 'IN_PROGRESS'), ('completed', 'COMPLETED')], max_length=20)),
                ('active_time_period', django.contrib.postgres.fields.jsonb.JSONField()),
                ('delivery_operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.DeliveryOperator')),
                ('end_location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_delivery_end_location', to='web_app.Location')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.AcmeOrder')),
                ('start_location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_delivery_start_location', to='web_app.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('dimension', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), null=True, size=3)),
                ('shape', models.CharField(choices=[('postcard', 'POSTCARD'), ('letter', 'LETTER'), ('large_envelope', 'LARGE_ENVELOPE'), ('parcel', 'PARCEL')], max_length=20)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web_app.AcmeOrder')),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('CEO', 'CEO'), ('DO', 'DO'), ('CO', 'CO'), ('CS', 'CS'), ('CD', 'CD')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='web_app.AcmeUser')),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warehouse_name', models.CharField(max_length=255, null=True)),
                ('max_capacity', models.FloatField()),
                ('is_active', models.BooleanField(default=True)),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='web_app.Contact')),
            ],
        ),
        migrations.AddField(
            model_name='deliveryoperator',
            name='current_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='web_app.Location'),
        ),
        migrations.AddField(
            model_name='deliveryoperator',
            name='operator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='web_app.AcmeUser'),
        ),
        migrations.AddField(
            model_name='acmeuser',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='web_app.Contact'),
        ),
        migrations.AddField(
            model_name='acmeorderstatus',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='web_app.Warehouse'),
        ),
        migrations.AddField(
            model_name='acmeorder',
            name='end_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='acme_order_end_location', to='web_app.Location'),
        ),
        migrations.AddField(
            model_name='acmeorder',
            name='start_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='acme_order_start_location', to='web_app.Location'),
        ),
        migrations.AddField(
            model_name='acmecustomer',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='web_app.Contact'),
        ),
        migrations.AlterUniqueTogether(
            name='orderdelivery',
            unique_together={('order', 'delivery_operator')},
        ),
        migrations.AlterUniqueTogether(
            name='acmeorderstatus',
            unique_together={('order', 'created_on')},
        ),
    ]
