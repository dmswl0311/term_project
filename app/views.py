from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Voca
from .models import Today
from .models import Profile
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.db.models import F

import json
from django.views.decorators.csrf import csrf_exempt

from chatterbot import ChatBot
try:
    from django.utills import simplejson as json
except ImportError:
    import json


def index(request):
    todays = Today.objects.order_by('?')[0]

    context = {"todays": todays}
    return render(request, 'index.html', context)


#----------------------------------
# 챗봇
chatbot = ChatBot('Ron Obvious',
                  trainer='chatterbot.trainers.ChatterBotCorpusTrainer')

# Train based on the english corpus

#Already trained and it's supposed to be persistent
#chatbot.train("chatterbot.corpus.english")


@csrf_exempt
def get_response(request):
    response = {'status': None}

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        message = data['message']

        chat_response = chatbot.get_response(message).text
        response['message'] = {
            'text': chat_response,
            'user': False,
            'chat_bot': True
        }
        response['status'] = 'ok'

    else:
        response['error'] = 'no post data found'

    return HttpResponse(json.dumps(response), content_type="application/json")


def chatbot(request, template_name="chatbot.html"):
    context = {'title': 'Chatbot Version 1.0'}
    return render(None, template_name, context)


# --------------------------------------------------------
def voca(request):
    vocas = Voca.objects.all()
    paginator = Paginator(vocas, 10)
    now_page = request.GET.get('page')
    vocas = paginator.get_page(now_page)

    context = {"vocas": vocas}

    return render(request, 'voca.html', context)


def search(request):
    search_word = request.GET['search']
    # if ord('가') <= ord(search_word) <= ord('힣'):
    vocas = Voca.objects.filter(
        Q(mean__icontains=search_word) | Q(word__icontains=search_word))
    # else:
    #     vocas = Voca.objects.filter(word__icontains=search_word)

    # paginator=Paginator(vocas,5)
    # now_page=request.GET.get('page')
    # vocas=paginator.get_page(now_page)

    context = {"vocas": vocas}
    return render(request, 'search.html', context)


#단어 테스트임
def voca_test(request):
    vocas_test = Voca.objects.order_by('?')[0]
    context = {"vocas_test": vocas_test}

    return render(request, 'voca_test.html', context)


def test_result(request):
    # user_test_point = Profile.objects.values('user_test_point')
    user = request.user
    profile_obj = Profile.objects.get(user=user)
    test_word = request.GET['test_word']
    test_mean = request.GET['mean']
    flag = "플래그"

    if test_mean == test_word:
        flag = "정답"
        profile_obj.user_test_point = F('user_test_point') + 1
        profile_obj.save()
        context = {"flag": flag}

        return render(request, 'test_result.html', context)
    else:
        flag = "오답"
        context = {"flag": flag}
        context['mean'] = test_mean
        return render(request, 'test_result.html', context)


#----------------------------------


#단어 카테고리 나누기
def voca_cate(request):

    return render(request, 'voca_cate.html')


def voca_elementary(request):
    vocas = Voca.objects.all()
    vocas = Voca.objects.filter(grade='초등')

    paginator = Paginator(vocas, 5)
    now_page = request.GET.get('page')
    vocas = paginator.get_page(now_page)

    context = {"vocas": vocas}
    return render(request, 'voca_elementary.html', context)


def voca_high(request):
    vocas = Voca.objects.all()
    vocas = Voca.objects.filter(grade='중고')

    paginator = Paginator(vocas, 5)
    now_page = request.GET.get('page')
    vocas = paginator.get_page(now_page)

    context = {"vocas": vocas}
    return render(request, 'voca_high.html', context)


def voca_ma(request):
    vocas = Voca.objects.all()
    vocas = Voca.objects.filter(grade='전문')

    paginator = Paginator(vocas, 5)
    now_page = request.GET.get('page')
    vocas = paginator.get_page(now_page)

    context = {"vocas": vocas}
    return render(request, 'voca_ma.html', context)


#----------------------------------
def listen(request):

    return render(request, 'listen.html')


def write(request):

    return render(request, 'write.html')


def pronounce(request):

    return render(request, 'pronounce.html')


def user_profile(request):

    return render(request, 'user_profile.html')
