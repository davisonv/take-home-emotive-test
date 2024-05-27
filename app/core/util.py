from django.core.validators import RegexValidator

class Validators:
    """Class containing reusable validation methods."""
    phone_validator = RegexValidator(
        regex=r'^(\+?[1-9]\d{0,2}\s?)?(\(?\d{1,4}\)?\s?)?(\d{1,4}[\s.-]?)?\d{1,4}[\s.-]?\d{1,9}$',
        message="""Phone number must be entered in a valid international format, 
        e.g., '+1 800-555-1234', '0800 555 1234', '(0800) 555-1234', '+44 20 7946 0958', 
        '+91 98765 43210'."""
    )