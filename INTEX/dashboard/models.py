from django.db import models
 
# Create your models here.
class Comorbidity(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return(self.name)

    class Meta:
        db_table = 'comorbidity'

class Person(models.Model):
    personID = models.OneToOneField('auth.User', on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    comorbidity = models.ForeignKey('Comorbidity', null=True, blank=True, on_delete=models.SET_NULL)
    age = models.IntegerField(default=18)
    weight = models.IntegerField(default=180)
    height = models.IntegerField(default=72)

    def __str__(self):
        return(self.first_name + ' ' + self.last_name)

    class Meta:
        db_table = 'person'
