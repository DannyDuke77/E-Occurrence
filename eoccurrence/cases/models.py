from django.db import models
from django.utils import timezone

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Case(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('under_investigation', 'Under Investigation'),
        ('in_court', 'In Court'),
        ('closed', 'Closed'),
        ('dismissed', 'Dismissed'),
    ]

    BAIL_CHOICES = [
        ('granted', 'Granted'),
        ('denied', 'Denied'),
        ('pending', 'Pending'),
    ]

    CASE_TYPE_CHOICES = [
    # Crimes against persons
    ('ASSAULT', 'Assault'),
    ('GBV', 'Gender-Based Violence'),
    ('HOMICIDE', 'Homicide / Murder'),
    ('MISSING_PERSON', 'Missing Person'),
    ('SUICIDE', 'Suicide / Attempted Suicide'),

    # Property crimes
    ('THEFT', 'Theft'),
    ('ROBBERY', 'Robbery'),
    ('BURGLARY', 'Burglary / Break-in'),
    ('ARSON', 'Arson'),

    # Fraud & corruption
    ('FRAUD', 'Fraud'),
    ('CORRUPTION', 'Corruption / Bribery'),

    # Public order
    ('TRAFFIC', 'Traffic Offense'),
    ('PUBLIC_DISTURBANCE', 'Public Disturbance'),
    ('ILLEGAL_ASSEMBLY', 'Illegal Assembly / Protest'),

    # Drugs & contraband
    ('DRUG_POSSESSION', 'Drug Possession / Trafficking'),
    ('ILLEGAL_WEAPONS', 'Illegal Possession of Firearms / Weapons'),

    # Domestic / family issues
    ('DOMESTIC', 'Domestic Dispute'),
    ('CHILD_ABUSE', 'Child Abuse / Neglect'),

    # Miscellaneous
    ('LOST_PROPERTY', 'Lost Property'),
    ('RECOVERED_PROPERTY', 'Recovered Property'),
    ('OTHER', 'Other'),
]

    case_number = models.CharField(max_length=50, unique=True)
    case_type = models.CharField(
        max_length=30, choices=CASE_TYPE_CHOICES, default='OTHER',
    )
    complainant = models.ForeignKey(
        'Complainant', on_delete=models.SET_NULL, null=True, related_name='cases'
    )
    suspects = models.ManyToManyField(
        'Suspect', blank=True, related_name='cases'
    )
    witnesses = models.ManyToManyField(
        'Witness', blank=True, related_name='cases'
    )
    incident_date = models.DateField(null=True, blank=True)  # Date of the incident
    location = models.CharField(max_length=255, blank=True, null=True)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    recorded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='cases_reported'
    )
    
    bail_decision = models.CharField(
        max_length=20, choices=BAIL_CHOICES, default='pending',
    )

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='open')
    court_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.case_number:
            today = timezone.now().strftime('%Y%m%d')
            last_case = Case.objects.filter(case_number__startswith=today).order_by('-case_number').first()
            if last_case:
                last_number = int(last_case.case_number[-4:]) + 1
            else:
                last_number = 1
            self.case_number = f"{today}-{last_number:04d}"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.case_number} - {self.title}"


class Complainant(models.Model):
    # Basic personal details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    id_number = models.CharField(max_length=20, blank=True, null=True, unique=True)  # National ID or passport
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Demographics
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # Address / location
    address = models.TextField(blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    sub_county = models.CharField(max_length=100, blank=True, null=True)

    # Meta fields
    created_at = models.DateTimeField(auto_now_add=True)  # When record was first created
    updated_at = models.DateTimeField(auto_now=True)      # Last update time

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return f"{full_name} - {self.id_number or 'No ID'}"
    
class Suspect(models.Model):
    name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    contact_info = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    arrest_date = models.DateField(blank=True, null=True)
    charges = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Witness(models.Model):
    name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    contact_info = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_statement = models.DateField(auto_now_add=True)
    statement = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Witnesses"