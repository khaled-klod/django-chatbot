from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *

admin.site.register(Company)
admin.site.register(University)



admin.site.register(Application)
admin.site.register(Skills)
admin.site.register(Characteristics)

admin.site.register(Person)
admin.site.register(PersonSkills)
admin.site.register(PersonLanguages)
admin.site.register(FinalView)

#admin.site.register(AllSkill)

#admin.site.register(desired_skill)