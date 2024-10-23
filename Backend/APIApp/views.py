from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from APIApp.serializer import *
# KNOX TOKEN
from knox.auth import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
# CUSTOM METHODS
from APIApp.utils import *
from APIApp.common import datatable
import json
from django.db.models import RestrictedError
from APIApp.common.api_response_message import *
from datetime import datetime
from django.db.models import Q
from APIApp.common.pagination import *



# LOGIN FUNCTION ::
class LoginAPI(APIView):
    """
        Summary or Description of the Function:
            * Log-in SuperAdmin.
    """
    def post(self, request, *args, **kwargs):      
        try:
            serializer_class = LoginSerializer(data=request.data, context={'request': request})
            if serializer_class.is_valid():
                user = serializer_class.validated_data['user']
                token = AuthToken.objects.create(user)[1]
                user_data = User.objects.get(user_name = user)
                if user_data:
                    data={  
                        'user_id':user_data.id,
                        'user_name':user_data.user_name,
                        'is_superadmin':user_data.is_superadmin,
                        "message": LOGIN_VERIFIED,
                        "Token": token,
                    }
                return Response(data,status.HTTP_200_OK)
            else:
                return BackendAPIResponse.login_serializer_error(self.__class__.__name__, request, serializer_class)
            
        except Exception as e:
            return BackendAPIResponse.exception_error(self.__class__.__name__, request, e)
        
        
        
        
        
        
# Here Category Views Api logic

class PostCategoryAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        """
        This function posts Category data to a database.
        
        :param request: The `request` parameter in the `post` function is typically an HTTP request
        object that contains information about the request made to the server. It includes data sent by
        the client, such as form data or JSON payload, headers, user authentication details, and other
        metadata related to the request. In this
        :return: The `post` function returns a Response object with the serialized data and a status of
        HTTP 201 CREATED if the serializer is valid and the data is saved successfully. If the
        serializer is not valid, it returns a Response object with the serializer errors and a status of
        HTTP 400 BAD REQUEST. If an exception occurs during the process, it returns an exception error
        response using the `BackendAPIResponse
        """
        try:
            serializer_class = PostCategorySerializer(data=request.data,context={'request':request})
            if serializer_class.is_valid():
                serializer_class.save()
                response = serializer_class.data
                response['status']=status.HTTP_201_CREATED
                response['message']=CommonApiMessages.create('Category')
                return Response(response,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return BackendAPIResponse.exception_error(self.__class__.__name__,request,e)
        
        


class CategoryListDatatableAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        
        """
        The `CategoryListDatatable` class is an API view in Python that retrieves and processes data for a
        datatable related to categories, handling authentication and permissions.
        """
        try:
            query_set = Category.objects.all()
            data_table = json.loads(request.GET.get('data_table'))
            
            serializer_class = GetCategorySerializer
            searchField = ['id','category_name']
            sortFields = ['-id','category_name']
            result = datatable.DataTablesServer(request=data_table,columns=sortFields,qs=query_set,searchField=searchField,\
                serializer=serializer_class).output_result()
            return Response(result,status=status.HTTP_200_OK)
        
        except Exception as e:
            return BackendAPIResponse.exception_error(self.__class__.__name__,request,e)
        
        
class PutCategoryAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,*args, **kwargs):
        """
        Summary or Description of the function:
            Get category data particular id based.
        """
        try:
            cate_id = request.query_params.get('id',0)
            if cate_id != 0:
                query_set = Category.objects.filter(id=cate_id)
            else:
                query_set = Category.objects.all()
            serializer_class = GetCategorySerializer(query_set,many=True)
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return BackendAPIResponse.exception_error(self.__class__.__name__,request,e)
        
    
    def put(self,request,*args,**kwargs):
        """
        Summary or Description of the function:
            Put Category details particular id based.
        """
        try:
            cate_id = request.query_params.get('id')
            data = request.data.copy()
            data['edited_date'] = datetime.now()
            query_set = Category.objects.get(id=cate_id)
            serializer_class = PutCategorySerializer(query_set,data=data,context={'request':request,'id':cate_id},partial=True)
            if serializer_class.is_valid():
                serializer_class.save()
                response = serializer_class.data
                response['status']=status.HTTP_201_CREATED
                response['message']=CommonApiMessages.update('Category')
                return Response(response,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return BackendAPIResponse.exception_error(self.__class__.__name__,request,e)
        
        
    def delete(self,request,*args,**kwargs):
        """
        Summary or Description of the function:
            Delete Category particular Category data to database.
        """
        try:
            id = request.query_params.get('id')
            if id:
                query_set = Category.objects.filter(id=id)
                if query_set.exists():
                    query_set.delete()
                    response_data = {
                        "message": CommonApiMessages.delete("Category"),
                        "status": status.HTTP_200_OK,
                    }
                else:
                    return Response({'message': 'Category is being referenced with another instance',\
                        "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                return Response(
                    data=response_data,
                    status=status.HTTP_200_OK,
                )
            else:
                return Response({'message':PARAMS_MISSING, "status": status.HTTP_400_BAD_REQUEST}\
                    ,status=status.HTTP_400_BAD_REQUEST)

        except RestrictedError:
            return Response(
                data=CommonApiMessages.restrict_delete("Category"),
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        except Exception as e:
            return BackendAPIResponse.exception_error(self.__class__.__name__, request, e)
        
        
        
# Here Product Views Api logic

class PostProductAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        """
        This function posts Product data to a database.
        
        :param request: The `request` parameter in the `post` function is typically an HTTP request
        object that contains information about the request made to the server. It includes data sent by
        the client, such as form data or JSON payload, headers, user authentication details, and other
        metadata related to the request. In this
        :return: The `post` function returns a Response object with the serialized data and a status of
        HTTP 201 CREATED if the serializer is valid and the data is saved successfully. If the
        serializer is not valid, it returns a Response object with the serializer errors and a status of
        HTTP 400 BAD REQUEST. If an exception occurs during the process, it returns an exception error
        response using the `BackendAPIResponse
        """
        try:
            serializer_class = PostProductSerializer(data=request.data,context={'request':request})
            if serializer_class.is_valid():
                serializer_class.save()
                response = serializer_class.data
                response['status']=status.HTTP_201_CREATED
                response['message']=CommonApiMessages.create('Product')
                return Response(response,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return BackendAPIResponse.exception_error(self.__class__.__name__,request,e)
        
        


class ProductListDatatableAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        
        """
        The `ProductListDatatable` class is an API view in Python that retrieves and processes data for a
        datatable related to categories, handling authentication and permissions.
        """
        try:
            query_set = Product.objects.all()
            print(query_set.values('id', 'product_name', 'encrypted_price'),'---------------------------------------')
            data_table = json.loads(request.GET.get('data_table'))
            
            serializer_class = GetProductSerializer
            searchField = ['id','category__category_name','product_name','price','description']
            sortFields = ['-id','category__category_name','product_name','price','description']
            result = datatable.DataTablesServer(request=data_table,columns=sortFields,qs=query_set,searchField=searchField,\
                serializer=serializer_class).output_result()
            return Response(result,status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return BackendAPIResponse.exception_error(self.__class__.__name__,request,e)
        
        
class PutProductAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,*args, **kwargs):
        """
        Summary or Description of the function:
            Get Product data particular id based.
        """
        try:
            product_id = request.query_params.get('id',0)
            if product_id != 0:
                query_set = Product.objects.filter(id=product_id)
            else:
                query_set = Product.objects.all()
            serializer_class = GetProductSerializer(query_set,many=True)
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return BackendAPIResponse.exception_error(self.__class__.__name__,request,e)
        
    
    def put(self,request,*args,**kwargs):
        """
        Summary or Description of the function:
            Put Product details particular id based.
        """
        try:
            product_id = request.query_params.get('id')
            data = request.data.copy()
            data['edited_date'] = datetime.now()
            query_set = Product.objects.get(id=product_id)
            serializer_class = PutProductSerializer(query_set,data=data,context={'request':request,'id':product_id},partial=True)
            if serializer_class.is_valid():
                serializer_class.save()
                response = serializer_class.data
                response['status']=status.HTTP_201_CREATED
                response['message']=CommonApiMessages.update('Product')
                return Response(response,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return BackendAPIResponse.exception_error(self.__class__.__name__,request,e)
        
        
    def delete(self,request,*args,**kwargs):
        """
        Summary or Description of the function:
            Delete Product particular Product data to database.
        """
        try:
            product_id = request.query_params.get('id')
            if product_id:
                query_set = Product.objects.filter(id=product_id)
                if query_set.exists():
                    query_set.delete()
                    response_data = {
                        "message": CommonApiMessages.delete("Product"),
                        "status": status.HTTP_200_OK,
                    }
                else:
                    return Response({'message': 'Product is being referenced with another instance',\
                        "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                return Response(
                    data=response_data,
                    status=status.HTTP_200_OK,
                )
            else:
                return Response({'message':PARAMS_MISSING, "status": status.HTTP_400_BAD_REQUEST}\
                    ,status=status.HTTP_400_BAD_REQUEST)

        except RestrictedError:
            return Response(
                data=CommonApiMessages.restrict_delete("Product"),
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        except Exception as e:
            return BackendAPIResponse.exception_error(self.__class__.__name__, request, e)
        
        
class GetSearchProductApi(APIView):
    def get(self, request):
        try:
            count = int(request.query_params.get("count", 5))
            searchword = request.query_params.get("searchword", "")
            
            # Apply filter based on the searchword
            if searchword:
                queryset = Product.objects.filter(
                    Q(product_name__icontains=searchword) | 
                    Q(category__category_name__icontains=searchword)
                ).order_by('id')  
            else:
                queryset = Product.objects.all().order_by('id')

            
            paginator = ProductPageSizePagination(count)
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            
            # Serialize the paginated queryset
            serializer = GetProductSerializer(
                paginated_queryset,
                many=True,
                context={"request": request},
            )
            response_data = {
                "products": serializer.data,
            }

            return paginator.get_paginated_response(response_data)

        except Exception as e:
            print(str(e))
            return BackendAPIResponse.exception_error(
                self.__class__.__name__, request, e
            )


