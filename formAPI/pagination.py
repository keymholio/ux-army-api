"""
File used override pagination
"""
from rest_framework import pagination
from rest_framework import serializers

class CurrentPageField(serializers.Field):
    """
    Field to return current page
    """
    page_field = 'page'
  
    def to_native(self, value):
        """
        Returns the current page
        """
        current_page_number = value.number
        return current_page_number

class NextPageField(serializers.Field):
    """
    Field to return next page
    """
    page_field = 'page'
  
    def to_native(self, value):
        """
        Returns the next page
        """
        if not value.has_next():
            return None
        next_page_number = value.next_page_number()
        return next_page_number

class PreviousPageField(serializers.Field):
    """
    Field to return prev page
    """
    page_field = 'page'
  
    def to_native(self, value):
        """
        Returns the prev page
        """
        if not value.has_previous():
            return None
        previous_page_number = value.previous_page_number()
        return previous_page_number

class CustomPaginationSerializer(pagination.BasePaginationSerializer):
    """
    Pagination for formAPi
    """
    count = serializers.Field(source='paginator.count')
    next = pagination.NextPageField(source='*')
    previous = pagination.PreviousPageField(source='*')
    page = CurrentPageField(source='*')
    next_page = NextPageField(source='*')
    previous_page = PreviousPageField(source='*')
