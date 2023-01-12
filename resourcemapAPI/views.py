from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from resourcemap.models import Requests,Rides
from .serializers import ResourceSerializer,ProjectSerializer
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from collections import deque
from datetime import datetime, date, timedelta
import logging
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from users.models import User
from rest_framework.pagination import PageNumberPagination
import collections
logger = logging.getLogger(__file__)

@api_view(['GET'])
def getRequestData(request):
    ## check cookie and authenticate
    token = request.COOKIES.get('jwt')
    print(token)
    paginator = PageNumberPagination()
    paginator.page_size = 5
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    reqs = Requests.objects.filter(requesterid=payload['id'])
    user = User.objects.get(id=payload['id'])
    username = user.name
    result_page = paginator.paginate_queryset(reqs, request)
    serializer = ProjectSerializer(result_page, many=True)
    # return Response({'USER':username,'DATA':serializer.data})
    return paginator.get_paginated_response(serializer.data)
    # once we pass the dictionary in Response the output is JSON data

@api_view(['GET'])
def getRiderData(request):
    ## check cookie and authenticate
    token = request.COOKIES.get('jwt')
    print(token)
    paginator = PageNumberPagination()
    paginator.page_size = 5
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    reqs = Rides.objects.filter(riderid=str(payload['id']))
    user = User.objects.get(id=payload['id'])
    username = user.name
    result_page = paginator.paginate_queryset(reqs, request)
    serializer = ResourceSerializer(result_page, many=True)
    # return Response({'USER':username,'DATA':serializer.data})
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def getAllRiderData(request):
    ## check cookie and authenticate
    token = request.COOKIES.get('jwt')
    print(token)
    paginator = PageNumberPagination()
    paginator.page_size = 5
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    reqs = Rides.objects.all()
    # user = User.objects.get(id=payload['id'])
    # username = user.name
    result_page = paginator.paginate_queryset(reqs, request)
    serializer = ResourceSerializer(result_page, many=True)
    # return Response({'USER':username,'DATA':serializer.data})
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def addrequest(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    # projects = Requests.objects.filter(requesterid=payload['id'])
    if 'riderid' in request.data:
        raise AuthenticationFailed('Unauthenticated!')
    request.data['riderid']=payload['id']
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def addrider(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    # projects = Requests.objects.filter(requesterid=payload['id'])
    if 'riderid' in request.data:
        raise AuthenticationFailed('Unauthenticated!')
    request.data['riderid']=payload['id']
    serializer = ResourceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


def clear(request):
    token = request.COOKIES.get('jwt')
    print(token)
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    p = Requests.objects.filter(requesterid=payload['id'])
    for i in p:
        i.status="Pending"
        i.save()
    context = {"Data has been cleared": "Completed"}
    return JsonResponse(context)

def clear1(request):
    token = request.COOKIES.get('jwt')
    print(token)
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    p = Requests.objects.filter(requesterid=payload['id'])
    for i in p:
        if i.status=="APPLIED":
            i.status="PENDING"
            i.save()
def updateDB(request,mapdic):
    clear1(request)
    for req_id in mapdic:
        t = Requests.objects.get(id=req_id)
        if t.status.lower()=="pending":
            t.status = "APPLIED"  # change field
        t.save() # this will update only


@api_view(['GET'])
def mapResource(request):
    try:
        token = request.COOKIES.get('jwt')
        print(token)
        paginator = PageNumberPagination()
        paginator.page_size = 5
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        projects = Requests.objects.filter(requesterid=payload['id'])
        resources = Rides.objects.all()
        p=projects.count()
        r=resources.count()
        # r=0
        if p==0:
            logger.info("Inside Map Resource and No project is available")
            return Response({'REQUESTS AVAILABILITY':'NO REQUEST IS AVAILABLE'},status=status.HTTP_204_NO_CONTENT)
        if r==0:
            logger.info("Inside Map Resource and No resource is available to map")
            return Response({'RIDERS AVAILABILITY':'NO RIDERS IS AVAILABLE TO MAP ON PROJECTS'},status=status.HTTP_204_NO_CONTENT)
        
        
        resource_data1 = list(Rides.objects.all().values_list('riderid','fromplace', 'toplace', 'dateandtime','quantity'))
        request_data1 = list(Requests.objects.filter(requesterid=payload['id']).values_list('id','fromplace','toplace','dateandtime','numberassets','status'))
        resource_data,request_data=[],[]
        for i in resource_data1:
            resource_data.append(list(i))
        for i in request_data1:
            request_data.append(list(i))
        mapDict={}
        reqs_update=[]
        for req_id,req_from,req_to,req_date,req_quantity,req_status in request_data:
            flag=False
            if req_status.lower()=='expired': continue
            for i in range(len(resource_data)):
                res_id, res_from,res_to,res_date,res_quantity = resource_data[i]
                if res_from==req_from and req_to==res_to and req_date==res_date and req_quantity<=res_quantity:
                    # if req_id not in mapDict:
                    flag=True
                    name= User.objects.get(id=res_id).name
                    mapDict[req_id]={'RIDER_ID': res_id, 'NAME':name, 'FROM':res_from,'TO':res_to,'DATE and TIME': res_date, 'QUANTITY':req_quantity}
                    reqs_update.append(req_id)
                    print(mapDict)
                    resource_data[i][4]-=req_quantity
                    print('----------')
                    print(resource_data,'----------')
                    print('----------')
                    break
            if not flag:
                mapDict[req_id]={'RIDERS AVAILABE': 0}
        updateDB(request,reqs_update)
        return Response(mapDict)
    except:
        content = {'DATABASE NAME OR ENTRIES ARE INVALID':"PLEASE RAISE THE TICKET"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
                
                    


        







