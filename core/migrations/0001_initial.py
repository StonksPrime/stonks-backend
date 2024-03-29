# Generated by Django 3.1.5 on 2021-01-31 18:41

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('public_profile', models.BooleanField(default=0)),
                ('birth_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'core_investor',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('ticker', models.CharField(max_length=60, unique=True)),
                ('sector', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=60)),
                ('last_price', models.DecimalField(decimal_places=10, default=0, max_digits=20)),
            ],
            options={
                'db_table': 'core_financial_asset',
            },
        ),
        migrations.CreateModel(
            name='Broker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('fiscal_country', django_countries.fields.CountryField(max_length=2)),
            ],
            options={
                'db_table': 'broker',
            },
        ),
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.asset')),
            ],
            options={
                'db_table': 'core_asset_crypto',
            },
            bases=('core.asset',),
        ),
        migrations.CreateModel(
            name='ETF',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.asset')),
                ('isin', models.CharField(max_length=60)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('region', models.CharField(max_length=60)),
            ],
            options={
                'db_table': 'core_asset_etf',
            },
            bases=('core.asset',),
        ),
        migrations.CreateModel(
            name='Fiat',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.asset')),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
            options={
                'db_table': 'core_asset_fiat',
            },
            bases=('core.asset',),
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.asset')),
                ('isin', models.CharField(max_length=60)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('region', models.CharField(max_length=60)),
            ],
            options={
                'db_table': 'core_asset_fund',
            },
            bases=('core.asset',),
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.asset')),
                ('isin', models.CharField(max_length=60)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('region', models.CharField(max_length=60)),
            ],
            options={
                'db_table': 'core_asset_stock',
            },
            bases=('core.asset',),
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=8, default=0, max_digits=18)),
                ('break_even_price', models.DecimalField(decimal_places=8, default=0, max_digits=18)),
                ('closing_price', models.DecimalField(decimal_places=8, default=0, max_digits=18)),
                ('opening_date', models.DateTimeField(default=None)),
                ('closing_date', models.DateTimeField(default=None)),
                ('order_status', models.CharField(choices=[('O', 'Open'), ('C', 'Closed'), ('P', 'Pending'), ('X', 'Canceled')], max_length=1)),
                ('asset', models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='position_asset', to='core.asset')),
                ('broker', models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='position_broker', to='core.broker')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='position_investor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'core_investor_asset_position',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broker_username', models.CharField(blank=True, max_length=60)),
                ('broker_password', models.CharField(blank=True, max_length=60)),
                ('token_key', models.CharField(blank=True, max_length=200)),
                ('token_secret', models.CharField(blank=True, max_length=200)),
                ('broker_exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.broker')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'core_investor_broker_account',
            },
        ),
        migrations.AddField(
            model_name='investor',
            name='brokers',
            field=models.ManyToManyField(through='core.Account', to='core.Broker'),
        ),
        migrations.AddField(
            model_name='investor',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='investor',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
