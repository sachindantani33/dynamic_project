# # views.py
# from django.contrib.auth.views import PasswordResetView
# from django.urls import reverse_lazy

# class CustomPasswordResetView(PasswordResetView):
#     email_template_name = 'web-site/password_reset_email.html'
#     template_name = 'web-site/password_reset.html'
#     success_url = reverse_lazy('password_reset_done')

#     def get_email_context(self, *args, **kwargs):
#         context = super().get_email_context(*args, **kwargs)
#         context['domain'] = 'https://untraveling-demeritoriously-jorden.ngrok-free.dev'  # Your laptop IP
#         context['protocol'] = 'http'
#         return context
