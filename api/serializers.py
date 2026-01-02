from rest_framework import serializers
from .models import PhoneNumber, OTP, Contact, Prospect, Activity

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['id', 'phone_number', 'created_at']
        read_only_fields = ['id', 'created_at']

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['id', 'phone_number', 'otp_code', 'is_valid', 'created_at', 'expires_at']
        read_only_fields = ['id', 'otp_code', 'is_valid', 'created_at', 'expires_at']

class OTPVerifySerializer(serializers.Serializer):
    """Serializer for OTP verification endpoint"""
    phone_number = serializers.CharField(required=True, help_text="Phone number string")
    otp_code = serializers.CharField(required=True, help_text="OTP code to verify")

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone_number', 'email', 'company', 'type']
        read_only_fields = ['id']

class ProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prospect
        fields = '__all__'
        read_only_fields = ['id']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title', 'description', 'type', 'timestamp']
        read_only_fields = ['id', 'timestamp']
