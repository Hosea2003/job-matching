from matching.models import JobHardSkill, JobOffer, User, UserHardSkill, UserSoftSkill
from django.db.models.functions import Coalesce
from django.db.models import (
    Sum,
    Case,
    When,
    FloatField,
    Value,
    F,
    IntegerField,
    Count,
    OuterRef,
    Subquery,
    Exists,
)
import math

"""
To make the formula simple and clean:
- having all the skills needed and having a level higher or equal than the required level is a 100% matching
- if the user has the skill but the level is less than required: 
"""


def select_matching_offers(user: User):
    def user_hardskill_level():
        return UserHardSkill.objects.filter(
            user=user,
            hardskill=OuterRef("job_hardskills__hardskill"),
        ).values("level")

    def user_softskill_level():
        return UserSoftSkill.objects.filter(
            user=user,
            softskill=OuterRef("job_softskills__softskill"),
        ).values("level")

    if user is None:
        return []

    user_hard_skills = UserHardSkill.objects.filter(user=user).values(
        "hardskill__id", "level"
    )

    user_soft_skills = UserSoftSkill.objects.filter(user=user).values(
        "softskill__id", "level"
    )

    jobs = (
        JobOffer.objects.annotate(
            required_hardskills=Count("job_hardskills"),
            required_softskills=Count("job_softskills"),
        )
        .annotate(
            # calculate hardskill matching
            total_hardskills_match=Sum(
                Case(
                    When(
                        job_hardskills__hardskill__in=user_hard_skills.values(
                            "hardskill"
                        ),
                        then=1,
                    ),
                    default=0,
                    output_field=IntegerField(),
                )
            ),
            total_softskills_match=Sum(
                Case(
                    When(
                        job_softskills__softskill__in=user_soft_skills.values(
                            "softskill"
                        ),
                        then=1,
                    ),
                    default=0,
                    output_field=IntegerField(),
                )
            ),
            total_hardskills_required=Count("job_hardskills"),
            total_softskills_required=Count("job_softskills"),
            hard_skill_match=Sum(
                Case(
                    When(
                        job_hardskills__hardskill__in=user_hard_skills.values(
                            "hardskill"
                        ),
                        then=Case(
                            When(
                                job_hardskills__level__gt=Subquery(
                                    user_hardskill_level()
                                ),
                                then=(
                                    Subquery(user_hardskill_level())
                                    / F("job_hardskills__level")
                                ),
                            ),
                            default=1.0,
                            output_field=FloatField(),
                        ),
                    ),
                    default=0,
                    output_field=FloatField(),
                )
            )
            / F("total_hardskills_required"),
            soft_skill_match=Sum(
                Case(
                    When(
                        job_softskills__softskill__in=user_soft_skills.values(
                            "softskill"
                        ),
                        then=Case(
                            When(
                                job_softskills__level__gt=Subquery(
                                    user_softskill_level()
                                ),
                                then=(
                                    Subquery(user_softskill_level())
                                    / F("job_softskills__level")
                                ),
                            ),
                            default=1.0,
                            output_field=FloatField(),
                        ),
                    ),
                    default=0,
                    output_field=FloatField(),
                )
            )
            / F("total_softskills_required"),
            experience_bonus=Case(
                When(experience=0, then=1),
                When(
                    experience__gt=user.experience,
                    then=user.experience / F("experience"),
                ),
                default=1,
                output_field=FloatField(),
            ),
            total_match=(
                F("hard_skill_match") * 0.5
                + F("soft_skill_match") * 0.2
                + F("experience_bonus") * 0.3
            )
            * 100,
        )
        .filter(total_match__gte=50)
        .order_by("-total_match")
    )

    return jobs
