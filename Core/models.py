from unicodedata import name
from django.core.exceptions import ValidationError
from django.db import models
from Auth.models import User
from django.db.models import CheckConstraint, Q
from filer.fields.image import FilerFileField, FilerImageField
from Core.utils import compress
from filer.models.abstract import BaseImage
from filer.models.filemodels import File
from django.urls import NoReverseMatch, reverse

class Operator(User):

    class Meta:
        proxy=True

class Venue(models.Model):
    venue = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.venue

class Batch(models.Model):
    batch = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.batch)
    
    def clean(self) -> None:
        if self.batch < 1998:
            raise ValidationError("The Batches cannot be made before college establishment.") 

    class Meta:
        verbose_name_plural = "Batches"
        ordering = ['batch',]
        constraints = [
            CheckConstraint(
                check = Q(batch__gt=1997), name="check_batch"
            )
        ]

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
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    
    def late_entry_count(self):
        return self.late_entry.all().count()
    
    def timestamp_entry(self):
        return self.late_entry.all().last().timestamp

    def __str__(self):
        return self.name

class LateEntry(models.Model):
    timestamp = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='late_entry')
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, related_name="late_entry", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Late Entries'
    
    def __str__(self):
        return str(self.student.name)+'_'+str(self.student.st_no)

class StudentImage(models.Model):
    def get_image_path(self, filename):
        return f'student/{self.batch.batch}/{filename}'
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    # image = models.FileField(upload_to = get_image_path)
    img = FilerImageField(null=True,blank=True, on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #     # call the compress function
    #     new_image = compress(self.image)
    #     # set self.image to new_image
    #     self.image = new_image
    #     # save
    #     super().save(*args, **kwargs)


class CustomImage(BaseImage):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)

    class Meta(BaseImage.Meta):
        app_label = 'Core'
        default_manager_name = 'objects'
    
    def get_admin_change_url(self):
        return reverse(
            'admin:{0}_{1}_change'.format(
                "filer",
                "file",
            ),
            args=(self.pk,)
        )

    def get_admin_delete_url(self):
        return reverse(
            'admin:{0}_{1}_delete'.format( "filer","file",),
            args=(self.pk,))

    def save(self, *args, **kwargs):
        folder = str(self.folder)
        meta_information = folder.rsplit('/')
        request_batch = meta_information[1]
        branch = meta_information[2]
        self.batch = Batch.objects.get(batch=int(request_batch))
        self.branch = Branch.objects.get(name=branch)
        self.has_all_mandatory_data = self._check_validity()
        super().save(*args, **kwargs)

class FilerAdmin(File):

    @classmethod
    def matches_file_type(cls, iname, ifile, mime_type):
        # source: https://www.freeformatter.com/mime-types-list.html
        image_subtypes = ['gif', 'jpeg', 'png', 'x-png', 'svg+xml']
        maintype, subtype = mime_type.split('/')
        return maintype == 'image' and subtype in image_subtypes