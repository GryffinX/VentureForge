from django.contrib import admin
from .models import Skill, Category, Project, Proposal, FreelancerSkill, ProjectSkill
# Register your models here.

admin.site.register(Skill)
admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Proposal)
admin.site.register(FreelancerSkill)
admin.site.register(ProjectSkill)
