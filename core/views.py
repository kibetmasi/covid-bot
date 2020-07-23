from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests
import datetime
import emoji
import random
import json

@csrf_exempt
def index(request):
    if request.method == 'POST':
        # retrieve incoming message from POST request in lowercase
        incoming_msg = request.POST['Body'].lower()

        # create Twilio XML response
        resp = MessagingResponse()
        msg = resp.message()

        
        
        if incoming_msg == 'prevention':
        	 response = emoji.emojize("""
:clap:Wash your hands regularly with plenty of soap and water(or use hand-based alcohol sanitiser)
:mask:Always cover your mouth with a cloth when sneezing or coughing
:tv:Always stay updated on Covid19 news. You can get verified information from https://www.health.go.ke/covid-19/
:dizzy_face:Common signs and symptoms may include headaches, bodyache, fever and shortness of breath
:kissing_heart:Avoid kissing, hugging and handshakes with people who have flu-like symptoms
:heart:

_This information is given by the ministry of health Kenya._
_Incase you have these symptoms, call 0800 721 316_

You can message me "misconceptions" to know some of the common Covid19 misconceptions in Kenya
""", use_aliases=True)
        	 msg.body(response)
        	 responded = True  
                
        
        if incoming_msg == 'misconceptions':
        	 response = emoji.emojize("""
~:sunglasses:A vaccine to prevent COVID-19 is available.~ No vaccine currently exists

~:sunglasses:Drinking Alcohol Will Protect You from Coronavirus~ Alcohol does not kill the viruses inside your body

~:sunglasses:Coronavirus only affects older people~ All people of all ages are suspectible to Covid19

_Only obtain news about the pandemic from reputable sources!_
""", use_aliases=True)
        	 msg.body(response)
        	 responded = True
        
        
        if incoming_msg == 'owner':
        	 response = emoji.emojize("""
:sunglasses:Covidbot ICS2020 MasiK
""", use_aliases=True)
        	 msg.body(response)
        	 responded = True        
   
        
        if incoming_msg == 'symptoms':
        	 response = emoji.emojize("""
:pill:The novel CoronaVirus symptoms may include: 
*Most common sysmtoms;*
:heavy_check_mark: Fever
:heavy_check_mark: Dry coughs
:heavy_check_mark: Tiredness
*Less common symptoms;*
:heavy_check_mark: Running stomach
:heavy_check_mark: Loss of taste or smell
:heavy_check_mark: Sore throat
*Serious symptoms;*
:heavy_check_mark: Chest pain or pressure
:heavy_check_mark: Loss of speech or movement
:heavy_check_mark: Difficulty in breathing

_If you feel the above symptoms or suspect someone, call the Ministry of Health hotline 0800721316, 0732353535, 0729471414_
Save a life:pray:
""", use_aliases=True)
        	 msg.body(response)
        	 responded = True
        
        
        if incoming_msg == 'hello':
        	 response = emoji.emojize("""
*Hey! I am CovidBot.* I give latest Corona virus stats, preventions and symptoms in Kenya :man: 
Let's be friends :wink:
*You can give me the following commands:*
:black_small_square: *'kenya':* Get stats for Covid19::earth_africa: 
:black_small_square: *'yes':* Get daily stats for Covid :smiley:
:black_small_square: *Symptoms*: show Covid19 symptoms:
:black_small_square: *prevention*: show various ways to protect oneself from covid:
:black_small_square: *'statistics <country>'*: Show the latest COVID19 statistics for each country. :earth_americas:
:black_small_square: *'statistics <prefix>'*: Show the latest COVID19 statistics for all countries starting with that prefix. :globe_with_meridians:
:black_small_square::globe_with_meridians::black_small_square::globe_with_meridians:PEGHIN


""", use_aliases=True)
        	 msg.body(response)
        	 responded = True  
                
                
                
               
        elif incoming_msg == 'kenya':
            # returns a quote
            r = requests.get('https://corona.lmao.ninja/v2/countries/kenya')
            if r.status_code == 200:
                data = r.json()
                kenya = f"""
                Total tests done stands at {data["tests"]},\n 
and the cases are {data["cases"]}.\n
We have {data["recovered"]} recoveries,\n
while {data["active"]} are active cases.\n
Now {data["critical"]} are critical cases.\n
Sadly {data["deaths"]} Kenyans have died.\n
Would you like me to tell you the stats for today alone?
                """
            else:
                kenya = 'I could not retrieve the info at this time, sorry.'
            msg.body(kenya)
            responded = True
        elif incoming_msg == 'yes':
            # returns a quote
            r = requests.get('https://corona.lmao.ninja/v2/countries/kenya')
            if r.status_code == 200:
                data = r.json()
                yes = f"""
Today`s cases are {data["todayCases"]}'.\n
We have {data["todayRecovered"]} recoveries today.\n
Unfortunately we have lost {data["todayDeaths"]} Kenyans today.\n
That is all I have for you.
Stay safe we shall overcome!
                """
            else:
                yes = 'I could not retrieve the info at this time, sorry.'
            msg.body(yes)
            responded = True
        elif incoming_msg.startswith('statistics'):
            # runs task to aggregate data from Apify Covid-19 public actors
            requests.post('https://api.apify.com/v2/actor-tasks/5MjRnMQJNMQ8TybLD/run-sync?token=qTt3H59g5qoWzesLWXeBKhsXu&ui=1')         
            # get the last run dataset items
            r = requests.get('https://api.apify.com/v2/actor-tasks/5MjRnMQJNMQ8TybLD/runs/last/dataset/items?token=qTt3H59g5qoWzesLWXeBKhsXu')         
            if r.status_code == 200:
                data = r.json()
                country = incoming_msg.replace('statistics', '')
                country = country.strip()
                country_data = list(filter(lambda x: x['country'].lower().startswith(country), data))
                if country_data:
                    result = ''
                    for i in range(len(country_data)):
                        data_dict = country_data[i]
                        last_updated = datetime.datetime.strptime(data_dict.get('lastUpdatedApify', None), "%Y-%m-%dT%H:%M:%S.%fZ")
                        result += """
*Statistics for country {}*
Infected: {}
Tested: {}
Recovered: {}
Deceased: {}
Last updated: {:02}/{:02}/{:02} {:02}:{:02}:{:03} UTC
""".format(
    data_dict['country'], 
    data_dict.get('infected', 'NA'), 
    data_dict.get('tested', 'NA'), 
    data_dict.get('recovered', 'NA'), 
    data_dict.get('deceased', 'NA'),
    last_updated.day,
    last_updated.month,
    last_updated.year,
    last_updated.hour,
    last_updated.minute,
    last_updated.second
    )
                else:
                    result = "Country not found. Sorry!"
            
            else:
                result = "I cannot retrieve statistics at this time. Sorry!"

            msg.body(result)
            responded = True
        return HttpResponse(str(resp))



        
