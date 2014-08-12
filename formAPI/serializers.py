"""
Serializers for the models used in the API
"""
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from rest_framework import serializers
from formAPI.models import FormAPI, Task, Event
from formAPI import choices
import datetime


class UserSerializer(serializers.ModelSerializer):
    """
    Main serializer for the user model
    """
    snippets = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        """
        Serializes the user
        Sets the password to write only
        """
        model = User
        fields = \
            ('id', 'username', 'password', 'first_name', 'last_name', 'email', )
        write_only_fields = ('password',)

    def restore_object(self, attrs, instance=None):
        """
        Used to set password and return the user
        """
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user


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
            'id', 'created',
            'name', 'email', 'phone', 'gender', 'job', 'birthYear', 'state',
            'income', 'experience', 'hoursOnline', 'educationLevel',
            'employment', 'participateTime',  'completed_initial', 'participant'
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
        choices=choices.GENDER_CHOICES
    )
    job = serializers.ChoiceField(
        choices=choices.JOB_CHOICES
    )
    birthYear = serializers.IntegerField(
        validators=[validate_year],
    )
    state = serializers.ChoiceField(
        choices=choices.STATE_CHOICES
    )
    income = serializers.ChoiceField(
        choices=choices.INCOME_CHOICES
    )
    experience = serializers.ChoiceField(
        choices=choices.EXPERIENCE_CHOICES
    )
    hoursOnline = serializers.ChoiceField(
        choices=choices.HOURS_ONLINE_CHOICES
    )
    educationLevel = serializers.ChoiceField(
        choices=choices.EDUCATION_LEVEL_CHOICES
    )
    employment = serializers.ChoiceField(
        choices=choices.EMPLOYMENT_CHOICES
    )
    participateTime = serializers.ChoiceField(
        choices=choices.PARTICIPATE_TIME_CHOICES
    )
    completed_initial = serializers.BooleanField(
        default=True
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
            instance.hoursOnline = \
                attrs.get('hoursOnline', instance.hoursOnline)
            instance.educationLevel = \
                attrs.get('educationLevel', instance.educationLevel)
            instance.employment = \
                attrs.get('employment', instance.employment)
            instance.participateTime = \
                attrs.get('participateTime', instance.participateTime)
            instance.completed_initial = \
                attrs.get('completed_initial', instance.completed_initial)
            return instance
        return FormAPI(**attrs)


class FormAPI_Serializer_Put_Validated(serializers.Serializer):
    """
    Used as put serializer, with validation to require information
    """
    id = serializers.Field()
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Phone number must be numeric',
                code='Invalid phone'
            ),
        ],
        required=False
    )
    gender = serializers.ChoiceField(
        choices=choices.GENDER_CHOICES,
        required=False
    )
    job = serializers.ChoiceField(
        choices=choices.JOB_CHOICES,
        required=False
    )
    birthYear = serializers.IntegerField(
        validators=[validate_year],
        required=False
    )
    state = serializers.ChoiceField(
        choices=choices.STATE_CHOICES,
        required=False
    )
    income = serializers.ChoiceField(
        choices=choices.INCOME_CHOICES,
        required=False
    )
    experience = serializers.ChoiceField(
        choices=choices.EXPERIENCE_CHOICES,
        required=False
    )
    hoursOnline = serializers.ChoiceField(
        choices=choices.HOURS_ONLINE_CHOICES,
        required=False
    )
    educationLevel = serializers.ChoiceField(
        choices=choices.EDUCATION_LEVEL_CHOICES,
        required=False
    )
    employment = serializers.ChoiceField(
        choices=choices.EMPLOYMENT_CHOICES,
        required=False
    )
    participateTime = serializers.ChoiceField(
        choices=choices.PARTICIPATE_TIME_CHOICES,
        required=False
    )
    completed_initial = serializers.BooleanField(
        default=False
    )

    def restore_object(self, attrs, instance=None):
        """
        Will be used to update the model when auth
        Allows to update only a few or all fields
        Name and email can be updated
        """
        attrs['completed_initial'] = False
        if ((instance.name != "" and 'name' not in attrs) or\
        ('name' in attrs and attrs['name'] != "")) and\
        ((instance.email != "" and 'email' not in attrs) or\
        ('email' in attrs and attrs['email'] != "")) and\
        ((instance.phone != "" and 'phone' not in attrs) or\
        ('phone' in attrs and attrs['phone'] != "")) and\
        ((instance.gender != "" and 'gender' not in attrs) or\
        ('gender' in attrs and attrs['gender'] != "")) and\
        ((instance.job != "" and 'job' not in attrs) or\
        ('job' in attrs and attrs['job'] != "")) and\
        ((instance.birthYear != None and 'birthYear' not in attrs) or\
        ('birthYear' in attrs and attrs['birthYear'] != None)) and\
        ((instance.state != "" and 'state' not in attrs) or\
        ('state' in attrs and attrs['state'] != "")) and\
        ((instance.income != "" and 'income' not in attrs) or\
        ('income' in attrs and attrs['income'] != "")) and\
        ((instance.experience != "" and 'experience' not in attrs) or\
        ('experience' in attrs and attrs['experience'] != "")) and\
        ((instance.hoursOnline != "" and 'hoursOnline' not in attrs) or\
        ('hoursOnline' in attrs and attrs['hoursOnline'] != ""))and\
        ((instance.educationLevel != "" and 'educationLevel' not in attrs) or\
        ('educationLevel' in attrs and attrs['educationLevel'] != "")) and\
        ((instance.employment != "" and 'employment' not in attrs) or\
        ('employment' in attrs and attrs['employment'] != ""))and\
        ((instance.participateTime != "" and 'participateTime' not in attrs) or\
        ('participateTime' in attrs and attrs['participateTime'] != "")):
            attrs['completed_initial'] = True
        if instance:
            instance.name = attrs.get('name', instance.name)
            instance.email = attrs.get('email', instance.email)
            instance.phone = attrs.get('phone', instance.phone)
            instance.gender = attrs.get('gender', instance.gender)
            instance.job = attrs.get('job', instance.job)
            instance.birthYear = attrs.get('birthYear', instance.birthYear)
            instance.state = attrs.get('state', instance.state)
            instance.income = attrs.get('income', instance.income)
            instance.experience = attrs.get('experience', instance.experience)
            instance.hoursOnline = \
                attrs.get('hoursOnline', instance.hoursOnline)
            instance.educationLevel = \
                attrs.get('educationLevel', instance.educationLevel)
            instance.employment = \
                attrs.get('employment', instance.employment)
            instance.participateTime = \
                attrs.get('participateTime', instance.participateTime)
            instance.completed_initial = \
                attrs.get('completed_initial', instance.completed_initial)
            return instance
        return FormAPI(**attrs)


class TaskSerializer(serializers.ModelSerializer):
    events = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('title', 'description', 'is_active', 'events')

class EventSerializer(serializers.ModelSerializer):
    DATE_INPUT_FORMATS = [
        '%m/%d/%Y', '%m/%d/%y', 
        '%b %d %Y', '%b %d, %Y',
        '%B %d %Y', '%B %d, %Y',
        '%Y-%m-%d'
    ]
    date = serializers.DateField(
        input_formats=DATE_INPUT_FORMATS
    )
    time = serializers.TimeField(
        input_formats=[
            '%I:%M %p', '%I%p',
            '%I:%M%p', '%I %p',
        ]
    )
    class Meta:
        model = Event
        fields = ('task', 'participant', 'date', 'time', 'created')
