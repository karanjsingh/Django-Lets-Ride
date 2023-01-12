from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from .forms import RequesterForm,RiderForm
from django.contrib import messages
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
import jwt, datetime
from users.serializers import UserSerializer
from .models import Requests,Rides
import datetime
# from users.views import UserView

def querydict_to_dict(query_dict):
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        data[key] = v
    return data

def requester_index(request):
    return render(request, 'post_request.html', context={"form1":RequesterForm()})

def rider_index(request):
    return render(request, 'rider_request.html', context={"form1":RiderForm()})

def rider_entry(request):
    Dict=querydict_to_dict(request.GET)
    FROM = Dict['FROM'][0]
    TO = Dict['TO'][0]
    DATE_TIME = Dict['DATE_TIME'][0]
    TRAVEL_MEDIUM = Dict['TRAVEL_MEDIUM'][0]
    ASSET_COUNT = Dict['ASSET_COUNT'][0]
    ## check cookie and authenticate
    token = request.COOKIES.get('jwt')
    print(token)
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    print(payload,payload['id'])
    # user = User.objects.filter(id=payload['id']).first()
    Rides.objects.create(riderid=payload['id'], fromplace=FROM, toplace=TO,
                        dateandtime=DATE_TIME, travelmedium=TRAVEL_MEDIUM,
                        quantity=ASSET_COUNT)
    messages.success(request, f'Entry is Created')
    return HttpResponseRedirect('/form/rider/')

def req_entry(request):
    Dict=querydict_to_dict(request.GET)
    FROM = Dict['FROM'][0]
    TO = Dict['TO'][0]
    DATE_TIME = Dict['DATE_TIME'][0]
    ASSET_SENSITIVITY = Dict['ASSET_SENSITIVITY'][0]
    ASSET_COUNT = Dict['ASSET_COUNT'][0]
    WHOME_TO_DELIVER = Dict['WHOME_TO_DELIVER'][0]
    ASSET_TYPE = Dict['ASSET_TYPE'][0]
    STATUS= "PENDING"
    today = datetime.datetime.now()
    datetime_str = datetime.datetime.strptime(DATE_TIME, '%Y-%m-%d')   ## convert str to datetime
    if datetime_str-today<datetime.timedelta(hours=5):
        STATUS="EXPIRED"
    ## check cookie and authenticate
    token = request.COOKIES.get('jwt')
    print(token)
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    # user = User.objects.filter(id=payload['id']).first()
    Requests.objects.create(requesterid=payload['id'],fromplace=FROM, toplace=TO,
                        dateandtime=DATE_TIME, status=STATUS, assettype=ASSET_TYPE,
                        numberassets=ASSET_COUNT,todeliverperson=WHOME_TO_DELIVER,packagesensitivity=ASSET_SENSITIVITY)
    # flag = Dict["result[flag]"][0]
    messages.success(request, f'Entry is Created')

    return HttpResponseRedirect('/form/request/')

def showRiderData(request):
    token = request.COOKIES.get('jwt')
    print(token)
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    # MODEL_HEADERS=[f.name for f in Rides._meta.get_fields()]
    # MODEL_HEADERS.pop(0)
    # MODEL_HEADERS.pop(0)
    MODEL_HEADERS = ['FROM','TO', 'DATE AND TIME', 'TRAVEL MEDIUM', 'NUMBER OF ASSET']
    query_results = [list(i.values()) for i in list(Rides.objects.filter(riderid=str(payload['id'])).values('fromplace', 'toplace', 'dateandtime','travelmedium','quantity'))]
    #return a response to your template and add query_results to the context
    return render(request, "TABLEOFINTEREST.html", {
            "query_results" : query_results,
            "model_headers" : MODEL_HEADERS
        }) 

def showRequestData(request):
    token = request.COOKIES.get('jwt')
    print(token)
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    ## checking if any entry is expired or not
    data = Requests.objects.filter(requesterid=payload['id'])
    today = datetime.date.today()
    for i in data:
        # datetime_str = datetime.datetime.strptime(i.dateandtime, '%Y-%m-%d')   ## convert str to datetime
        # print(i.fromplace,i.dateandtime-today)
        if i.status.lower()=="pending" and i.dateandtime-today<datetime.timedelta(hours=1):
            i.status="EXPIRED"
            i.save()
    MODEL_HEADERS = ['FROM','TO', 'DATE AND TIME', 'NUMBER OF ASSET', 'ASSET TYPE', 'ASSET SENSITIVITY', 'WHOME TO DELIVER', 'ACCEPTED PERSON DETAIL', 'STATUS' ]
    query_results = [list(i.values()) for i in list(Requests.objects.filter(requesterid=payload['id']).values('fromplace', 'toplace', 'dateandtime','numberassets','assettype','packagesensitivity','todeliverperson','deliverby','status'))]
    
    return render(request, "TABLEREQUESTS.html", {
            "query_results" : query_results,
            "model_headers" : MODEL_HEADERS
        })

def showAllRiderData(request):
    token = request.COOKIES.get('jwt')
    print(token)
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    # MODEL_HEADERS=[f.name for f in Rides._meta.get_fields()]
    # MODEL_HEADERS.pop(0)
    # MODEL_HEADERS.pop(0)
    MODEL_HEADERS = ['FROM','TO', 'DATE AND TIME', 'TRAVEL MEDIUM', 'NUMBER OF ASSET']
    query_results = [list(i.values()) for i in list(Rides.objects.all().values('fromplace', 'toplace', 'dateandtime','travelmedium','quantity'))]
    #return a response to your template and add query_results to the context
    return render(request, "TABLEOFINTEREST.html", {
            "query_results" : query_results,
            "model_headers" : MODEL_HEADERS
        }) 