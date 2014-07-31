"""
File used to specify various choices
Used for /choices/ endpoint 
"""
import datetime

YEAR_RANGE = 101
GENDER_CHOICES = [
    ('Female', 'Female'),
    ('Male', 'Male'),
]

JOB_CHOICES = [
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

STATE_CHOICES = [
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

INCOME_CHOICES = [
    ('Less than $40,000', 'Less than $40,000'),
    ('$40,000 to $100,000', '$40,000 to $100,000'),
    ('$100,000 or more', '$100,000 or more')
]

EXPERIENCE_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Expert', 'Expert'),
]

HOURS_ONLINE_CHOICES = [
    ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), 
    ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), 
    ('10+', '10+'), 
]

EDUCATION_LEVEL_CHOICES = [
    ('High School', 'High School'),
    ('College', 'College'),
    ('Graduate School', 'Graduate School'),
]

EMPLOYMENT_CHOICES = [
    ('Employed at home', 'Employed at home'),
    ('Employed in an office', 'Employed in an office'),
    ('Employed outside an office', 'Employed outside an office'),
    ('In school', 'In school'),
    ('Unemployed', 'Unemployed'),
]

PARTICIPATE_TIME_CHOICES = [
    ('Mornings', 'Mornings'),
    ('Afternoons', 'Afternoons'),
    ('Night time', 'Night time'),
]
    
def get_choices():
    """
    Getting json resposne ready
    """
    all_choices = [
        GENDER_CHOICES,
        JOB_CHOICES,
        STATE_CHOICES,
        INCOME_CHOICES,
        EXPERIENCE_CHOICES,
        HOURS_ONLINE_CHOICES,
        EDUCATION_LEVEL_CHOICES,
        EMPLOYMENT_CHOICES,
        PARTICIPATE_TIME_CHOICES
    ]
    var_choices = [
        'genderChoices',
        'jobChoices',
        'stateChoices',
        'incomeChoices',
        'experienceChoices',
        'hoursOnlineChoices',
        'educationLevelChoices',
        'employmentChoices',
        'participateTimeChoices'
    ]
    response = {
        'genderChoices': [],
        'jobChoices': [],
        'stateChoices': [],
        'incomeChoices': [],
        'experienceChoices': [],
        'hoursOnlineChoices': [],
        'educationLevelChoices': [],
        'employmentChoices': [],
        'participateTimeChoices': [],
        'birthYearChoices': [],
    }
    count = 0
    for choice in all_choices:
        for option in choice:
            response[var_choices[count]].append(option[0])
        count += 1
    now = datetime.datetime.now()
    response['birthYearChoices'].append('')
    for years_to_subtract in range(YEAR_RANGE):
        response['birthYearChoices'].append(now.year - years_to_subtract)
    return response
