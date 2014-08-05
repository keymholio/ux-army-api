"""
Main model class for the participants
"""
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import models
from formAPI import choices
import datetime
import hashlib
import json

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
        Creates a hashed value to check
        """
        initial = {}
        initial['name'] = self.name
        initial['email'] = self.email
        initial['id'] = self.id
        jsonresponse = json.dumps(initial)
        return jsonresponse

    #Created - time created
    created = models.DateTimeField(auto_now_add=True)

    #Name - name of participants
    name = models.CharField(
        max_length=100,
    )

    #Email of participant - validated with email regex
    email = models.EmailField(
        max_length=254, 
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
        max_length=25,
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
        blank=True, 
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

    #Has completed inital sign up
    completed_initial = models.BooleanField(
        default=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override of save to make sure hash is created with ID
        Sends email once this is done
        """
        super(FormAPI, self).save(*args, **kwargs)
        if self.hashInit == '':
            hasher = hashlib.sha512()
            hasher.update(self.createHASH())
            self.hashInit = hasher.hexdigest()
            formapi = FormAPI.objects.get(pk = self.id)
            formapi.hashInit = self.hashInit
            formapi.save()
            email = EmailMessage(
                to=[self.email]
            )
            email.template_name = "confirmation email"
            link = self.hashInit
            email.global_merge_vars = {'URL': link}
            email.use_template_subject = True
            email.use_template_from = True
            email.send()

    class Meta:
        ordering = ('created',)
