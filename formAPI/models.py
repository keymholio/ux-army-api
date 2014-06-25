from django.db import models
from django.core.validators import RegexValidator , validate_email, EmailValidator
from django.core.exceptions import ValidationError
from django.core.signing import TimestampSigner
import datetime
import json
import base64
from django.core.mail import EmailMessage


class FormAPI(models.Model):
    def validate_year(value):
        now = datetime.datetime.now()
        if value < (now.year - 100) or value > now.year:
            raise ValidationError('%s is not a valid year' % value)
    def createHASH(self):
        initial = {}
        initial['name'] = self.name
        initial['email'] = self.email
        initial['id'] = self.id

        print self.id
        signer = TimestampSigner()
        initial['signed'] = signer.sign(self.email)
        jsonresponse = json.dumps(initial)
        
        # print initial
        # print jsonresponse
        # print base64.urlsafe_b64encode(jsonresponse)
        # email = EmailMessage(
        #     "Link to complete application", 
        #     "Please go to " + base64.urlsafe_b64encode(jsonresponse) +
        #     "\nto complete your application", 
        #     to=[self.email]
        # )
        # email.send()
        return jsonresponse
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z ]*$',
                message='Name must consist of characters A-Z and/or a-z',
                code='Invalid Name'
            ),
        ]
    )
    email = models.EmailField(max_length = 254, 
        unique=False, error_messages={'unique':"This email has already been registered."})
    """models.CharField(
        max_length=100,
        validators=[
            EmailValidator(),
        ]
    )"""
    phone = models.CharField(
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Phone number must be numeric',
                code='Invalid phone'
            ),
        ]
    )
    gender = models.CharField(
        max_length=6, 
        blank=True, 
        choices=[
            ('Male' , 'Male'),
            ('Female' , 'Female')
        ]
    )
    job = models.CharField(
        max_length = 25,
        blank=True,
        choices=[
            ('BDC Manager', 'BDC Manager'), 
            ('Controller', 'Controller'),
            ('Dealertrack Employee', 'Dealertrack Employee'),
            ('Entry Level Technician', 'Entry Level Technician'),
            ('F&I Director', 'F&I Director'),
            ('F&I Manager', 'F&I Manager'),
            ('Fixed Operations Director', 'Fixed Operations Director'),
            ('General Manager', 'General Manager'),
            ('Internet Director', 'Internet Director'),
            ('Office Manager', 'Office Manager'),
            ('Parts Advisor', 'Parts Advisor'),
            ('Parts Manager', 'Parts Manager'),
            ('Receptionist', 'Receptionist'),
            ('Sales Consultant', 'Sales Consultant'),
            ('Sales Manager', 'Sales Manager'),
            ('Service Advisor', 'Service Advisor'),
            ('Service Manager', 'Service Manager'),
            ('Title Clerk', 'Title Clerk'),
            ('Other', 'Other'),
        ]
    )
    birthYear = models.IntegerField(
        max_length=4,
        null=True,
        blank=True,
        validators=[validate_year],
    )
    state = models.CharField(
        max_length=2, 
        blank = True, 
        choices=[
            ('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'), 
            ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'),
            ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('IA', 'IA'),
            ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), ('MD', 'MD'),
            ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'),
            ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'),
            ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'), ('OH', 'OH'),
            ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'),
            ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'),
            ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY')
        ]
    )    
    income = models.CharField(
        max_length=20, 
        blank=True,
        choices=[
            ('Less than $40,000' , 'Less than $40,000'),
            ('$40,000 to $100,000' , '$40,000 to $100,000'),
            ('$100,000 or more' , '$100,000 or more')
        ]
    )
    experience = models.CharField(
        max_length=12,
        blank=True,
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Expert', 'Expert'),
        ]
    )
    hoursOnline = models.CharField(
        max_length=3,
        blank=True,
        choices=[
            ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), 
            ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('10+', '10+'), 
        ]
    )
    educationLevel = models.CharField(
        max_length=15,
        blank=True,
        choices=[
            ('High School', 'High School'),
            ('College', 'College'),
            ('Graduate School', 'Graduate School'),
        ]
    )
    employment = models.CharField(
        max_length=100,
        blank=True,
        choices=[
            ('Employed at home', 'Employed at home'),
            ('Employed in an office', 'Employed in an office'),
            ('Employed outside an office', 'Employed outside an office'),
            ('In school', 'In school'),
            ('Unemployed', 'Unemployed'),
        ]
    )
    participateTime = models.CharField(
        max_length=20,
        blank=True,
        choices=[
            ('Mornings', 'Mornings'),
            ('Afternoons', 'Afternoons'),
            ('Night time', 'Night time'),
        ]
    )
    hashInit = models.CharField(max_length=1000, editable = False)

    def save(self, *args, **kwargs):
        print self.hashInit
        super(FormAPI, self).save(*args, **kwargs)
        if self.hashInit == '':
            self.hashInit = self.createHASH()
            email = EmailMessage(
                "Link to complete application", 
                "Please go to " + base64.urlsafe_b64encode(self.hashInit) +
                "\nto complete your application", 
                to=[self.email]
            )
            email.send()
            formapi = FormAPI.objects.get(pk = self.id)
            formapi.hashInit = self.hashInit
            formapi.save()

    class Meta:
        ordering = ('created',)