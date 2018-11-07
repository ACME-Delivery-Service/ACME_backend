# Generated by Django 2.1.2 on 2018-10-11 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('additional_info', models.CharField(max_length=255)),
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
                ('contact_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.Contact')),
            ],
        ),
        migrations.CreateModel(
            name='DispatchOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DispatchStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.TimeField()),
                ('status', models.CharField(max_length=20)),
                ('dispatch_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.DispatchOrder')),
            ],
        ),
        migrations.CreateModel(
            name='IncomingOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.TimeField()),
                ('priority', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('volume', models.FloatField()),
                ('shape', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TransportationCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transportation_types', models.CharField(max_length=50)),
                ('contact_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.Contact')),
            ],
        ),
        migrations.CreateModel(
            name='TransportationRoutes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transport_type', models.CharField(max_length=50)),
                ('start_location', models.CharField(max_length=255)),
                ('end_location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TransportationVector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weather', models.CharField(max_length=50)),
                ('traffic', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_capacity', models.FloatField()),
                ('is_active', models.BooleanField(default=True)),
                ('contact_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.Contact')),
            ],
        ),
        migrations.AddField(
            model_name='incomingorder',
            name='parcel_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.Parcel'),
        ),
        migrations.AddField(
            model_name='dispatchstatus',
            name='warehouse_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.Warehouse'),
        ),
        migrations.AddField(
            model_name='dispatchorder',
            name='incoming_order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.IncomingOrder'),
        ),
    ]
