"""
Serializers for the models used in the API
"""
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from formAPI.models import FormAPI
from formAPI import choices
from rest_framework import serializers
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
            ('id', 'username', 'password', 'first_name', 'last_name', 'email')
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
            'employment', 'participateTime',
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
            return instance
        return FormAPI(**attrs)