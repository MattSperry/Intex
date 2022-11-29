from django.db import models
from datetime import datetime
import django
 
# Create your models here.
class Comorbidity(models.Model):
    name = models.CharField(max_length=20, primary_key = True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return(self.name)
    class Meta:
        db_table = 'Comorbidity'

class Race(models.Model):
    race = models.CharField(max_length = 20, primary_key = True)

    def __str__(self):
        return(self.race)

    class Meta:
        db_table = 'Race'

class Person(models.Model):
    personID = models.OneToOneField('auth.User', on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    comorbidity = models.ForeignKey('Comorbidity', null=True, blank=True, on_delete=models.SET_NULL)
    date_of_birth = models.DateField(default=django.utils.timezone.now)
    weight = models.IntegerField()
    height = models.IntegerField()
    gender = models.BinaryField()
    race = models.ForeignKey('Race', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return(self.first_name + ' ' + self.last_name)

    class Meta:
        db_table = 'person'

class JournalEntry(models.Model):
    personID = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    journalID = models.AutoField(primary_key=True)
    date_time_recorded = models.DateTimeField(default=datetime.now(), blank=True)
    date_time_eaten = models.DateTimeField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    food_name = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.journalID) + " " + str(self.date_time_recorded)

    class Meta:
        db_table = 'Journal Entry'


    
