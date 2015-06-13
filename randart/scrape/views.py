from django.http import HttpResponse

def index(request):
    return HttpResponse('hello, testing scrape views.')
