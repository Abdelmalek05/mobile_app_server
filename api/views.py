from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import random
import uuid

from .models import PhoneNumber, OTP, Contact, Prospect
from .serializers import PhoneNumberSerializer, OTPSerializer, ContactSerializer, ProspectSerializer

class PhoneNumberViewSet(viewsets.ModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if exists, if so return it, otherwise create
        obj, created = PhoneNumber.objects.get_or_create(phone_number=phone_number)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class OTPViewSet(viewsets.ModelViewSet):
    queryset = OTP.objects.all()
    serializer_class = OTPSerializer
    http_method_names = ['post'] # Only allow custom actions essentially

    @action(detail=False, methods=['post'])
    def generate(self, request):
        phone_number_str = request.data.get('phone_number')
        if not phone_number_str:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure phone number exists in DB
        phone_obj, _ = PhoneNumber.objects.get_or_create(phone_number=phone_number_str)

        otp_code = f"{random.randint(10000, 99999)}"
        expires_at = timezone.now() + timedelta(minutes=5)

        otp = OTP.objects.create(
            phone_number=phone_obj,
            otp_code=otp_code,
            expires_at=expires_at,
            is_valid=True
        )

        # In a real app, send SMS here. For now just return it for testing.
        return Response({
            'message': 'OTP generated successfully',
            'phone_number': phone_number_str,
            'otp_code': otp_code, # Included for development/testing convenience
            'expires_at': expires_at
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        phone_number_str = request.data.get('phone_number')
        otp_code = request.data.get('otp_code')

        if not phone_number_str or not otp_code:
            return Response({'error': 'Phone number and OTP code are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            phone_obj = PhoneNumber.objects.get(phone_number=phone_number_str)
        except PhoneNumber.DoesNotExist:
             return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)

        # Find the latest valid OTP for this phone number
        otp = OTP.objects.filter(
            phone_number=phone_obj,
            otp_code=otp_code,
            is_valid=True,
            expires_at__gt=timezone.now()
        ).first()

        if otp:
            # Mark as used (invalidate)
            otp.is_valid = False
            otp.save()
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_field = 'id'

class ProspectViewSet(viewsets.ModelViewSet):
    queryset = Prospect.objects.all()
    serializer_class = ProspectSerializer
    lookup_field = 'id'
