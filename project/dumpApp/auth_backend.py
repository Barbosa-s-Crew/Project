from django.contrib.auth.backends import BaseBackend

class MyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):

        
