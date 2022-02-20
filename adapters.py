from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest

from users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


# class SocialAccountAdapter(DefaultSocialAccountAdapter):
#     def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
#         return getattr(settings, "SOCIALACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        # print(user)
        try:
            user = User.objects.get(email=user.email)
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass
        except Exception as e:
            print(e)

    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "SOCIALACCOUNT_ALLOW_REGISTRATION", True)
