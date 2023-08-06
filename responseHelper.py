from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta


def incompleteDetailsResponse():
    return Response({"success":False,"message":"incomplete details"},status=400)
 
def finalResponse(success:bool,data,message:str,status_code,token=""):
    expiry_datetime = timezone.now()  + timezone.timedelta(days=1)
    response= Response(data={"success":success,"data":data,"message":message},status=status_code)
    if(len(token)>0):response.set_cookie(key="token",value=token,expires=expiry_datetime,httponly=True)
    return response 


def logouthelper():
    response=Response(data={"success":True,"message":"user logged out successfully"},status=200)
    response.set_cookie(key="token",value="NULL",expires=timezone.now(),httponly=True)
    return response