from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import PhoneNumber, OTP

class OTPManualTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.phone_number = "0555123456"
        self.otp_code = "12345"

    def test_manual_otp_generation(self):
        url = '/api/otps/generate/'
        data = {
            'phone_number': self.phone_number,
            'otp_code': self.otp_code
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['otp_code'], self.otp_code)
        
        # Verify it's in DB
        self.assertTrue(OTP.objects.filter(otp_code=self.otp_code).exists())
        
        otps = OTP.objects.filter(phone_number__phone_number=self.phone_number)
        self.assertEqual(otps.count(), 1)
        self.assertEqual(otps.first().otp_code, self.otp_code)

    def test_phone_number_validation(self):
        url = '/api/otps/generate/'
        data = {
            'phone_number': '1234567890', # Does not start with 0
            'otp_code': '12345'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Phone number must start with 0', str(response.data))

    def test_missing_otp_code(self):
        url = '/api/otps/generate/'
        data = {
            'phone_number': self.phone_number
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('OTP code is required', str(response.data))

    def test_otp_verification(self):
        # First generate
        self.client.post('/api/otps/generate/', {
            'phone_number': self.phone_number,
            'otp_code': self.otp_code
        }, format='json')
        
        # Then verify
        url = '/api/otps/verify/'
        data = {
            'phone_number': self.phone_number,
            'otp_code': self.otp_code
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check invalidation
        otp = OTP.objects.get(otp_code=self.otp_code)
        self.assertFalse(otp.is_valid)
