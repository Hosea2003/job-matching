from django.shortcuts import render
from django.http import HttpRequest

from matching.models import User
from matching.selector import select_matching_offers


# Create your views here.
def index(request: HttpRequest):
    email = request.GET.get("email", "")
    default_user = User.objects.filter(email__icontains=email).first()
    offers = select_matching_offers(default_user)
    return render(request, "offers.html", context={"jobs": offers})
