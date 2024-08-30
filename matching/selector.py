from matching.models import JobHardSkill, JobOffer, User, UserHardSkill, UserSoftSkill
from django.db.models.functions import Coalesce
from django.db.models import (
    Sum,
    Case,
    When,
    FloatField,
    F,
    IntegerField,
    Count,
    OuterRef,
    Subquery,
)


def select_matching_offers(user: User):
    # get level for a specific hardskill of an user
    def user_hardskill_level():
        return UserHardSkill.objects.filter(
            user=user,
            hardskill=OuterRef("job_hardskills__hardskill"),
        ).values("level")

    # get level for a specific softskill of an user
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
                                # if the level hardskill required is higher than the user
                                # we calculate the ratio between the level of the user and the required level
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
            # calculate final result by considering the percentage
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
