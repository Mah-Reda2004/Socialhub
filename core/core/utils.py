from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(user):
    subject = "Welcome to SocialHub 🎉"
    from_email = "no-reply@socialhub.com"
    to_email = [user.email]

    # Render HTML template
    html_content = render_to_string("account/welcome_email.html", {"user": user})
    
    # Create email
    email = EmailMultiAlternatives(subject, "", from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()
def send_password_reset_email(user, reset_code):
    subject = "Reset your SocialHub password"
    from_email = "no-reply@socialhub.com"
    to_email = [user.email]

    html_content = render_to_string(
        "emails/password_reset_email.html", 
        {"user": user, "reset_code": reset_code}
    )

    email = EmailMultiAlternatives(subject, "", from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()