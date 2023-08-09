from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView,api_view
from responseHelper import incompleteDetailsResponse,finalResponse,logouthelper
from .models import UserModel
from bcrypt import hashpw,checkpw,gensalt
from sendMailHelper import sendOTPEmail
from django.utils import timezone
from datetime import timedelta
from .Serializers import userModelSerializer
import random
from .Helper.jwtHelper import generate_jwt_token,verify_jwt_token
# Create your views here.

class testView(APIView):
   
    def post(self, request, *args, **kwargs):
        print("hello")
        data=request.data
        return Response(data={"success":True,"data":data,"message":"testing api is working"})
    
    def get(self,request,*agrs,**kwargs):
       data= UserModel.objects.all().delete()
       return   Response(data={"success":True,"data":data,"message":"delete api is working"})
    
#create registration routes
class userRegister(APIView):
    def post(self,request,*args,**kwargs):
        # get data from the body
        name=request.data.get("name")
        email=request.data.get("email")
        password=request.data.get("password")
        role=request.data.get("role")
        #check if any detail is missing
        if(name is None or email is None or password is None):return incompleteDetailsResponse()
        
        #check if user already exists or not
        check=UserModel.objects.filter(email=email)
        if(len(check)>0):return finalResponse(success=False,data=[],message="user already exists",status_code=400)
        
        # hash the password
        hash_password=hashpw(password.encode("utf-8"), gensalt())
        
        #generate OTP
        otp=random.randint(1001,9999)
        
        # if all details are provided  create user and send otp for verification
        user=UserModel(name=name,email=email,password=hash_password)
        if(role is not None and (role=="edge" or role=="admin")): user.role=role
        # send the mail
        result=sendOTPEmail(emailTo=email,name=name,otp=otp)
        
        #save otp and ot expire  in user and create it
        user.otp=otp
        user.otpExpire= timezone.now()+timedelta(minutes=10)
        user.save()
        
        #return the result
        return finalResponse(True,result,"verification otp sent",201)
        
        
class VerfiyOTP(APIView):
    def post(self,request,*args,**kwargs):
        #get otp from params
        otp=request.data.get("otp")
        email=request.data.get("email")
        two_factor_auth=request.data.get("two_factor_auth")
        #if otp not present send incomplete details response
        if(otp is None or otp == "" or email is None or two_factor_auth is None):return incompleteDetailsResponse()               
        
        #check if user exists
        user=UserModel.objects.filter(email=email).first()
        print(user)
        if(user is None):return finalResponse(False,[],"user doesn't exists",400)
        
        #verify 
        
        if(user.otp!=otp):return finalResponse(False,[],"invalid otp",400)
        if(user.otpExpire<timezone.now()):return finalResponse(False,[],"otp expired",400)
        
        user.otp="";user.otpExpire=None
        user.is_verified=True;user.is_active=True
        user.is_two_factor_auth_enabled=two_factor_auth
        user.save()
        #serialize the data
        serialized_data=userModelSerializer(user,many=False)
         
        #create token and set it into cookies
        token=generate_jwt_token(user.id)
         
        
        # send response
        return finalResponse(True,serialized_data.data,"user verified successfull",201,token=token)
       

class resendOTP(APIView):
    def get(self,request,*args,**kwargs):
        email=request.query_params.get("email") or request.data.get("email")
        if(email is None): return incompleteDetailsResponse()
        
         #check if user exists
        user=UserModel.objects.filter(email=email).first()
        if(user is None):return finalResponse(False,[],"user doesn't exists",400)
        
        #generate OTP
        otp=random.randint(1001,9999)
        
        # send the mail
        result=sendOTPEmail(emailTo=email,name=user.name,otp=otp)
        
        #save otp and ot expire  in user and create it
        user.otp=otp
        user.otpExpire= timezone.now()+timedelta(minutes=10)
        user.save()
        
        #return the result
        return finalResponse(True,result,"verification otp sent",201)
                 
                 
class logout(APIView):
    def get(self,request,*args,**kwargs):
        email=request.query_params.get("email")
        
        if(email is None): return incompleteDetailsResponse()
        user=UserModel.objects.filter(email=email).first()
        
        if(user is None): return finalResponse(False,[],"user doesn't exists",400)
        
        user.is_active=False
        user.save()
        return  logouthelper()
                          
                          
                          
class login(APIView):
     def post(self,request,*args,**kwargs):
        #  get data from the body
        email=request.data.get("email")
        password=request.data.get("password")
        
        #check if any detail is missing
        if( email is None or password is None):return incompleteDetailsResponse()
        
        #check if user already exists or not
        user=UserModel.objects.filter(email=email).first()
        if(user is None ):return finalResponse(success=False,data=[],message="user doesn't exists",status_code=404)
        
        #match password
        print(user.password)
        if(checkpw(password=password.encode("utf-8"),hashed_password=user.password)==False):return finalResponse(success=False,data=[],message="invalid credentials",status_code=401)
        
        
        # check if 2nd factor auth is enabled
        if(user.is_two_factor_auth_enabled): 
             otp=random.randint(1001,9999)
        
        # send the mail
        result=sendOTPEmail(emailTo=email,name=user.name,otp=otp)
        
        #save otp and ot expire  in user and create it
        user.otp=otp
        user.otpExpire= timezone.now()+timedelta(minutes=10)
        user.save()
        
        #return the result
        return finalResponse(True,result,"verification otp sent",201)
                 
            
       
      
       
        

class forgetPassword(APIView):
    def post(self,request,*args,**kwargs):
        otp=request.data.get("otp")
        password=request.data.get("password")         
        email=request.data.get("email")   
        
        # check for complete details
        if(otp is None or otp=="" or password is None or email is None): return incompleteDetailsResponse()
        
        # check for user existance
        user=UserModel.objects.filter(email=email).first()
        
        if(user is None ):return finalResponse(success=False,data=[],message="user doesn't exists",status_code=404)
        
        #check if otp 
        if(user.otp!=otp or user.otpExpire is None or user.otpExpire<timezone.now()):return finalResponse(success=False,data=[],message="otp invalid",status_code=404)      
        
        #change the password
        hash_password=hashpw(password.encode("utf-8"), gensalt())        
        
        user.password=hash_password
        user.otp="";user.otpExpire=None
        user.save()
        return finalResponse(success=True,data=[],message="password changed successfullt",status_code=200)
                              