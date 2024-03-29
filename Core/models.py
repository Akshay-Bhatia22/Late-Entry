from django.db import models
from Auth.models import User

class Operator(User):

    class Meta:
        proxy=True

class Venue(models.Model):
    venue = models.CharField(max_length=255)


class Year(models.Model):
    class year_choices(models.IntegerChoices):
        First = 1 , ('1st year')
        Second = 2, ('2nd year')
        Third = 3, ('3rd year')
        Forth = 4, ('4th year')
    value = models.IntegerField(choices=year_choices.choices)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.get_value_display())

    class Meta:
        ordering = ['value',]

class Branch(models.Model):
    name = models.CharField(max_length=10, null=False)
    active = models.BooleanField(default=True)
    code = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Branches'

class Student(models.Model):
    st_no = models.CharField(primary_key=True, max_length=11)
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    picture = models.ImageField(upload_to='student')
    
    def late_entry_count(self):
        return ((self.late_entry.all().count()-1)%3)+1
    
    def timestamp_entry(self):
        return self.late_entry.all().last().created_at

    def __str__(self):
        return self.name

class LateEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='late_entry')
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, related_name="late_entry", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Late Entries'
    
    def __str__(self):
        return str(self.student.name)+'_'+str(self.student.st_no)+'_'+str(self.student.late_entry_count())