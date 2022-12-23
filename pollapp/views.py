import json
from django.shortcuts import render,get_object_or_404
from portalsdk import APIContext, APIMethodType, APIRequest
from time import sleep

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from .models import Question, Choice
from django.http import Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
import requests



class IndexView(generic.ListView):
    template_name = 'pollapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'pollapp/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pollapp/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'pollapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('pollapp:results', args=(question.id,)))

def consume_rest_api(request):
    response=requests.get('https://cso-app.herokuapp.com/csos')
    users=response.json()

    context={'users':users}
    print(users)
    return render(request, "pollapp/users.html",context)
    pass


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'pollapp/index.html', context)


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context={'question': question}
#     return render(request, 'pollapp/detail.html', context)

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'pollapp/results.html', {'question': question})


from portalsdk import APIContext, APIMethodType, APIRequest
from time import sleep


def c2b(request):
  # Public key on the API listener used to encrypt keys
  public_key = 'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArv9yxA69XQKBo24BaF/D+fvlqmGdYjqLQ5WtNBb5tquqGvAvG3WMFETVUSow/LizQalxj2ElMVrUmzu5mGGkxK08bWEXF7a1DEvtVJs6nppIlFJc2SnrU14AOrIrB28ogm58JjAl5BOQawOXD5dfSk7MaAA82pVHoIqEu0FxA8BOKU+RGTihRU+ptw1j4bsAJYiPbSX6i71gfPvwHPYamM0bfI4CmlsUUR3KvCG24rB6FNPcRBhM3jDuv8ae2kC33w9hEq8qNB55uw51vK7hyXoAa+U7IqP1y6nBdlN25gkxEA8yrsl1678cspeXr+3ciRyqoRgj9RD/ONbJhhxFvt1cLBh+qwK2eqISfBb06eRnNeC71oBokDm3zyCnkOtMDGl7IvnMfZfEPFCfg5QgJVk1msPpRvQxmEsrX9MQRyFVzgy2CWNIb7c+jPapyrNwoUbANlN8adU1m6yOuoX7F49x+OjiG2se0EJ6nafeKUXw/+hiJZvELUYgzKUtMAZVTNZfT8jjb58j8GVtuS+6TM2AutbejaCV84ZK58E2CRJqhmjQibEUO6KPdD7oTlEkFy52Y1uOOBXgYpqMzufNPmfdqqqSM4dU70PO8ogyKGiLAIxCetMjjm6FCMEA3Kc8K0Ig7/XtFm9By6VxTJK1Mg36TlHaZKP6VzVLXMtesJECAwEAAQ=='
  # Create Context with API to request a Session ID
  api_context = APIContext()
  # Api key
  api_context.api_key = 'tew2tgIZFu3rg3VexEXSlqGcBKwSS0GJ'
  # Public key
  api_context.public_key = public_key
  # Use ssl/https
  api_context.ssl = True
  # Method type (can be GET/POST/PUT)
  api_context.method_type = APIMethodType.GET
  # API address
  api_context.address = 'openapi.m-pesa.com'
  # API Port
  api_context.port = 443
  # API Path
  api_context.path = '/sandbox/ipg/v2/vodacomTZN/getSession/'

  # Add/update headers
  api_context.add_header('Origin', '*')

  # Parameters can be added to the call as well that on POST will be in JSON format and on GET will be URL parameters
  # api_context.add_parameter('key', 'value')

  #Do the API call and put result in a response packet
  api_request = APIRequest(api_context)

  # Do the API call and put result in a response packet
  result = None
  try:
      result = api_request.execute()
  except Exception as e:
      print('Call Failed: ' + str(e))

  if result is None:
      raise Exception('SessionKey call failed to get result. Please check.')

  # Display results
  print(result.status_code)
  print(result.headers)
  print(result.body)

  # The above call issued a sessionID which will be used as the API key in calls that needs the sessionID
  api_context = APIContext()
  api_context.api_key = result.body['output_SessionID']
  api_context.public_key = public_key
  api_context.ssl = True
  api_context.method_type = APIMethodType.POST
  api_context.address = 'openapi.m-pesa.com'
  api_context.port = 443
  api_context.path = '/sandbox/ipg/v2/vodacomTZN/c2bPayment/singleStage/'

  api_context.add_header('Origin', '*')

  api_context.add_parameter('input_Amount', '10')
  api_context.add_parameter('input_Country', 'TZN')
  api_context.add_parameter('input_Currency', 'TZS')
  api_context.add_parameter('input_CustomerMSISDN', '000000000001')
  api_context.add_parameter('input_ServiceProviderCode', '000000')
  api_context.add_parameter('input_ThirdPartyConversationID', 'asv02e5958774f7ba228d83d0d689761')
  api_context.add_parameter('input_TransactionReference', 'T1234C')
  api_context.add_parameter('input_PurchasedItemsDesc', 'Shoes')
  
  api_request = APIRequest(api_context)

  # SessionID can take up to 30 seconds to become 'live' in the system and will be invalid until it is
  sleep(30)

  result = None
  try:
      result = api_request.execute()
  except Exception as e:
      print('Call Failed: ' + str(e))

  if result is None:
      raise Exception('API call failed to get result. Please check.')

  print(result.status_code)
  print(result.headers)
  print(result.body) 

  return render(request,'pollapp/mpesa.html',{'result':result})   

# if __name__ == '__main__':
#   main()