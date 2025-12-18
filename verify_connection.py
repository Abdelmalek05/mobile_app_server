import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from api.models import Prospect, Contact, Phone

def test_connection():
    print("--------------------------------------------------")
    print("Testing Supabase Database Connection...")
    print("--------------------------------------------------")
    try:
        # Check Prospects
        p_count = Prospect.objects.count()
        print(f"✅ Prospects Table Accessible. Count: {p_count}")
        
        # Check Contacts
        c_count = Contact.objects.count()
        print(f"✅ Contacts Table Accessible. Count: {c_count}")
        
        # Check Phones
        ph_count = Phone.objects.count()
        print(f"✅ Phones Table Accessible. Count: {ph_count}")
        
        print("--------------------------------------------------")
        print("🎉 Connection SUCCESSFUL!")
        print("--------------------------------------------------")
        
    except Exception as e:
        print("--------------------------------------------------")
        print("❌ Connection FAILED")
        print(f"Error: {e}")
        print("--------------------------------------------------")

if __name__ == "__main__":
    test_connection()
