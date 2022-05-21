from django.core.validators import RegexValidator
    
class student_no_re(RegexValidator):
    regex = r'^[0-9A-Z]{1,11}$'
    message = 'Student no should only contain digits and uppercase alphabets. Max characters upto 11'

class student_name_re(RegexValidator):
    regex = r'^[^\s]([a-zA-Z]+\s)*([a-zA-Z]*)+[^\s]$'
    message = 'Student name should contain alphabets only with no leading and trailing whitespaces. Only one whitespace in between words is accepted'

class branch_name_re(RegexValidator):
    regex = r'^[^\s]([a-zA-Z&\(\)]+\s)*([a-zA-Z&\(\)]*)+[^\s]$'
    message = 'Branch name should contain alphabets only with no leading and trailing whitespaces. Only one whitespace in between words is accepted. Additionally &,(,) can be used'

class branch_code_re(RegexValidator):
    regex = r'^\d{1,3}$'
    message = 'Branch code should contain digits only max upto 999'