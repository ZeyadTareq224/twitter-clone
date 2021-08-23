from django.shortcuts import render, redirect
from django.views import View

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'landing/index.html')


