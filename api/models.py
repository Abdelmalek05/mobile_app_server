from django.db import models
import uuid

class Prospect(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entreprise = models.TextField()
    adresse = models.TextField(blank=True, null=True)
    wilaya = models.TextField(blank=True, null=True)
    commune = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    categorie = models.TextField(blank=True, null=True)
    forme_legale = models.TextField(blank=True, null=True)
    secteur = models.TextField(blank=True, null=True)
    sous_secteur = models.TextField(blank=True, null=True)
    nif = models.TextField(blank=True, null=True)
    registre_commerce = models.TextField(blank=True, null=True)
    status = models.TextField()

    class Meta:
        managed = False
        db_table = 'prospects'

    def __str__(self):
        return self.entreprise

class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    phone_number = models.TextField()
    email = models.TextField()
    company = models.TextField(blank=True, null=True)
    type = models.TextField()
    prospect = models.ForeignKey(Prospect, models.DO_NOTHING, blank=True, null=True, related_name='contacts')

    class Meta:
        managed = False
        db_table = 'contacts'

    def __str__(self):
        return self.name

class Phone(models.Model):
    phone_number = models.CharField(primary_key=True, max_length=20) 

    class Meta:
        managed = False
        db_table = 'phones'

    def __str__(self):
        return self.phone_number

class OTP(models.Model):
    # Composite primary key logic is tricky in Django. 
    # Usually we treat one as PK or use `unique_together`. 
    # Since schema is fixed, we'll map fields and use `unique_together` for Django's knowledge,
    # but actual DB usage might differ. 
    # However, Django ORM *needs* a single primary key to work well for updates/deletes.
    # The user said "composite primary key (phone_number + otp_code)".
    # We will mark `phone_number` as PK for Django model just to make it run, 
    # but be careful with .save() if it's not actually unique alone.
    # A better approach for Django read-only/managed=False is to maybe use a surrogate key if one existed,
    # but here we might have to pick one. 
    # LET'S ASSUME we can just use phone_number as the logical PK for querying by phone.
    
    phone_number = models.ForeignKey(Phone, models.DO_NOTHING, db_column='phone_number')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'otps'
        unique_together = (('phone_number', 'otp_code'),)
