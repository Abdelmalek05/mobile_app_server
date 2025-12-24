import uuid
from django.db import models

class PhoneNumber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #managed = False  # The table is already created via SQL
        db_table = 'phone_numbers'

    def __str__(self):
        return self.phone_number

class OTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.CharField(max_length=5)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        #managed = False
        db_table = 'otps'

    def __str__(self):
        return f"{self.phone_number.phone_number} - {self.otp_code}"

class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    company = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=50)

    class Meta:
        #managed = False
        db_table = 'contacts'

    def __str__(self):
        return self.name

class Prospect(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entreprise = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    wilaya = models.CharField(max_length=100, null=True, blank=True)
    commune = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    categorie = models.CharField(max_length=100, null=True, blank=True)
    forme_legale = models.CharField(max_length=100, null=True, blank=True)
    secteur = models.CharField(max_length=100, null=True, blank=True)
    sous_secteur = models.CharField(max_length=100, null=True, blank=True)
    nif = models.CharField(max_length=50, null=True, blank=True)
    registre_commerce = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50)

    class Meta:
        #managed = False
        db_table = 'prospects'

    def __str__(self):
        return self.entreprise
