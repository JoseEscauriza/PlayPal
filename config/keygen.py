# key generating function
from django.core.management.utils import get_random_secret_key

mykey = get_random_secret_key()  # function call assigned to variable

print(mykey)  # printing of key. Store this in your .env file
