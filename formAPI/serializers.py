from django.contrib.auth.models import User
from django.core.validators import RegexValidator , validate_email, EmailValidator
from django.core.exceptions import ValidationError
from django.forms import widgets
from formAPI.models import FormAPI
from rest_framework import serializers
import datetime


class FormAPI_Serializer(serializers.HyperlinkedModelSerializer):
    """
    Initial serializer, default
    Will be used for post data
    Saves the initial model to DB
    """
    formAPIUsers = serializers.PrimaryKeyRelatedField(many=True)
    class Meta:
        model = FormAPI
        fields = (
            'id','created',
            'name', 'email', 'phone','gender','job','birthYear', 'state', 'income',
            'experience','hoursOnline','educationLevel','employment', 'participateTime',
        )

def validate_year(value):
    """
    Used to validate the year once a put is sent
    """
    now = datetime.datetime.now()
    if value < (now.year - 100) or value > now.year:
        raise ValidationError('%s is not a valid year' % value)

class FormAPI_Serializer_Put(serializers.Serializer):
    """
    Used as put serializer, with validation to require information
    """
    id = serializers.Field()
    phone = serializers.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Phone number must be numeric',
                code='Invalid phone'
            ),
        ]
    )
    gender = serializers.ChoiceField(
        choices=[
            ('Male' , 'Male'),
            ('Female' , 'Female')
        ],
    )
    job = serializers.ChoiceField(
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
    birthYear = serializers.IntegerField(
        validators=[validate_year],
    )
    state = serializers.ChoiceField(
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
    income = serializers.ChoiceField(
        choices=[
            ('Less than $40,000' , 'Less than $40,000'),
            ('$40,000 to $100,000' , '$40,000 to $100,000'),
            ('$100,000 or more' , '$100,000 or more')
        ]
    )
    experience = serializers.ChoiceField(
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Expert', 'Expert'),
        ]
    )
    hoursOnline = serializers.ChoiceField(
        choices=[
            ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), 
            ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('10+', '10+'), 
        ]
    )
    educationLevel = serializers.ChoiceField(
        choices=[
            ('High School', 'High School'),
            ('College', 'College'),
            ('Graduate School', 'Graduate School'),
        ]
    )
    employment = serializers.ChoiceField(
        choices=[
            ('Employed at home', 'Employed at home'),
            ('Employed in an office', 'Employed in an office'),
            ('Employed outside an office', 'Employed outside an office'),
            ('In school', 'In school'),
            ('Unemployed', 'Unemployed'),
        ]
    )
    participateTime = serializers.ChoiceField(
        choices=[
            ('Mornings', 'Mornings'),
            ('Afternoons', 'Afternoons'),
            ('Night time', 'Night time'),
        ]
    )
    def restore_object(self, attrs, instance=None):
        """
        Will be used to update the model
        """
        if instance:
            instance.phone = attrs.get('phone', instance.phone)
            instance.gender = attrs.get('gender', instance.gender)
            instance.job = attrs.get('job', instance.job)
            instance.birthYear = attrs.get('birthYear', instance.birthYear)
            instance.state = attrs.get('state', instance.state)
            instance.income = attrs.get('income', instance.income)
            instance.experience = attrs.get('experience', instance.experience)
            instance.hoursOnline = attrs.get('hoursOnline', instance.hoursOnline)
            instance.educationLevel = attrs.get('educationLevel', instance.educationLevel)
            instance.employment = attrs.get('employment', instance.employment)
            instance.participateTime = attrs.get('participateTime', instance.participateTime)
            return instance
        return FormAPI(**attrs)