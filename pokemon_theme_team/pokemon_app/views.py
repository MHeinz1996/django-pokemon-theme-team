from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests as HTTP_Client
import pprint
import os
import random

pp = pprint.PrettyPrinter(indent=2, depth=2)

# list our pokemon team


# Create your views here.
def index(request):
    poke_team = []
    used_names = []
    rand_num = str(random.randrange(898)+1)

    if request.GET.get('pokemon'):
        if int(request.GET.get('pokemon')) > 0 and int(request.GET.get('pokemon')) < 899:
            poke_id = request.GET.get('pokemon')
    else:
        poke_id = rand_num

    endpoint = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    
    API_response = HTTP_Client.get(endpoint)
    responseJSON = API_response.json()
    poke_team.append(responseJSON)
    
    used_names.append(responseJSON['name'])

    # New endpoint for specific type
    poke_type = responseJSON['types'][0]['type']['url']

    new_API_response = HTTP_Client.get(poke_type)
    new_responseJSON = new_API_response.json()
    num_of_type = len(new_responseJSON['pokemon'])

    while len(used_names)<6:
        new_id = random.randrange(len(poke_type))
        new_pokemon = new_responseJSON['pokemon'][new_id]['pokemon']

        new_url = new_pokemon['url']
            
        API_response = HTTP_Client.get(new_url)
        responseJSON = API_response.json()

        if responseJSON['name'] not in used_names:
            poke_team.append(responseJSON)
            used_names.append(responseJSON['name'])

    pp.pprint(poke_team)
    response = render(request, 'pokemon_app/index.html', {'poke_team':poke_team})
    return response