from django.shortcuts import render
import requests


# Create your views here.
def index(request):
    return render(request, 'pages/index.html')


def bad_search(request):
    er = {'name': "Please enter a location for your date.", 'image_url': "https://media1.giphy.com/media/6uGhT1O4sxpi8/giphy.gif"}
    return render(request, 'pages/index.html', er)


def search(request, location=None):
    import requests
    search = "https://api.yelp.com/v3/businesses/search"
    auth_key = "N0Cc2WUBNk_eeKPj-PNdPC6Psm_YDGJ5mbUJLqRJjWS5Ir-g22GI0toSDs4Ie0ieW-ydIyMXSFEv9i58rant3jUHHrpCfXgvXiy5mwu9eSng0BKVrA_qEizwCHOmXXYx"
    HEADERS = {'Authorization': 'bearer {}'.format(auth_key)}
    PARAMETERS = {'limit': 50, 'radius': 8000, 'location': location}
    response = requests.get(url = search, params = PARAMETERS, headers = HEADERS).json()
    context = highest_rated(response)
    return render(request, 'pages/index.html', context, content_type='string')

def highest_rated(response):
    dict_business = []
    highest = 3
    chosen = 'No suitable venues were found'
    tmp = {}
    # tmp fix for a return value bug
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCnfTkcfMsh1rtHVq2_CcJGCfz1oKZvD1E=&callback=initMap"
    for business in response['businesses']:
        if business['rating'] >= highest:
            highest = business['rating']
            tmp = business
    return tmp
