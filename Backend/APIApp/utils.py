from APIApp.models import *

#  THIRD PARTY PACKAGE IMPORT
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
import traceback

def Log(transaction_name, msg, Ip, Mode=None, userid=None):
    import socket
    HOSTNAME = socket.gethostname()
    Logs.objects.create(
        transaction_name=transaction_name, mode=Mode, log_message=str(msg),
        user_id=userid,system_name=HOSTNAME, ip_address=Ip
        )
    
class BackendAPIResponse:
    
    @staticmethod
    def login_serializer_error(className, request, serializer, user_id=None):
        Ip = request.META['REMOTE_ADDR']
        msg = {'status': status.HTTP_400_BAD_REQUEST,'message': serializer.errors}
        Log(className, msg, Ip, request.method, user_id)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def serializer_error(className, request, serializer, user_id=None):
        Ip = request.META['REMOTE_ADDR']
        msg = {'status': status.HTTP_400_BAD_REQUEST,'message': serializer.errors}
        Log(className, msg, Ip, request.method, user_id)
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def transaction_error(className, request, error, user_id=None):
        Ip = request.META['REMOTE_ADDR']
        msg = {'status': status.HTTP_400_BAD_REQUEST,'message': error}
        Log(className, msg, Ip, request.method, user_id)
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def exception_error(className, request, e, user_id=None):
        log_msg={'error':str(e),'traceback':traceback.format_exc()}
        Ip = request.META['REMOTE_ADDR']
        mode = None
        Log(className, log_msg, Ip, request.method, user_id)
        error = {'status':status.HTTP_400_BAD_REQUEST, 'message' : 'Something went wrong!'}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def restricted_error(className, request, errorName, user_id=None):
        Ip = request.META['REMOTE_ADDR']
        error_message = f'{errorName} is being referenced with another instance'
       
        error_data = {'status': status.HTTP_409_CONFLICT, 'message': error_message}
        Log(className, request.method, error_data, Ip, user_id)


    @staticmethod
    def validation_error(msg, user_status):
        error_data = {'status':user_status, 'message': msg}
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)