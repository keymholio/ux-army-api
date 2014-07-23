from django.test import TestCase
from serializers import validate_year
from serializers import FormAPI_Serializer_Put
import mock
import unittest
from django.core.exceptions import ValidationError
from datetime import datetime

class SerializerTests(TestCase):
	def setUp(self):
		instance = mock.MagicMock()
		self = mock.MagicMock()
	def test_validate_year_test_too_old(self):
		self.assertRaises(ValidationError, validate_year, 1800)
	def test_validate_year_test_too_young(self):
		self.assertRaises(ValidationError, validate_year, (datetime.now().year + 1))
	def test_validate_year_test_pass(self):
		validate_year(datetime.now().year - 18)
	
class FormAPI_Serializer_Put_tests(TestCase):
	def setUp(self):
		self.sso = FormAPI_Serializer_Put()
	def test_validate_restore_object_blank_instance(self):
		# self.sso = mock.MagicMock()
		attrs = {
			'educationLevel': 'College', 
			'hoursOnline': '10', 
			'name': 'Elizabeth', 
			'birthYear': 1990, 
			'participateTime': 'Afternoons', 
			'gender': 'Female', 
			'state': 'NY', 
			'experience': 'Intermediate', 
			'phone': '6541239870', 
			'job': 'Internet Director', 
			'income': '$100,000 or more', 
			'employment': 'Employed at home', 
			'email': 'elizabeth@someemail.com'
		}
		response = self.sso.restore_object(attrs,) #instance = mock.MagicMock())
		self.assertEquals(response.educationLevel, 'College')
		self.assertEquals(response.hoursOnline, '10')
		self.assertEquals(response.birthYear, 1990)
		self.assertEquals(response.participateTime, 'Afternoons')
		self.assertEquals(response.state, 'NY')
		self.assertEquals(response.gender, 'Female')
		self.assertEquals(response.experience, 'Intermediate')
		self.assertEquals(response.phone, '6541239870')
		self.assertEquals(response.job, 'Internet Director')
		self.assertEquals(response.income, '$100,000 or more')
		self.assertEquals(response.employment, 'Employed at home')
		self.assertEquals(response.email, 'elizabeth@someemail.com')

	def test_validate_restore_object_nonblank_instance(self):
		attrs = {
			'educationLevel': 'College', 
			'hoursOnline': '10', 
			'name': 'Elizabeth', 
			'birthYear': 1990, 
			'participateTime': 'Afternoons', 
			'gender': 'Female', 
			'state': 'NY', 
			'experience': 'Intermediate', 
			'phone': '6541239870', 
			'job': 'Internet Director', 
			'income': '$100,000 or more', 
			'employment': 'Employed at home', 
			'email': 'elizabeth@someemail.com'
		}
		response = self.sso.restore_object(attrs, instance = mock.MagicMock())
		self.assertEquals(response.educationLevel, 'College')
		self.assertEquals(response.hoursOnline, '10')
		self.assertEquals(response.birthYear, 1990)
		self.assertEquals(response.participateTime, 'Afternoons')
		self.assertEquals(response.state, 'NY')
		self.assertEquals(response.gender, 'Female')
		self.assertEquals(response.experience, 'Intermediate')
		self.assertEquals(response.phone, '6541239870')
		self.assertEquals(response.job, 'Internet Director')
		self.assertEquals(response.income, '$100,000 or more')
		self.assertEquals(response.employment, 'Employed at home')