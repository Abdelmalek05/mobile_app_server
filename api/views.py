from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta
import random
import uuid

from .models import PhoneNumber, OTP, Contact, Prospect, Activity
from .serializers import PhoneNumberSerializer, OTPSerializer, OTPVerifySerializer, ContactSerializer, ProspectSerializer, ActivitySerializer

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
        phone_number_str = request.data.get("phone_number")
        if not phone_number_str:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Check if phone number exists (do NOT create)
            phone_obj = PhoneNumber.objects.get(phone_number=phone_number_str)
        except PhoneNumber.DoesNotExist:
            return Response({'error': 'Phone number not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Generate OTP for existing phone number
        otp_code = f"{random.randint(10000, 99999)}"
        otp = OTP.objects.create(
            phone_number=phone_obj, 
            otp_code=otp_code
        )
        return Response({
            "success": True,
            "message": "OTP generated successfully",
            "otp_code": otp_code
        }, status=status.HTTP_201_CREATED)

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
        
        LOGIN ENDPOINT: Only generates OTP for EXISTING phone numbers.
        Does NOT create phone numbers.
        """
        phone_number_str = request.data.get('phone_number')
        if not phone_number_str:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if phone number exists (do NOT create with get_or_create)
            phone_obj = PhoneNumber.objects.get(phone_number=phone_number_str)
        except PhoneNumber.DoesNotExist:
            return Response({'error': 'Phone number not found'}, status=status.HTTP_404_NOT_FOUND)

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
            
            # Get or create a user for this phone number (for activities tracking)
            from django.contrib.auth.models import User
            user, _ = User.objects.get_or_create(
                username=phone_number_str,
                defaults={'is_active': True}
            )
            
            # Get or create auth token for this user
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'OTP verified successfully',
                'token': token.key,
                'user_id': user.id,
                'phone_number': phone_number_str
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        """Return only contacts belonging to the logged-in user"""
        return Contact.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically assign the logged-in user when creating a contact"""
        serializer.save(user=self.request.user)

class ProspectViewSet(viewsets.ModelViewSet):
    serializer_class = ProspectSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        """Return only prospects belonging to the logged-in user"""
        return Prospect.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically assign the logged-in user when creating a prospect"""
        serializer.save(user=self.request.user)

class ActivityViewSet(ReadOnlyModelViewSet):
    serializer_class = ActivitySerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        """Return only activities belonging to the logged-in user, ordered by most recent"""
        return Activity.objects.filter(user=self.request.user).order_by('-timestamp')