from django.db import models
 
# Create your models here.
class Comorbidity(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return(self.name)

    class Meta:
        db_table = 'comorbidity'
class Person(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    comorbidity = models.ForeignKey('Comorbidity', null=True, blank=True, on_delete=models.SET_NULL)
    age = models.IntegerField()
    weight = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return(self.name)

    class Meta:
        db_table = 'person'
