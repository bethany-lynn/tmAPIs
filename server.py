from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TICKETMASTER_KEY']


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY}

    

    # Make a request to the Event Search endpoint to search for events
    res = requests.get(url, params=payload)
    # ^ make a request to an endpoint: takes URL as str, 
        # returns Response object.
        # pass payload dict as a keyword argument called params

    data = res.json()
    # ^ getting str from ticketmaster
    # print("this is data", data['_embedded'])
    # print("this is keys", list(data['_embedded'].keys()))
    list_events = data['_embedded']['events']
    # ^ gets list of events out of data, storing in variable list_events"

    # payload['postalCode'] = 'postalcode'
    # print("this is an event", list_events[0])
    # MAKE ARRAY of all events

    # data = {'Test': ['This is just some test data'],
            # 'page': {'totalElements': 1}}

    events = []
    for event in list_events:
        # if event zipcode within user entered radius of user entered zipcode
        events.append(event)
        # print(event)
        
    # - Use form data from the user to populate any search parameters
    #
    # - Make sure to save the JSON data from the response to the `data`
    #   variable so that it can display on the page. This is useful for
    #   debugging purposes!
    #
    # - Replace the empty list in `events` with the list of events from your
    #   search results



    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""
    # TODO: Finish implementing this view function
    print(id)
    # url = 'https://app.ticketmaster.com/discovery/v2/events/{G5vYZ98wrHxhM}'
    url = f'https://app.ticketmaster.com/discovery/v2/events/{id}'
    payload = {'apikey': API_KEY}

    # makes a request to event search endpoint to search for events
    res = requests.get(url, params=payload)

    # saves the json data to a variable 'data'
    data = res.json()
    print("this is the data", data)
    
    # dictionary from json data
    # event_by_id = data['events'][id]
    # print("this is the event", event_by_id)

    id_event = data['_embedded'][id]


    # event_details = []
    # for event in event_by_id:
    #     event_details.append(event)


    return render_template('event-details.html',event=id_event)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
