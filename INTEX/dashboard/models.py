from django.db import models
 
# Create your models here.
class MovieData(models.Model):
    movie = models.CharField(max_length=100)
    domesticBoxOffice = models.IntegerField()
 
    class Meta:
        verbose_name_plural = 'Movie Domestic Box Office Data'
        db_table = 'movie_data'
 
    def __str__(self):
        return f'{self.movie}-{self.domesticBoxOffice}'