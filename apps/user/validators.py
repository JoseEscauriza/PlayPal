from django.core.exceptions import ValidationError

# RATING CHECK >= 1 AND <= 5
def check_rating_range(value):
    if value < 0 or value > 5:
        raise ValidationError("Rating must be between 0 and 5")