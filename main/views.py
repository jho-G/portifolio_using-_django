from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def home(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Prepare email content
        subject = f"Portfolio Contact: Message from {name}"
        full_message = f"""
        Name: {name}
        Email: {email}
        
        Message:
        {message}
        """
        
        try:
            # Send email to yourself
            send_mail(
                subject=subject,
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],  # Send to yourself
                fail_silently=False,
            )
            
            # Also send confirmation to the user
            user_subject = "Message Received - Yohannes Girma"
            user_message = f"""
            Hi {name},
            
            Thank you for reaching out! I've received your message and will get back to you soon.
            
            Best regards,
            Yohannes Girma
            """
            
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,  # Don't crash if user email fails
            )
            
            messages.success(request, 'Message sent successfully!')
            return redirect('home')
            
        except Exception as e:
            print(f"Email sending failed: {e}")
            messages.error(request, 'Failed to send message. Please try again later.')
    
    return render(request, 'main/index.html')




# main/views.py - Add this function
def test_email(request):
    try:
        send_mail(
            subject='Test Email',
            message='This is a test email from Django.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return HttpResponse("Test email sent successfully!")
    except Exception as e:
        return HttpResponse(f"Failed to send email: {e}")