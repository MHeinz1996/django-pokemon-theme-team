from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests as HTTP_Client
import pprint
import os
import random

pp = pprint.PrettyPrinter(indent=2, depth=2)

# Create your views here.
def index(request):
    # Holds our team
    poke_team = []

    # used to prevent duplicates
    used_names = []

    # Get our starting pokemon
    rand_num = str(random.randrange(898)+1)

    # Allows user to specify the first pokemon
    if request.GET.get('pokemon'):
        if int(request.GET.get('pokemon')) > 0 and int(request.GET.get('pokemon')) < 899:
            poke_id = request.GET.get('pokemon')
        else:
            # Generates a random pokemon if they input an invalid ID
            poke_id = rand_num
    else:
        # Generates a random pokemon if none are specified
        poke_id = rand_num

    # Set our endpoint with the starting pokemon
    endpoint = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    
    API_response = HTTP_Client.get(endpoint)
    responseJSON = API_response.json()

    # Add that pokemon to our team
    poke_team.append(responseJSON)
    
    # Add that pokemon to our used names list
    used_names.append(responseJSON['name'])

    # New endpoint for specific type
    poke_type = responseJSON['types'][0]['type']['url']

    # Getting data for that pokemon type using the new endpoint
    new_API_response = HTTP_Client.get(poke_type)
    new_responseJSON = new_API_response.json()

    # Find out how many pokemon share this type
    num_of_type = len(new_responseJSON['pokemon'])

    # Fill out rest of team
    while len(used_names)<6:
        new_id = random.randrange(num_of_type)
        new_pokemon = new_responseJSON['pokemon'][new_id]['pokemon']

        # Grab a new pokemon's url so we can grab it's name and sprite
        new_url = new_pokemon['url']
        API_response = HTTP_Client.get(new_url)
        responseJSON = API_response.json()

        # Add pokemon to our team if it is not a duplicate
        if responseJSON['name'] not in used_names:
            poke_team.append(responseJSON)
            used_names.append(responseJSON['name'])

    pp.pprint(poke_team)

    response = render(request, 'pokemon_app/index.html', {'poke_team':poke_team})
    return response