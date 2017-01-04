'''captcha app views'''
import random
import uuid
import pickle
import requests
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Image, Captcha

GRID_SIZE = 12
MAX_NUMBER_OF_SIGNALS = 3
CAPTCHA_TYPES_COUNT = 2
SELECT_ALL = 0
SELECT_SOME_OF_SEVERAL = 1

#@csrf_exempt
def demo(request):
    '''
    Demo view for capstone.
    '''
    context = {}
    
    if request.method == 'GET':
        context['submission_required'] = True
        return render(request, 'captcha/demo.html', context)
    elif request.method == 'POST':
        data = {}                
        data['captcha_token'] = request.POST['captcha_token']
        data['captcha_selections'] = request.POST['captcha_selections']
        response = json.loads(requests.post('http://localhost:8000/captcha/', data = data).text)

        if response['valid']:
            context['name'] = request.POST['name']
            return render(request, 'captcha/demo.html', context)
        else:
            context['incorrect'] = True
            context['submission_required'] = True
            request.method = 'GET'
            return render(request, 'captcha/demo.html', context)

#@csrf_exempt
def captcha(request, tag_cache = []):
    '''
    captcha
    '''
    if request.method == 'GET':
        #The default list assigned to the tag_cache keyword argument
        #persists through function calls, so at first it will be empty.
        #If empty, it gets populated with all of the tags in the database,
        #and then that query does not need to be made again, and tags
        #can be selected from tag_cache.
        if not tag_cache:
            for tag in [item.popitem()[1] for item in Image.objects.values('tag').distinct()]:
                tag_cache.append(tag)

        #Like using random, but is querying os.urandom() which uses the operating system's
        #random generator and is allegedly cryptographically secure. ¯\_(ツ)_/¯
        urandom = random.SystemRandom()
        urandom.shuffle(tag_cache)

        aggregate = []
        captcha_type = urandom.randrange(CAPTCHA_TYPES_COUNT)
        context = {}
        key = {}
        signal_tags = []
        current_image_count = 0

        for i in range(urandom.randrange(1, MAX_NUMBER_OF_SIGNALS + 1)):
            signal_tags.append(tag_cache[-(i + 1)])

        if captcha_type == SELECT_SOME_OF_SEVERAL:
            signal_tags_and_counts = {}

        for signal_tag in signal_tags:
            count = urandom.randrange(1, 4)
            current_image_count += count

            if captcha_type == SELECT_ALL: #Select all peas.
                key[signal_tag] = count
            elif captcha_type == SELECT_SOME_OF_SEVERAL: #Select 3 peas, 2 keys, 1 trees
                signal_tags_and_counts[signal_tag] = urandom.randrange(1, count + 1)
                key[signal_tag] = signal_tags_and_counts[signal_tag]

            signal = Image.objects.filter(tag = signal_tag)
            aggregate.extend([(signal[i].image_file.name, signal[i].tag) for i in urandom.sample( \
                     range(signal.count()), count)])

        noise_tag_count = 0
        while current_image_count < GRID_SIZE:
            noise_tag_count += 1
            noise_tag = tag_cache[-(noise_tag_count + len(signal_tags))]
            noise = Image.objects.filter(tag = noise_tag)
            free_size = GRID_SIZE - current_image_count
            count = min(urandom.randrange(1, MAX_NUMBER_OF_SIGNALS + 1), free_size)
            current_image_count += count
            aggregate.extend([(noise[i].image_file.name, noise[i].tag) for i in urandom.sample( \
                     range(noise.count()), count)])

        urandom.shuffle(aggregate)
        
        context['grid_images'] = zip(range(GRID_SIZE), [image[0] for image in aggregate])
        context['grid_size'] = GRID_SIZE
        if captcha_type == SELECT_ALL:
            context['prompt_string'] = 'Select all {}.' \
                                       .format(', '.join([tag if tag[-1] == 's' \
                                       else tag + 's' for tag in signal_tags]))
        elif captcha_type == SELECT_SOME_OF_SEVERAL:
            context['prompt_string'] = 'Select {}.'.format(', '.join(['{} {}' \
            .format(count, (signal if signal[-1] == 's' else signal + 's') \
                            if count > 1 else (signal if not signal[-1] == 's' \
                            else signal[:-1])) for signal, count in \
                            signal_tags_and_counts.items()]))

        token = uuid.uuid4().hex
        context['captcha_token'] = token
        Captcha(token = token, key = pickle.dumps(key), grid_images = \
                pickle.dumps([image[1] for image in aggregate])).save()

        return render(request, 'captcha/captcha.html', context)

    elif request.method == 'POST':
        if not 'captcha_token' in request.POST:
            return JsonResponse({'valid': False})

        token = request.POST['captcha_token']
        query = Captcha.objects.filter(token = token)

        if len(query) == 0:
            return JsonResponse({'valid': False})

        captcha_ = query[0]
        captcha_.delete()
        images = pickle.loads(captcha_.grid_images)
        key = pickle.loads(captcha_.key)
        captcha_selections = int(request.POST['captcha_selections'])
        print(captcha_selections)
        selected = {}
        for tag in [images[i] for i in range(GRID_SIZE) \
                    if (captcha_selections & (1 << i))]:
            selected[tag] = selected.get(tag, 0) + 1

        if selected == key:
            return JsonResponse({'valid': True})
        else:
            return JsonResponse({'valid': False})
