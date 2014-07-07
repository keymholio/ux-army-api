from django.core.validators import RegexValidator , validate_email, EmailValidator
from django.core.exceptions import ValidationError
from django.core.signing import TimestampSigner
from django.core.mail import EmailMessage
from django.db import models
import base64
import datetime
import json
from formAPI import choices

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class FormAPI(models.Model):
    """
    Class for the whole FormAPI
    Includes all model properties which are using validation
    """
    def validate_year(value):
        """
        Used to validate a specific year
        Makes sure the year is within 100 years
        """
        now = datetime.datetime.now()
        if value < (now.year - 100) or value > now.year:
            raise ValidationError('%s is not a valid year' % value)

    def createHASH(self):
        """
        Creates a signed value from the email
        This signed value is based on time that will be checked
        before a put is executed
        """
        initial = {}
        initial['name'] = self.name
        initial['email'] = self.email
        initial['id'] = self.id
        signer = TimestampSigner()
        initial['signed'] = signer.sign(self.email)
        jsonresponse = json.dumps(initial)
        return jsonresponse

    #Created - time created
    created = models.DateTimeField(auto_now_add=True)

    #Owner - superusers
    #owner = models.ForeignKey('auth.User', related_name='formAPIUsers')

    #Name of participant - validated to only include letters and spaces
    #TODO include ' and -
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

    #Email of participant - validated with email regex
    email = models.EmailField(
        max_length = 254, 
        unique=True, 
        error_messages={'unique':"This email has already been registered."}
    )

    #Phone number of participant - validated to include only 10 digits
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

    #Gender of participant - either Male of Female use
    gender = models.CharField(
        max_length=6, 
        blank=True, 
        choices=choices.GENDER_CHOICES
    )

    #Job of participant - can only be on of provided (validated)
    job = models.CharField(
        max_length = 25,
        blank=True,
        choices=choices.JOB_CHOICES
    )

    #Birth year of participant - validated with validate_year and 4 digits
    birthYear = models.IntegerField(
        max_length=4,
        null=True,
        blank=True,
        validators=[validate_year],
    )

    #State the participant resides in - validated against 50 states
    state = models.CharField(
        max_length=2, 
        blank = True, 
        choices=choices.STATE_CHOICES
    )    

    #Income of participant - Must be one of 3 choices
    income = models.CharField(
        max_length=20, 
        blank=True,
        choices=choices.INCOME_CHOICES
    )

    #Experience of participant - Must be one of 3 choices
    experience = models.CharField(
        max_length=12,
        blank=True,
        choices=choices.EXPERIENCE_CHOICES
    )

    #Hours online - Must be 1 of 12 choices
    hoursOnline = models.CharField(
        max_length=3,
        blank=True,
        choices=choices.HOURS_ONLINE_CHOICES
    )

    #Education level of participant
    educationLevel = models.CharField(
        max_length=15,
        blank=True,
        choices=choices.EDUCATION_LEVEL_CHOICES
    )

    #Employment of participant
    employment = models.CharField(
        max_length=100,
        blank=True,
        choices=choices.EMPLOYMENT_CHOICES
    )

    #Time which the participant wishes to participate
    participateTime = models.CharField(
        max_length=20,
        blank=True,
        choices=choices.PARTICIPATE_TIME_CHOICES
    )

    #Hash of email (signed using time)
    hashInit = models.CharField(
        max_length=1000, 
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override of save to make sure hash is created with ID
        Sends email once this is done
        """
        super(FormAPI, self).save(*args, **kwargs)
        if self.hashInit == '':
            self.hashInit = self.createHASH()
            email = EmailMessage(
                "Link to complete application", 
                "Please go to http://127.0.0.1:9000/#/" + base64.urlsafe_b64encode(self.hashInit) +
                "\nto complete your application", 
                to=[self.email]
            )
            email.send()
            formapi = FormAPI.objects.get(pk = self.id)
            formapi.hashInit = self.hashInit
            formapi.save()

    class Meta:
        ordering = ('created',)