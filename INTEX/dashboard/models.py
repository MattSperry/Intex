from django.db import models
 
# Create your models here.
class Person(models.Model):
    personID = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name + " " + self.last_name
    class Meta:
        db_table = "person"