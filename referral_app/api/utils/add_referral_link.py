from typing import Dict

from referral_app.api.models import User

from .exceptions import PhoneDoesNotExist, ReferralAlreadyExist


def add_referral(request, invite_code: str) -> Dict[str, str]:
    try:
        inviting_user = User.objects.get(invite_code=invite_code)
    except User.DoesNotExist:
        raise PhoneDoesNotExist()

    check_existing_referral(request.user)

    if inviting_user != request.user:
        inviting_user.referred_users.add(request.user)
        inviting_user.save()
        return {"message": "Referrer added successfully"}
    return {"message": "Not allowed to activate your own invitation code!"}


def check_existing_referral(user: User) -> None:
    if user.referral_activated:
        raise ReferralAlreadyExist()
    user.referral_activated = True
    user.save(update_fields=["referral_activated"])
