from django.contrib.auth import get_user_model
from django.db import models

OS_CHOICE = [
    ['Android', 'Android'],
    ['Iphone', 'Iphone'],
    ['Window', 'Window'],
    ['Linux', 'Linux'],
    ['Mac', 'Mac'],
    ['Other', 'Other']
]

class Visitor(models.Model):
    date = models.DateTimeField(auto_now=True)
    os = models.CharField(max_length=50, choices=OS_CHOICE)
    description = models.TextField()
    page = models.CharField(max_length=50)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True, default=None)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    isp = models.CharField(max_length=150, blank=True, null=True)
    country_code3 = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.user} {self.os}'
