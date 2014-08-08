"""
Test file for API
"""
from django.contrib.auth.models import User
from formAPI.models import FormAPI
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
import json

class AccountTests(APITestCase):
    def test_choices(self):
        self.client = APIClient()
        response = self.client.get('/choices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
        	{"experienceChoices": ["Beginner", "Intermediate", "Expert"], \
        	"educationLevelChoices": ["High School", "College", "Graduate School"],\
        	 "genderChoices": ["Female", "Male"], \
        	 "hoursOnlineChoices": ["0", "1", "2", "3", "4", "5", \
        	 "6", "7", "8", "9", "10", "10+"], \
        	 "stateChoices": ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE",\
        	  "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",\
        	   "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",\
        	    "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",\
        	     "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"], \
        	     "birthYearChoices": [2014, 2013, 2012, 2011, 2010, 2009, 2008, \
        	     2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997,\
	      1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986,\
	       1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975,\
	        1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966, 1965, 1964,\
	         1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954,\
	          1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944,\
	           1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935,\
	            1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926,\
	             1925, 1924, 1923, 1922, 1921, 1920, 1919, 1918, 1917,\
	              1916, 1915, 1914], \
	              "participateTimeChoices": ["Mornings", "Afternoons", \
	              "Night time"],\
	               "jobChoices": ["BDC Manager", "Controller", \
	               "Dealertrack Employee",\
	                "Entry Level Technician", "F&I Director", \
	                "F&I Manager", "Fixed Operations Director",\
	                 "General Manager", "Internet Director", \
	                 "Office Manager", "Parts Advisor", \
	                 "Parts Manager", "Receptionist", \
	                 "Sales Consultant", "Sales Manager", \
	                 "Service Advisor", "Service Manager", \
	                 "Title Clerk", "Other"], \
	                 "employmentChoices": ["Employed at home", \
	                 "Employed in an office", \
	                 "Employed outside an office", "In school", \
	                 "Unemployed"], \
	                 "incomeChoices": ["Less than $40,000", \
	                 "$40,000 to $100,000", "$100,000 or more"]}
        )
        

class ParticipantListTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.post('/api/', 
                {
                    "name" : "victor",
                    "email" : "victor@email.com",
                    'educationLevel' : 'College', 
                    'hoursOnline': '10', 
                    'birthYear': 1990, 
                    'participateTime': 'Afternoons', 
                    'gender': 'Male', 
                    'state': 'NY', 
                    'experience': 'Intermediate', 
                    'phone': '5556664444', 
                    'job': 'Internet Director', 
                    'income': '$100,000 or more', 
                    'employment': 'Employed at home'
                }
            )
        self.client.post('/api/', 
                {
                    "name" : "mark",
                    "email" : "mark@email.com",
                }
            )
        self.user = User.objects.create_user(
            username='test_user', email='test_email', password='test_pw')

    def test_check_valid_sign_up_bad(self):
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user, token=None)
        self.client.put('/api/1/', {'gender': 'Male'})
        get_hash = FormAPI.objects.get(email = 'victor@email.com').hashInit
        response = self.client.post('/demo-form-check/',
            {
                "hashed" : get_hash
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_valid_sign_up_good(self):
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user, token=None)
        get_hash = FormAPI.objects.get(email = 'mark@email.com').hashInit
        response = self.client.post('/demo-form-check/',
            {
                "hashed" : get_hash
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incorrect_login_token(self):
        response = self.client.post('/login/', 
                {
                    'username' : 'incorrect_user',
                    'password' : 'incorrect_pass'
                }
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_token(self):
        response = self.client.post('/login/', 
                {
                    'username' : 'test_user',
                    'password' : 'test_pw'
                }
            )
        self.assertIsNotNone(json.loads(response.content)['token'])

    def test_login_and_logout(self):
        response = self.client.post('/login/', 
                {
                    'username' : 'test_user',
                    'password' : 'test_pw'
                }
            )
        self.assertIsNotNone(json.loads(response.content)['token'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = json.loads(response.content)['token']
        user = User.objects.filter(auth_token=token)
        self.assertTrue(user.count() == 1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response_logout = self.client.post('/logout/')
        user = User.objects.filter(auth_token=token)
        self.client.credentials()
        self.assertTrue(user.count() == 0)
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)

    def test_put_on_empty(self):
        response = self.client.put('/api/12/', 
            {
                "name" : "mark",
                "email" : "mark@email.com",
                'educationLevel' : 'College', 
                'hoursOnline': '5', 
                'birthYear': 1950, 
                'participateTime': 'Mornings', 
                'gender': 'Male', 
                'state': 'CA', 
                'experience': 'Expert', 
                'phone': '5552224444', 
                'job': 'Controller', 
                'income': 'Less than $40,000', 
                'employment': 'Unemployed'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((json.loads(response.content))['educationLevel'], 'College')
        self.assertEqual((json.loads(response.content))['hoursOnline'], '5')
        self.assertEqual((json.loads(response.content))['birthYear'], 1950)
        self.assertEqual((json.loads(response.content))['participateTime'], 'Mornings')
        self.assertEqual((json.loads(response.content))['gender'], 'Male')
        self.assertEqual((json.loads(response.content))['state'], 'CA')
        self.assertEqual((json.loads(response.content))['experience'], 'Expert')
        self.assertEqual((json.loads(response.content))['phone'], '5552224444')
        self.assertEqual((json.loads(response.content))['job'], 'Controller')
        self.assertEqual((json.loads(response.content))['income'], 'Less than $40,000')
        self.assertEqual((json.loads(response.content))['employment'], 'Unemployed')

    def test_put_on_not_empty(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.put('/api/14/', 
            {
                "name" : "mark",
                "email" : "mark@email.com",
                'educationLevel' : 'College', 
                'hoursOnline': '5', 
                'birthYear': 1950, 
                'participateTime': 'Mornings', 
                'gender': 'Male', 
                'state': 'CA', 
                'experience': 'Expert', 
                'phone': '5552223333', 
                'job': 'Controller', 
                'income': 'Less than $40,000', 
                'employment': 'Unemployed'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/api/14/', 
            {
                "name" : "mark",
                "email" : "mark@email.com",
                'educationLevel' : 'College', 
                'hoursOnline': '5', 
                'birthYear': 1950, 
                'participateTime': 'Mornings', 
                'gender': 'Male', 
                'state': 'CA', 
                'experience': 'Expert', 
                'phone': '5552223333', 
                'job': 'Controller', 
                'income': 'Less than $40,000', 
                'employment': 'Unemployed'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_on_not_empty_auth(self):
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user, token=None)
        response = self.client.put('/api/16/', 
            {
                "name" : "mark",
                "email" : "mark@email.com",
                'educationLevel' : 'College', 
                'hoursOnline': '5', 
                'participateTime': 'Mornings', 
                'gender': 'Male', 
                'state': 'CA', 
                'experience': 'Expert', 
                'phone': '5552223333', 
                'job': 'Controller', 
                'income': 'Less than $40,000', 
                'employment': 'Unemployed'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/api/16/', 
            {
                'birthYear': 1950, 
                'gender': 'Female', 
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((json.loads(response.content))['name'], 'mark')
        self.assertEqual((json.loads(response.content))['email'], 'mark@email.com')
        self.assertEqual((json.loads(response.content))['educationLevel'], 'College')
        self.assertEqual((json.loads(response.content))['hoursOnline'], '5')
        self.assertEqual((json.loads(response.content))['participateTime'], 'Mornings')
        self.assertEqual((json.loads(response.content))['gender'], 'Female')
        self.assertEqual((json.loads(response.content))['state'], 'CA')
        self.assertEqual((json.loads(response.content))['experience'], 'Expert')
        self.assertEqual((json.loads(response.content))['phone'], '5552223333')
        self.assertEqual((json.loads(response.content))['job'], 'Controller')
        self.assertEqual((json.loads(response.content))['income'], 'Less than $40,000')
        self.assertEqual((json.loads(response.content))['employment'], 'Unemployed')
        self.assertEqual((json.loads(response.content))['birthYear'],  1950)
        self.assertEqual((json.loads(response.content))['completed_initial'], True)

    def test_validate_delete(self):
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user, token=None)
        response = self.client.get('/api/')
        original_count = json.loads(response.content)['count']
        delete_response = self.client.delete('/api/17/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/api/')
        count_after_delete = json.loads(response.content)['count']
        self.assertEqual(count_after_delete, (original_count - 1))

    def test_validate_forced_auth_participant_list(self):
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user, token=None)
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((json.loads(response.content))['results'][1]['name'], 'victor')
        self.assertEqual((json.loads(response.content))['results'][1]['email'], 'victor@email.com')
        self.assertEqual((json.loads(response.content))['results'][1]['educationLevel'], 'College')
        self.assertEqual((json.loads(response.content))['results'][1]['hoursOnline'], '10')
        self.assertEqual((json.loads(response.content))['results'][1]['birthYear'], 1990)
        self.assertEqual((json.loads(response.content))['results'][1]['participateTime'], 'Afternoons')
        self.assertEqual((json.loads(response.content))['results'][1]['gender'], 'Male')
        self.assertEqual((json.loads(response.content))['results'][1]['state'], 'NY')
        self.assertEqual((json.loads(response.content))['results'][1]['experience'], 'Intermediate')
        self.assertEqual((json.loads(response.content))['results'][1]['phone'], '5556664444')
        self.assertEqual((json.loads(response.content))['results'][1]['job'], 'Internet Director')
        self.assertEqual((json.loads(response.content))['results'][1]['income'], '$100,000 or more')
        self.assertEqual((json.loads(response.content))['results'][1]['employment'], 'Employed at home')

    def test_validate_forced_auth_user_list(self):
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user, token=None)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((json.loads(response.content))[0]['username'], 'test_user')
        self.assertEqual((json.loads(response.content))[0]['first_name'], '')
        self.assertEqual((json.loads(response.content))[0]['last_name'], '')
        self.assertEqual((json.loads(response.content))[0]['email'], 'test_email')

    def test_validate_forced_auth_participant_specific_no_auth(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get('/api/11/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_validate_forced_auth_participant_specific_with_auth(self):
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user, token=None)
        response = self.client.get('/api/23/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((json.loads(response.content))['name'], 'victor')
        self.assertEqual((json.loads(response.content))['email'], 'victor@email.com')
        self.assertEqual((json.loads(response.content))['educationLevel'], 'College')
        self.assertEqual((json.loads(response.content))['hoursOnline'], '10')
        self.assertEqual((json.loads(response.content))['birthYear'], 1990)
        self.assertEqual((json.loads(response.content))['participateTime'], 'Afternoons')
        self.assertEqual((json.loads(response.content))['gender'], 'Male')
        self.assertEqual((json.loads(response.content))['state'], 'NY')
        self.assertEqual((json.loads(response.content))['experience'], 'Intermediate')
        self.assertEqual((json.loads(response.content))['phone'], '5556664444')
        self.assertEqual((json.loads(response.content))['job'], 'Internet Director')
        self.assertEqual((json.loads(response.content))['income'], '$100,000 or more')
        self.assertEqual((json.loads(response.content))['employment'], 'Employed at home')

    def test_validate_initial_input_empty(self):
        participant = FormAPI.objects.get(email='mark@email.com')
        self.assertEqual(participant.name, 'mark')
        self.assertEqual(participant.email, 'mark@email.com')
        self.assertEqual(participant.educationLevel, '')
        self.assertEqual(participant.hoursOnline, '')
        self.assertEqual(participant.birthYear, None)
        self.assertEqual(participant.participateTime, '')
        self.assertEqual(participant.gender, '')
        self.assertEqual(participant.state, '')
        self.assertEqual(participant.experience, '')
        self.assertEqual(participant.phone, '')
        self.assertEqual(participant.job, '')
        self.assertEqual(participant.income, '')
        self.assertEqual(participant.employment, '')
        self.assertIsNotNone(participant.hashInit)
        self.assertIsNotNone(participant.created)

    def test_validate_initial_input_filled(self):
        participant = FormAPI.objects.get(email='victor@email.com')
        self.assertEqual(participant.name, 'victor')
        self.assertEqual(participant.email, 'victor@email.com')
        self.assertEqual(participant.educationLevel, 'College')
        self.assertEqual(participant.hoursOnline, '10')
        self.assertEqual(participant.birthYear, 1990)
        self.assertEqual(participant.participateTime, 'Afternoons')
        self.assertEqual(participant.gender, 'Male')
        self.assertEqual(participant.state, 'NY')
        self.assertEqual(participant.experience, 'Intermediate')
        self.assertEqual(participant.phone, '5556664444')
        self.assertEqual(participant.job, 'Internet Director')
        self.assertEqual(participant.income, '$100,000 or more')
        self.assertEqual(participant.employment, 'Employed at home')
        self.assertIsNotNone(participant.hashInit)
        self.assertIsNotNone(participant.created)

    def test_validate_unauthorized_participant_list(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_validate_unauthorized_user_list(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_validate_unauthorized_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token BADTOKEN')
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content)['detail'],
            'Invalid token'
        )

    def test_validating_filters(self):
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user, token=None)
        self.client.post('/api/', 
                {
                    "name" : "emily",
                    "email" : "emily@email.com",
                    'educationLevel' : 'High School', 
                    'hoursOnline': '5', 
                    'birthYear': 1995, 
                    'participateTime': 'Afternoons', 
                    'gender': 'Female', 
                    'state': 'CA', 
                    'experience': 'Beginner', 
                    'phone': '1234567890', 
                    'job': 'Controller', 
                    'income': '$100,000 or more', 
                    'employment': 'Employed at home'
                }
            )

        self.client.post('/api/', 
                {
                    "name" : "john",
                    "email" : "john@email.com",
                    'educationLevel' : 'Graduate School', 
                    'hoursOnline': '9', 
                    'birthYear': 1982, 
                    'participateTime': 'Mornings', 
                    'gender': 'Female', 
                    'state': 'NY', 
                    'experience': 'Expert', 
                    'phone': '1234567890', 
                    'job': 'Controller', 
                    'income': 'Less than $40,000', 
                    'employment': 'Unemployed'
                }
            )

        self.client.post('/api/', 
                {
                    "name" : "john",
                    "email" : "john1@email.com",
                    'educationLevel' : 'Graduate School', 
                    'hoursOnline': '9', 
                    'birthYear': 1982, 
                    'participateTime': 'Mornings', 
                    'gender': 'Female', 
                    'state': 'CA', 
                    'experience': 'Expert', 
                    'phone': '1234567890', 
                    'job': 'Controller', 
                    'income': 'Less than $40,000', 
                    'employment': 'Unemployed'
                }
            )
        response_state = json.loads(self.client.get('/api/?state=NY').content)
        self.assertEqual(response_state['count'], 2)
        response_state = json.loads(
            self.client.get(
                '/api/?state=NY&educationLevel=Graduate+School').content)
        self.assertEqual(response_state['count'], 1)
        response_state = json.loads(self.client.get(
            '/api/?experience=Expert').content)
        self.assertEqual(response_state['count'], 2)