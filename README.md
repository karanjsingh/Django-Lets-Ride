# Django-Lets-Ride

## ABOUT

There will be 2 persons one is a Rider and the other is an Asset Transportation Requester (will be referred as requester from now on). 
A Rider is a person who travels from one place to another and is willing to carry some assets(packages/luggages) along with him. 
A Requester is a person who wants his assets to be carried by someone else from one place to another. 
Requesters can create transportation requests and Riders can share their rides independently

## BASIC REQUIREMENTS:	

Features	
* A Rider can share his travel info with details like from and to locations, the number of assets he can take with him etc. 
* Requesters can request to carry their assets, with details like from and to locations, the type of assets, number of assets that need to be carried.
* A Requester should be able to see all the asset transportation requests requested by him. 
* A Requester should be able to see all the matching travel info shared by Riders based on his asset transportation requests locations. 
* A Requester can apply to carry his assets by a Rider.

## Tech Stack:
 * Django
 * Django Rest Framework
 

## API

User API's
  * USER REGISTER: http://127.0.0.1:8000/user/register/
  * USER LOGIN : http://127.0.0.1:8000/user/login/
  * USER INFO: http://127.0.0.1:8000/user/user/

Application API's:
* GET YOUR REQUESTS: http://127.0.0.1:8000/api/requests/
* GET YOUR RIDES REQUESTS: http://127.0.0.1:8000/api/rides/
* GET ALL RIDERS INFORMATION: http://127.0.0.1:8000/api/allriders/
* ADD PACKAGE REQUEST: http://127.0.0.1:8000/api/addreq/
* ADD RIDE REQUEST: http://127.0.0.1:8000/api/addride/
* MAP PACKAGE REQUESTS WITH RIDERS AVAILABLE: http://127.0.0.1:8000/api/mapresource/




