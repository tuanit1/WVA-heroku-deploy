import requests as rq
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import main.base64_change as bs
import base64
from django.core.paginator import Paginator
from Constant import SERVER_URL
import requests
import json

# Create your views here.
def decode_Item_cate(category):
    category['cat_id'] = int(category['cat_id'])
    category['cat_name'] = bs.decode_Str(category['cat_name'])
    category['cat_image'] = bs.decode_Str(category['cat_image'])
    category['cat_type'] = int(category['cat_type'])
    category['cat_status'] = int(category['cat_status'])
    return category

def decode_Cate(categories):
    for category in categories:
        category = decode_Item_cate(category)
    return categories

def getCategory(id):
    postObj = {
        'method_name': 'GET_CATE_BYID',
        'cate_id': id
    }

    data = {
        'data': json.dumps(postObj)
    }

    res = requests.post(SERVER_URL , data = data)
    return_obj = json.loads(res.content)

    return return_obj['category'] if return_obj['status'] == "success" else []

def category(request , pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    postObj = {
        'method_name': 'LOAD_CATEGORT',
        'type':pk,
        'search_txt': q
    }

    data = {
        'data': json.dumps(postObj)
    }

    res = requests.post(SERVER_URL , data = data)
    return_obj = json.loads(res.content)

    categories = return_obj['category'] if return_obj['status'] == "success" else []

    categories_de = decode_Cate(categories)
    p = Paginator(categories_de, 8)
    page = request.GET.get('page') 
    list_cats = p.get_page(page)
    nums = "a" * list_cats.paginator.num_pages
    context = {'list_cats':list_cats, 'nums': nums, 'choice':pk}
    return render(request, 'category/category.html', context)

@login_required(login_url='/login')
def addCategory(request, pk):
    if request.method == 'POST':

        if 'file_img' in request.FILES:
            print("update image")

            url = SERVER_URL + '/uploadImage.php'
            files = {'file': request.FILES['file_img']}
            data = {'crr': request.POST.get('thumbnail')}
            res = rq.post(url, files=files, params=data)
        
            js = json.loads(res.content)
            if(js['status'] == 1):
                image_dir = SERVER_URL + '/image/'+js['dir'];
                thumbnail = base64.b64encode(image_dir.encode('utf-8')).decode('utf-8')
            else:
                messages.error(request, "Something wrong when upload image, please try again!")
                return redirect('videoapp:create')
        else:
            messages.error(request, "Thumbnail is required!")
            return redirect('videoapp:create')
            
        postObj = {
            'method_name': 'ADD_CATEGORY',
            'cat_name':bs.encode_Str(request.POST.get('Name')), 
            'cat_image': thumbnail,
            'cat_type':pk, 
            'status':request.POST.get('status')
        }

        data = {
            'data': json.dumps(postObj)
        }
        res = requests.post(SERVER_URL , data = data)
        return_obj = json.loads(res.content)
        print(return_obj)
        if str(return_obj) == "success":
            return redirect('category:category', pk)
        else:
            return HttpResponse("Error")
    else:
        page = 'add'
        context = {'page': page, 'choice':pk}
        return render(request, 'category/categorydetail.html', context)

@login_required(login_url='/login')
def editCategory(request, pk, id):
    
    category = getCategory(id)
    category = decode_Item_cate(category)
    if request.method == 'POST':

        thumbnail = bs.encode_Str(request.POST.get('thumbnail'))

        #check user update image
        if 'file_img' in request.FILES:
            print("update imageeeeeeeeeeeeeeeeeee")

            url = SERVER_URL + '/uploadImage.php'
            files = {'file': request.FILES['file_img']}
            data = {'crr': request.POST.get('thumbnail')}
            res = rq.post(url, files=files, params=data)
        
            js = json.loads(res.content)
            if(js['status'] == 1):
                image_dir = SERVER_URL + '/image/'+js['dir'];
                thumbnail = base64.b64encode(image_dir.encode('utf-8')).decode('utf-8')
            else:
                messages.error(request, "Something wrong when upload image, please try again!")
                return redirect('category:category', pk = pk)

        postObj = {
            'method_name': 'UPDATE_CATEGORY',
            'cate_id':id,
            'cat_name':bs.encode_Str(request.POST.get('Name')), 
            'cat_image': thumbnail,
            'cat_type':pk, 
            'status':request.POST.get('status')
        }

        data = {
            'data': json.dumps(postObj)
        }
        res = requests.post(SERVER_URL , data = data)
        return_obj = json.loads(res.content)
        if str(return_obj) == "success":
            return redirect('category:category', pk)
        else:
            return HttpResponse("Error")
    else:
        page = 'edit'
        context = {'page': page, 'choice':pk, 'category':category}
        return render(request, 'category/categorydetail.html', context)

@login_required(login_url='/login')
def disableCategory(request, pk, id):
    category = getCategory(id)
    
    postObj = {
        'method_name': 'UPDATE_STATUS_CATE',
        'cate_id': id,
        'status': 1 if category['cat_status'] == '0' else 0
    }

    data = {
        'data': json.dumps(postObj)
    }
    res = requests.post(SERVER_URL , data = data)
    return redirect("category:category", pk)