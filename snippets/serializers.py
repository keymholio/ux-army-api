from django.forms import widgets
from rest_framework import serializers
from snippets.models import Snippet
from django.contrib.auth.models import User
from django.core.validators import RegexValidator , validate_email, EmailValidator
from django.core.exceptions import ValidationError
import datetime


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.Field(source='owner.username')

    class Meta:
        model = Snippet
        fields = (
            'id','created', 
            'name', 'email', 'phone','gender','job','birthYear', 'state', 'income',
            'experience','hoursOnline','educationLevel','employment', 'participateTime',
        )

# class SnippetSerializer2(serializers.HyperlinkedModelSerializer):
#     # owner = serializers.Field(source='owner.username')

#     class Meta:
#         model = Snippet1
#         fields = (
#             'id','created', 
#             'name', 'email', 'phone','gender','job','birthYear', 'state', 'income',
#             'experience','hoursOnline','educationLevel','employment', 'participateTime',
#         )
def validate_year(value):
    	now = datetime.datetime.now()
        if value < (now.year - 100) or value > now.year:
            raise ValidationError('%s is not a valid year' % value)

# class SnippetSerializer(serializers.Serializer):
#     id = serializers.Field()  # Note: `Field` is an untyped read-only field.
#     name = serializers.CharField(max_length=100)
#     email = serializers.CharField(max_length=100000)
#     phone = serializers.CharField(required=False, max_length=100)
#     gender = serializers.CharField(required=False, max_length=100000)
#     job = serializers.CharField(required=False, max_length=100)
#     birthYear = serializers.IntegerField(required=False)
#     state = serializers.CharField(required=False, max_length=100)
#     income = serializers.CharField(required=False, max_length=100000)
#     experience = serializers.CharField(required=False, max_length=100)
#     hoursOnline = serializers.CharField(required=False, max_length=100000)
#     educationLevel = serializers.CharField(required=False, max_length=100)
#     employment = serializers.CharField(required=False, max_length=100000)
#     participateTime = serializers.CharField(required=False, max_length=100)

#     def restore_object(self, attrs, instance=None):
#         """
#         Create or update a new snippet instance, given a dictionary
#         of deserialized field values.

#         Note that if we don't define this method, then deserializing
#         data will simply return a dictionary of items.
#         """
#         if instance:
#             # Update existing instance
#             instance.name = attrs.get('name', instance.name)
#             instance.email = attrs.get('email', instance.email)
#             instance.phone = attrs.get('phone', instance.phone)
#             instance.gender = attrs.get('gender', instance.gender)
#             instance.job = attrs.get('job', instance.job)
#             instance.birthYear = attrs.get('birthYear', instance.birthYear)
#             instance.state = attrs.get('state', instance.state)
#             instance.income = attrs.get('income', instance.income)
#             instance.experience = attrs.get('experience', instance.experience)
#             instance.hoursOnline = attrs.get('hoursOnline', instance.hoursOnline)
#             instance.educationLevel = attrs.get('educationLevel', instance.educationLevel)
#             instance.employment = attrs.get('employment', instance.employment)
#             instance.participateTime = attrs.get('participateTime', instance.participateTime)
#             return instance

#         # Create new instance
#         return Snippet(**attrs)

class SnippetSerializer_other(serializers.Serializer):
	
    id = serializers.Field()  # Note: `Field` is an untyped read-only field.
    name = serializers.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z ]*$',
                message='Name must consist of characters A-Z and/or a-z',
                code='Invalid Name'
            ),
        ]
    )
    email = serializers.CharField(
        max_length=100,
        validators=[
            EmailValidator(),
        ]
    )
    phone = serializers.CharField(
        max_length=10,
        #blank=True,
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
        # max_length=20, 
        # blank=True,
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
        Create or update a new snippet instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            # Update existing instance
            instance.name = attrs.get('name', instance.name)
            instance.email = attrs.get('email', instance.email)
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

        # Create new instance
        return Snippet(**attrs)