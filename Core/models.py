from django.db import models

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
        return self.late_entry.all().count()


class LateEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='late_entry')

    class Meta:
        verbose_name_plural = 'Late Entries'