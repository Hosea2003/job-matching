from django.contrib import admin

from matching.models import (
    HardSkill,
    JobHardSkill,
    JobOffer,
    JobSoftSkill,
    SoftSkill,
    User,
    UserHardSkill,
    UserSoftSkill,
)

# Register your models here.
admin.site.register(
    (
        User,
        JobOffer,
        HardSkill,
        SoftSkill,
        UserHardSkill,
        UserSoftSkill,
        JobHardSkill,
        JobSoftSkill,
    )
)
