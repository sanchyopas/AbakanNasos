from subdomain.models import Subdomain


def subdomain(request):
  return {"subdomains": Subdomain.objects.all()}