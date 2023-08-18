from rest_framework.exceptions import APIException, AuthenticationFailed


class PhoneDoesNotExist(APIException):
    status_code = 400
    default_detail = "Such phone number does not exist"


class InvalidAuthorizationCode(APIException):
    status_code = 403
    default_detail = "Invalid authorization code"


class TokenAuthorizationExpiredError(AuthenticationFailed):
    status_code = 403
    default_detail = "Authorization token expired"


class TokenAuthorizationInvalidError(AuthenticationFailed):
    status_code = 403
    default_detail = "Authorization token is invalid"


class ReferralAlreadyExist(APIException):
    status_code = 400
    default_detail = "Referral link has already been activated"
