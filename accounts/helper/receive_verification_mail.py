import logging

from django.http import Http404, HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.signing import SignatureExpired, BadSignature

from verify_email.app_configurations import GetFieldFromSettings

from .confirm_token import verify_user


from verify_email.errors import (
    InvalidToken,
    MaxRetriesExceeded,
    UserAlreadyActive,
    UserNotFound,
)

logger = logging.getLogger(__name__)

pkg_configs = GetFieldFromSettings()

login_page = pkg_configs.get('login_page')

success_msg = pkg_configs.get('verification_success_msg')
failed_msg = pkg_configs.get('verification_failed_msg')

failed_template = pkg_configs.get('verification_failed_template')
success_template = pkg_configs.get('verification_success_template')
link_expired_template = pkg_configs.get('link_expired_template')
request_new_email_template = pkg_configs.get('request_new_email_template')
new_email_sent_template = pkg_configs.get('new_email_sent_template')



def receive_verification_mail(request, useremail, usertoken):
    try:
        verified = verify_user(useremail, usertoken)
        if verified is True:
            if login_page and not success_template:
                messages.success(request, success_msg)
                return redirect(to=login_page)
            return render(
                request,
                template_name=success_template,
                context={
                    'msg': success_msg,
                    'status': 'Verification Successful!',
                    'link': reverse(login_page)
                }
            )
        else:
            # we dont know what went wrong...
            raise ValueError
    except (ValueError, TypeError) as error:
        logger.error(f'[ERROR]: Something went wrong while verifying user, exception: {error}')
        return render(
            request,
            template_name=failed_template,
            context={
                'msg': failed_msg,
                'minor_msg': 'There is something wrong with this link...',
                'status': 'Verification Failed!',
            }
        )
    except SignatureExpired:
        return render(
            request,
            template_name=link_expired_template,
            context={
                'msg': 'The link has lived its life :( Request a new one!',
                'status': 'Expired!',
                'encoded_email': useremail,
                'encoded_token': usertoken
            }
        )
    except BadSignature:
        return render(
            request,
            template_name=failed_template,
            context={
                'msg': 'This link was modified before verification.',
                'minor_msg': 'Cannot request another verification link with faulty link.',
                'status': 'Faulty Link Detected!',
            }
        )
    except MaxRetriesExceeded:
        return render(
            request,
            template_name=failed_template,
            context={
                'msg': 'You have exceeded the maximum verification requests! Contact admin.',
                'status': 'Maxed out!',
            }
        )
    except InvalidToken:
        return render(
            request,
            template_name=failed_template,
            context={
                'msg': 'This link is invalid or been used already, we cannot verify using this link.',
                'status': 'Invalid Link',
            }
        )
    except UserNotFound:
        raise Http404("404 User not found")
    
    