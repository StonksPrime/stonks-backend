from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id','quantity', 'break_even_price', 'closing_price', 'opening_date', 'closing_date', 'order_status', 'user', 'asset', 'broker']

class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = ['id','name', 'ticker', 'sector', 'description', 'last_price']

class ETFSerializer(serializers.ModelSerializer):
    class Meta:
        model = ETF
        fields = ['id','name', 'ticker', 'sector', 'description', 'last_price', 'isin', 'country', 'region']

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ['id','name', 'ticker', 'sector', 'description', 'last_price', 'isin', 'country', 'region']

class FiatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fiat
        fields = ['id','name', 'ticker', 'sector', 'description', 'last_price']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id','name', 'ticker', 'sector', 'description', 'last_price', 'isin', 'country', 'region']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'person', 'broker_exchange', 'broker_username', 'broker_password', 'token_key', 'token_secret'] #TODO: passwords and keys should be here?

class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = ['id', 'name', 'country', 'fiscal_country']

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id','name', 'ticker', 'sector', 'description', 'last_price']

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'last_login','public_profile', 'birth_date','password','profile_picture']

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data


    def create(self, validated_data):
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        return self.Meta.model.objects.create_user(**data)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'password1', 'password2',
            'first_name', 'last_name',
        )
        read_only_fields = ('id',)

class LogInSerializer(TokenObtainPairSerializer):


    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token

    def validate(self, attrs):
        # The default result (access/refresh tokens)
        
        data = {}
        print(attrs)
        
        self.user = Investor.objects.filter(email=attrs[self.username_field]).first()
        
        refresh = self.get_token(self.user)

        data['token'] = {}
        data['token']['access_token'] = str(refresh.access_token)
        data['token']['refresh_token'] = str(refresh)

        update_last_login(None, self.user)

        if not self.user:
            raise ValidationError('The user is not valid.')

        if self.user:
            if not self.user.check_password(attrs['password']):
                raise ValidationError('Incorrect credentials.')

        if self.user is None or not self.user.is_active:
            raise ValidationError('No active account found with the given credentials')
        # Custom data to include a part from token
        data['id']= self.user.id
        data.update({'username': self.user.username})
        data['full_name'] = self.user.first_name + self.user.last_name
        data['role'] = 'user'
        return data