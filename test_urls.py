import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_tracking.settings')
django.setup()

from django.test import Client

client = Client()

# Test feedback/create/
print("Testing /feedback/create/...")
response = client.get('/feedback/create/')
print(f"Status: {response.status_code}")
if response.status_code == 500:
    print("ERROR: 500 Internal Server Error")
elif response.status_code == 302:
    print("Redirect to login (expected for non-authenticated user)")
else:
    print(f"Content-Type: {response.get('Content-Type')}")

# Test admin
print("\nTesting /admin/...")
response = client.get('/admin/')
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("Admin page loaded successfully")
elif response.status_code == 302:
    print("Redirect to login (expected for non-authenticated user)")
else:
    print(f"ERROR: {response.status_code}")