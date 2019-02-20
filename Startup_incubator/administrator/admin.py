from django.contrib import admin
from .models import Documents

from .models import Updates,Fund,Incubation,AssignMentor,Milestones,Reviews

from .models import Updates,Fund,Incubation,AssignMentor

# Register your models here.
admin.site.register(Documents)
admin.site.register(Reviews)	
# Register your models here.
admin.site.register(Updates)
admin.site.register(Fund)
admin.site.register(Incubation)
admin.site.register(AssignMentor)
admin.site.register(Milestones)


