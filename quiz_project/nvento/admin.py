from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Score)
admin.site.register(TopScorer)
