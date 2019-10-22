from django.shortcuts import render
import requests


search = "https://api.yelp.com/v3/businesses/search"
auth_key = "N0Cc2WUBNk_eeKPj-PNdPC6Psm_YDGJ5mbUJLqRJjWS5Ir-g22GI0toSDs4Ie0ieW-ydIyMXSFEv9i58rant3jUHHrpCfXgvXiy5mwu9eSng0BKVrA_qEizwCHOmXXYx"
HEADERS = {'Authorization': 'bearer {}'.format(auth_key)}

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

# user hits the button without a location input
def bad_search(request):
    er = {'name': "Please enter a location for your date.", 'image_url': "https://media1.giphy.com/media/6uGhT1O4sxpi8/giphy.gif"}
    return render(request, 'pages/index.html', er)

# update response dictionary so needed fields are top-level
def create_context(response):
    response['start'] = response['hours'][0]['open'][0]['start']
    response['stop'] = response['hours'][0]['open'][0]['end']
    if response['start'] == '0000':
        response['start'] = 'Open 24hrs'
    if response['stop'] == '0000':
        response['stop'] = ''
    if not 'price' in response:
        response['price'] = 'Free'
    else:
        response['price'] = 'PRICE: ' + response['price']
    rating = response['rating']
    stars = {}
    if rating % 1:
        response['half_star'] = '*'
    for i in range(int(rating)):
        stars[i] = i
    response['stars'] = stars
    return response
    
not_open = {}
# user enters all fields and hits button
def full_search(request, location, date, time):
    import requests
    PARAMETERS = {'limit': 50, 'radius': 8000, 'location': location}
    response = requests.get(url = search, params = PARAMETERS, headers = HEADERS).json()
    # delete not open business from response
    for venue in not_open:
        for business in response:
            if venue['id'] == business['id']:
                del business
    venue = highest_rated(response)
    url = 'https://api.yelp.com/v3/businesses/' + venue['id']
    response = requests.get(url = url, headers = HEADERS).json()
    response = create_context(response)
    if int(time.split()[0]) >= int(response['start']) and int(time.split()[0]) <= (int(response['stop']) - 200):
        not_open.clear()
        return render(request, 'pages/index.html', context=response, content_type='string')
    else:
        not_open[response['name']] = response
        return full_search(request, location, date, time)


# user searches with location only
def location_search_only(request, location=None):
    import requests
    PARAMETERS = {'limit': 50, 'radius': 8000, 'location': location}
    response = requests.get(url = search, params = PARAMETERS, headers = HEADERS).json()
    context = highest_rated(response)
    return render(request, 'pages/index.html', context, content_type='string')

# find highest rated venue in dict of venues
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
