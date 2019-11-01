from django.shortcuts import render
import requests
from pages.keys import yelp, maps


search = "https://api.yelp.com/v3/businesses/search"
HEADERS = {'Authorization': 'bearer {}'.format(yelp)}

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

# user hits the button without a location input
def bad_search(request):
    er = {'name': "Please enter a location for your date.", 'image_url': "https://media1.giphy.com/media/6uGhT1O4sxpi8/giphy.gif"}
    return render(request, 'pages/index.html', er)

# update response dictionary so needed fields are top-level
def create_context(response):
    if response['start'] == '0000':
        response['start'] = 'Open 24hrs'
    if response['stop'] == '0000':
        response['stop'] = ''
    if not 'price' in response:
        response['price'] = 'Free'
    rating = response['rating']
    stars = {}
    if rating % 1:
        response['half_star'] = '*'
    for i in range(int(rating)):
        stars[i] = i
    response['stars'] = stars
    # address is a list of lines in the address, like 123 abc street is 1 line, city name another, and so on
    if 'location' in response:
        if 'display_address' in response['location']:
            address = response['location']['display_address'][0]
            faddress = response['location']['display_address'][0].replace(' ', '+')
            response['address'] = address
            if len(response['location']['display_address']) > 1:
                for line in response['location']['display_address']:
                    if ',' in line and line != address:
                        address = address + ', ' + line
                        response['address'] = address
                        line = line.replace(',', '')
                        faddress = faddress + ',' + line
            else:
                response['address'] = address
        else:
            response['address'] = ['Unknown']
    else:
        response['address'] = ['Unknown']
        '''
        for i in response['location']['display_address']:
            response['address'].append(i)
            address = i
            if count == 0:
                addr = i
            count += 1
        address = addr + ' ' + address
        '''

    alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    count = 0
    # remove characters like '&' from address that might mess up google maps url
    for l in faddress:
        if l not in alpha:
            faddress.replace(l, '')
        count += 1
    # format venue name and address for google maps url
    fvenue = response['name'].replace(' ', '+')
    faddress = faddress.replace(' ', '+')
    response['fvenue'] = fvenue
    try:
        zip_code_s = faddress.split('+')[-1]
        zip_code = int(faddress.split('+')[-1])
        faddress = faddress.replace(zip_code_s, '')
        faddress = faddress[:-1]
    except:
        pass
    faddress = faddress.replace('&', '')
    response['faddress'] = faddress
    google_url = "https://www.google.com/maps/embed/v1/place?key=" + maps + "&q=" + fvenue + ',' + faddress
    google_dir = "https://www.google.com/maps?saddr=My+Location&daddr=" + faddress
    import requests
    test_maps = requests.get(google_url)
    if test_maps.status_code != 200:
        response['error'] = True
    response['debug'] = test_maps
    response['google_map'] = google_url
    response['google_dir'] = google_dir
    return response

def convert_user_dates(response, date, time):
    from datetime import datetime, timedelta
    # convert user input date/time into datetime object
    time = datetime.strptime(time, "%H:%M")
    time = time.strftime("%I:%M %p")
    desired = date + ' ' + time
    desired = datetime.strptime(desired, '%Y-%m-%d %I:%M %p')
    return response['businesses'], desired


def is_open(venue, desired, date, time):
    from datetime import datetime, timedelta
    weekday = desired.weekday()
    if not 'hours' in venue:
        venue['start'] = 'Open 24hrs'
        venue['stop'] = ''
        return True
    if len(venue['hours']) == 0:
        venue['start'] = 'Open 24hrs'
        venue['stop'] = ''
        return True
    if 'open' not in venue['hours'][0]:
        venue['start'] = 'Open 24hrs'
        venue['stop'] = ''
        return True
    if len(venue['hours'][0]['open']) == 0:
        venue['start'] = 'Open 24hrs'
        venue['stop'] = ''
        return True
    try:
        biz_day = venue['hours'][0]['open'][weekday]
    except:
        venue['start'] = 'Open 24hrs'
        venue['stop'] = ''
        return True

    biz_open_s = biz_day['start']
    biz_close_s = biz_day['end']
    # convert from 24 hour to 12 hur
    biz_open_s = datetime.strptime(biz_open_s, "%H%M")
    biz_open_s = biz_open_s.strftime("%I:%M %p")
    biz_close_s = datetime.strptime(biz_close_s, "%H%M")
    biz_close_s = biz_close_s.strftime("%I:%M %p")
    # formatted like: HH:MM AM
    venue['start'] = biz_open_s
    venue['stop'] = biz_close_s
    if is_open_late(biz_open_s, biz_close_s, time):
        # format like: YYY-MM-DD HH:MM AM
        biz_open_s = date + ' ' + biz_open_s
        biz_close_s = date + ' ' + biz_close_s 
        # create datetime objects
        biz_open = datetime.strptime(biz_open_s, "%Y-%m-%d %H:%M %p")
        biz_close = datetime.strptime(biz_close_s, "%Y-%m-%d %H:%M %p")
        # add 1 day to biz_close
        biz_close = biz_close + timedelta(days=1)
    # format like: YYY-MM-DD HH:MM AM
    else:
        biz_open_s = date + ' ' + biz_open_s
        biz_close_s = date + ' ' + biz_close_s 
        # converted into datetime objects
        biz_open = datetime.strptime(biz_open_s, "%Y-%m-%d %I:%M %p")
        biz_close = datetime.strptime(biz_close_s, "%Y-%m-%d %I:%M %p")
    if desired > biz_open and desired < biz_close:
        return True
    return False



def is_open_late(o, c, time):
    hour = int(time.split(":")[0])
    if hour > 9:
        if 'AM' in c and 'PM' in o:
            return True
    o_h = int(o.split(':')[0])
    c_h = int(c.split(':')[0])
    if o_h > c_h:
        return True
    return False



def full_search(request, location, date, time):
    import requests
    PARAMETERS = {'limit': 50, 'radius': 8000, 'location': location, 'sort_by': 'rating'}
    search_response = requests.get(url = search, params = PARAMETERS, headers = HEADERS).json()
    while(len(search_response['businesses']) > 0):
        list_businesses, desired = convert_user_dates(search_response, date, time)
        venue = randomize(list_businesses)
        v_id = venue['id']
        url = "http://api.yelp.com/v3/businesses/" + v_id
        venue = requests.get(url = url, params = PARAMETERS, headers = HEADERS).json()
        if is_open(venue, desired, date, time):
            venue = create_context(venue)
            if 'image_url' in venue and 'photos' in venue:
                if venue['image_url'] == venue['photos'][0]:
                    del venue['photos'][0]
            return render(request, 'pages/index.html', context=venue, content_type='string')
        else:
            count = 0
            for i in list_businesses:
                if i['id'] == v_id:
                    search_response['businesses'].pop(count)
                count += 1
    no_match = {'name': 'Nothing found.'}
    return render(request, 'pages/index.html', context=no_match, content_type='string')



def randomize(l_biz):
    import random
    a = random.randint(0, len(l_biz) - 1)
    return l_biz[a]


