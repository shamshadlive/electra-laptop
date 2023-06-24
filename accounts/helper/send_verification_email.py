from verify_email.email_handler import _VerifyEmail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail



class CustomVerifyEmail(_VerifyEmail):
     # Private :
    def __send_email(self, msg, useremail):
        subject = self.settings.get('subject')
        send_mail(
            subject, strip_tags(msg),
            from_email=self.settings.get('from_alias'),
            recipient_list=[useremail], html_message=msg
        )
        
    def send_verification_link(self, request, form):
        inactive_user = form.save(commit=False)
        inactive_user.is_active = False
        inactive_user.is_email_verified = False
        inactive_user.save()

        try:
            useremail = form.cleaned_data.get(self.settings.get('email_field_name'))
            if not useremail:
                raise KeyError(
                    'No key named "email" in your form. Your field should be named as email in form OR set a variable'
                    ' "EMAIL_FIELD_NAME" with the name of current field in settings.py if you want to use current name '
                    'as email field.'
                )

            verification_url = self.token_manager.generate_link(request, inactive_user, useremail)
            msg = render_to_string(
                self.settings.get('html_message_template', raise_exception=True),
                {"link": verification_url, "inactive_user": inactive_user}, 
                request=request
            )

            self.__send_email(msg, useremail)
            return inactive_user
        except Exception:
            inactive_user.delete()
            raise
        
    #  These is supposed to be called outside of this module
    def send_verification_email(request, form):
        return CustomVerifyEmail().send_verification_link(request, form)

