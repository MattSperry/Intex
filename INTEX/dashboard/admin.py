from django.contrib import admin
from .models import Person, Comorbidity, Race, JournalEntry, Food
 
# Register your models here.
admin.site.register(Person)
admin.site.register(Comorbidity)
admin.site.register(Race)
admin.site.register(JournalEntry)
admin.site.register(Food)


