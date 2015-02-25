from django.contrib import admin
from dnaedit.models import Species, Lab, LabFile
# Register your models here.


admin.site.register(Species)
admin.site.register(Lab)
admin.site.register(LabFile)