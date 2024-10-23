from django.shortcuts import render,redirect
from Web.utils import *
from Web.response_message import *
from django.contrib import messages
from django.conf import settings
import requests
import json
from django.http import JsonResponse
from django.urls import reverse

url = settings.BACK_END_URL

# Create your views here.

def login(request):
    """
    Summary or Description of the Function:
        * Admin login data and the bind data to input field.
    Method: POST
    """
    try:
        if request.method == "POST":
            data = {}
            context = {}
            
            # Get username and password from the request
            given_input = request.POST.get('txtusername')
            data['user_name'] = given_input
            password = request.POST.get('txtpassword')
            data['password'] = password
            
            # Send a POST request to the login URL
            login_data = requests.post(f'{url}/login/', data=data)
            user_data = login_data.json()

            # Handle the response based on the status code
            if login_data.status_code == 200:
                # Save user data in session
                request.session['Token'] = user_data.get('Token')
                request.session['User_id'] = user_data.get('user_id')
                request.session['User_name'] = user_data.get('user_name')
                request.session['isSuperAdmin'] = user_data.get('is_superadmin')
                messages.success(request, EventMessages.login())
                return redirect('create-category')
            else:
                # Handle login errors
                error_msg = user_data.get('message', ['An unknown error occurred.'])[0]
                if error_msg == 'Password is incorrect..!':
                    context['pwd_error_msg'] = error_msg
                else:
                    context['error_msg'] = error_msg
                messages.error(request, LOGIN_FAILED)
                return render(request, 'auth/login.html', context=context)
        else:
            return render(request, 'auth/login.html')
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        messages.error(request, "An unexpected error occurred. Please try again.")
        return render(request, 'auth/login.html')
    
    
def logout(request):
    try:
        request.session.flush()
        messages.success(request,EventMessages.logout())
        return redirect('/')
    
    except Exception as e:
        print(f"An error occurred during logout: {str(e)}")
        messages.error(request, "An error occurred while logging out. Please try again.")
        


# -----------------Category--------------------
def create_category(request):
    """
    Handles the creation or updating of categories based on user input.
    If an ID is provided, it updates the existing category; otherwise, it creates a new one.
    """
    try:
        user_id = request.session["User_id"]
        headers = WebResponse.Token_Authentication(request)

        if request.method == "POST":
            category = request.POST.get('txtcategory')
            hd_cate_id = request.POST.get('hd_cate_id')
            data = {'category_name': category}

            if hd_cate_id:
                # Update existing category
                data['editedby'] = user_id
                params = {"id": hd_cate_id}
                put_data = requests.put(f'{url}/put-category/', data=data, headers=headers, params=params)
                data = put_data.json()
                data['status'] = put_data.status_code
                return JsonResponse(data,safe=False)
                
            else:
                # Create new category
                data['createdby'] = user_id
                post_data = requests.post(f'{url}/post-category/', data=data, headers=headers)
                data = post_data.json()
                data['status'] = post_data.status_code
                return JsonResponse(data,safe=False)
            
        else:
            return render(request,'mypanel/category-list.html')
    except KeyError:
        return JsonResponse({'error': 'User ID not found in session.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)

            
    

def category_list_datatable(request):
    """
    Retrieves the category list and returns it as a JSON response.
    """
    user_id = request.session.get("User_id")  # Use get to avoid KeyError
    headers = WebResponse.Token_Authentication(request)

    try:
        data_tbl = dict(request.GET)
        params = {"data_table": json.dumps(data_tbl)}

        # Send GET request to fetch categories
        response = requests.get(
            f"{url}/getall-category-list/",
            headers=headers,
            params=params,
        )

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'error': 'Failed to fetch category list.', 'details': response.text}, status=response.status_code)

    except Exception as e:
        print(f"An error occurred while fetching category list: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)

        
def delete_category(request):
    """
    Deletes a category based on the provided category ID.
    Redirects to the category creation page with a success or error message.
    """
    try:
        user_id = request.session.get("User_id")
        headers = WebResponse.Token_Authentication(request)
        category_id = request.GET.get("category_id")

        # Check if category_id is provided
        if not category_id:
            messages.error(request, "Category ID is required.")
            return redirect("create-category")

        params = {"id": category_id, 'user_id': user_id}

        # Send DELETE request to delete the category
        response = requests.delete(
            f"{url}/delete-category/",
            headers=headers,
            params=params,
        )

        # Handle response based on status code
        if response.status_code == 200:
            messages.success(request, EventMessages.delete("Category"))
            return redirect("create-category")

        elif response.status_code == 400:
            error_message = response.json().get("message", "Bad request.")
            messages.error(request, error_message)
            return redirect("create-category")

        else:
            messages.error(request, "An error occurred while deleting the category.")
            return redirect("create-category")

    except Exception as e:
        print(f"An error occurred while deleting the category: {str(e)}")
        messages.error(request, "An unexpected error occurred. Please try again.")
        return redirect("create-category")

        
def get_category(request):
    """
    Summary or Description of the Function:
        * Get Category.
    """

    try:
        headers = WebResponse.Token_Authentication(request)
        category_id = request.GET.get("category_id")

        params = {"id": category_id}

        data = requests.get(
            "{url}/get-category/".format(url=url),
            headers=headers,
            params=params,
        ).json()[0]
        return JsonResponse(data,safe=False)

    except Exception as e:
        print(f"An error occurred while deleting the category: {str(e)}")
        messages.error(request, "An unexpected error occurred. Please try again.")
        return redirect("/create/category/")
        

# -----------------Product--------------------
def create_product(request):
    """
    Handles the creation or updating of product based on user input.
    If an ID is provided, it updates the existing product; otherwise, it creates a new one.
    """
    try:
        user_id = request.session["User_id"]
        headers = WebResponse.Token_Authentication(request)
        if request.method == "POST":
            category = request.POST.get('ddlcategory')
            product = request.POST.get('txt_product_name')
            desc = request.POST.get('txtdesc')
            price = request.POST.get('txt_price')
            hd_product_id = request.POST.get('hd_product_id')
            data = {'category':category,'product_name':product,'price':price,'description':desc if desc !="" else None}
            if hd_product_id:
                data['editedby'] = user_id
                params = {"id": hd_product_id}
                put_data = requests.put('{url}/put-product/'.format(url=url),data=data,headers=headers,params=params)
                data = put_data.json()
                data['status'] = put_data.status_code
                return JsonResponse(data,safe=False)
            else:
                data['createdby'] = user_id
                post_data = requests.post('{url}/post-product/'.format(url=url),data=data,headers=headers)
                data = post_data.json()
                data['status'] = post_data.status_code
                return JsonResponse(data,safe=False)
        else:
            data = requests.get(
                "{url}/get-category/".format(url=url),
                headers=headers,
            ).json()
            context = {'category':data}
            return render(request,'mypanel/product-list.html',context=context)
            
    except Exception as e:
        print(f"An error occurred while deleting the product: {str(e)}")
        messages.error(request, "An unexpected error occurred. Please try again.")
        return redirect("create-product")
    
def product_list_datatable(request):
    """
    Retrieves the product list and returns it as a JSON response.
    """
    user_id = request.session.get("User_id")  # Use get to avoid KeyError
    headers = WebResponse.Token_Authentication(request)

    try:
        data_tbl = dict(request.GET)
        params = {"data_table": json.dumps(data_tbl)}

        # Send GET request to fetch categories
        response = requests.get(
            f"{url}/get-datatable-productlist/",
            headers=headers,
            params=params,
        )

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'error': 'Failed to fetch product list.', 'details': response.text}, status=response.status_code)

    except Exception as e:
        print(f"An error occurred while fetching product list: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)

        
def delete_product(request):
    """
    Deletes a product based on the provided product ID.
    Redirects to the product creation page with a success or error message.
    """
    try:
        user_id = request.session.get("User_id")
        headers = WebResponse.Token_Authentication(request)
        product_id = request.GET.get("product_id")

        # Check if product_id is provided
        if not product_id:
            messages.error(request, "product ID is required.")
            return redirect("create-product")

        params = {"id": product_id, 'user_id': user_id}

        # Send DELETE request to delete the product
        response = requests.delete(
            f"{url}/delete-product/",
            headers=headers,
            params=params,
        )

        # Handle response based on status code
        if response.status_code == 200:
            messages.success(request, EventMessages.delete("product"))
            return redirect("create-product")

        elif response.status_code == 400:
            error_message = response.json().get("message", "Bad request.")
            messages.error(request, error_message)
            return redirect("create-product")

        else:
            messages.error(request, "An error occurred while deleting the product.")
            return redirect("create-product")

    except Exception as e:
        print(f"An error occurred while deleting the product: {str(e)}")
        messages.error(request, "An unexpected error occurred. Please try again.")
        return redirect("create-product")

        
def get_product(request):
    """
    Summary or Description of the Function:
        * Get product.
    """

    try:
        headers = WebResponse.Token_Authentication(request)
        product_id = request.GET.get("product_id")

        params = {"id": product_id}

        data = requests.get(
            "{url}/get-product/".format(url=url),
            headers=headers,
            params=params,
        ).json()[0]
        return JsonResponse(data,safe=False)

    except Exception as e:
        print(f"An error occurred while deleting the product: {str(e)}")
        messages.error(request, "An unexpected error occurred. Please try again.")
        return redirect("create-product")
    
    
def product_list_page(request):
    try:
        return render(request, 'mypanel/product.html')
    
    except Exception as e:
       return JsonResponse({'error': str(e)}, status=500)
    
    
def search_related_Product_results(request):
    try:
        headers = WebResponse.Token_Authentication(request)
        page = request.GET.get('page')
        count = request.GET.get('count')
        searchword = request.GET.get('searchword')
        params = {
            'count':count,
            'searchword':searchword,
            'page':page,
        }
        response = requests.get(
                "{url}/search-product/".format(url=url),
                headers=headers,
                params=params,
            ).json()
        return JsonResponse(response,safe=False)
    
    except Exception as e:
            messages.error(request, "An unexpected error occurred. Please try again.")
    

