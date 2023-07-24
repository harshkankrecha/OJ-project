from django.contrib import admin
from .models import Contest,Question,Submission,Testcases,Score

admin.site.register(Contest)
admin.site.register(Score)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Testcases)
