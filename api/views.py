from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import random
import uuid

from .models import PhoneNumber, OTP, Contact, Prospect
from .serializers import PhoneNumberSerializer, OTPSerializer, OTPVerifySerializer, ContactSerializer, ProspectSerializer

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
    http_method_names = ['post']


    @action(detail=False, methods=['post'])
    def request_otp(self, request):
        phone_number = request.data.get("phone_number")
        # create an OTP here, e.g., from request
        otp = OTP.objects.create(phone_number_id=PhoneNumber.objects.get(phone_number=phone_number).id, otp_code="12345")
        return Response({"success": True})

    def create(self, request, *args, **kwargs):
        """
        Standard POST to /api/otps/
        Expects: {"phone_number": "<UUID of PhoneNumber object>"}
        """
        phone_number_id = request.data.get('phone_number')
        
        if not phone_number_id:
            return Response({'error': 'Phone number ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get the PhoneNumber object by UUID
            phone_obj = PhoneNumber.objects.get(id=phone_number_id)
            
            # Generate OTP code
            otp_code = 12345
            expires_at = timezone.now() + timedelta(minutes=5)
            
            # Create OTP
            otp = OTP.objects.create(
                phone_number=phone_obj,
                otp_code=otp_code,
                expires_at=expires_at,
                is_valid=True
            )
            
            # Return response with OTP code visible
            return Response({
                'id': str(otp.id),
                'phone_number': str(phone_obj.id),
                'phone_number_string': phone_obj.phone_number,  # Actual phone number
                'otp_code': otp_code,  # Now visible!
                'is_valid': otp.is_valid,
                'created_at': otp.created_at,
                'expires_at': expires_at
            }, status=status.HTTP_201_CREATED)
            
        except PhoneNumber.DoesNotExist:
            return Response({'error': 'Phone number not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """
        Custom action: POST to /api/otps/generate/
        Expects: {"phone_number": "+1234567890"} (actual phone number string)
        """
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
            'otp_code': otp_code,
            'expires_at': expires_at
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        phone_number_str = serializer.validated_data.get('phone_number')
        otp_code = serializer.validated_data.get('otp_code')

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