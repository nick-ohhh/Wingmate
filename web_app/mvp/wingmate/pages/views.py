from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')


def search(request, location):
    context = {'location': location}
    return render(request, 'pages/index.html', context, content_type='string')
