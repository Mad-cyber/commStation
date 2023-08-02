from django.test import TestCase
from datetime import time

# test case to show date and time output
for h in range (0,24):
    for m in (0,30):
        print(time(h,m).strftime('%I:%M %p'))


