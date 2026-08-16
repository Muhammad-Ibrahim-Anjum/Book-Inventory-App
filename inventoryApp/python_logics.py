from datetime import datetime
from .models import Member

def generate_membership_number():
    year = datetime.now().year
    last = Member.objects.filter(membership_number__startswith=f"MEM-{year}-").count() + 1
    return f"MEM-{year}-{last:04d}"