from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from datetime import timedelta

class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        Override this method to add custom logic for expiration.
        """
        # 30-minute expiration logic
        expiration_time = timezone.now() + timedelta(minutes=30)
        return str(user.pk) + str(timestamp) + str(user.password) + str(user.date_joined) + str(expiration_time)

# Initialize token generator instance
password_reset_token = CustomPasswordResetTokenGenerator()
