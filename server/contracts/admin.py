from django.contrib import admin
from .models import Contract, Milestone, Deliverable, Dispute
# Register your models here.

admin.site.register(Contract)
admin.site.register(Milestone)
admin.site.register(Deliverable)
admin.site.register(Dispute)
