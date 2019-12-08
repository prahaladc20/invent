from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Inventory,InventoryApproval
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['groups'] = self.user.groups.values_list('name', flat=True)
        return data


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name','password')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		password = validated_data.pop('password')
		user = User(**validated_data)
		user.username = validated_data.get('email')
		user.set_password(password)
		user.save()
		return user
        
class InventorySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Inventory
        fields = ('author','product_id', 'product_name', 'vendor', 'mrp','batch_num','batch_date','quantity')


class InventoryApprovalSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = InventoryApproval
        fields = ('author','product_id', 'product_name', 'vendor', 'mrp','batch_num','batch_date','quantity','status','action', 'master_id')
