import json
import requests as rq
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import main.base64_change as bs
from datetime import date
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

def decode_Item_Video(video):
    video['vid_id'] = int(video['vid_id'])
    video['cat_id'] = int(video['cat_id'])
    video['vid_title'] = bs.decode_Str(video['vid_title'])
    video['vid_url'] = bs.decode_Str(video['vid_url'])
    video['vid_thumbnail'] = bs.decode_Str(video['vid_thumbnail'])
    video['vid_description'] = bs.decode_Str(video['vid_description'])
    video['vid_view'] = int(video['vid_view'])
    video['vid_duration'] = int(video['vid_duration'])
    video['vid_avg_rate'] = float(video['vid_avg_rate'])
    video['vid_status'] = int(video['vid_status'])
    video['vid_type'] = int(video['vid_type'])
    video['vid_is_premium'] = int(video['vid_is_premium'])
    return video

def decode_Video(videos):
    for video in videos:
        video = decode_Item_Video(video)
    return videos

def getVid(id):
    postObj = {
        'method_name': 'GET_VIDEO_BYID',
        'vid_id': id
    }

    data = {
        'data': json.dumps(postObj)
    }

    res = requests.post(SERVER_URL , data = data)
    return_obj = json.loads(res.content)

    return return_obj['video'] if return_obj['status'] == "success" else []

@login_required(login_url='/login')
def managervideo(request , pk, cat):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    postObj = {
        'method_name': 'LOAD_TV_OR_RADIO',
        'type':pk,
        'cate_id':cat,
        'search_txt': q
    }

    data = {
        'data': json.dumps(postObj)
    }

    res = requests.post(SERVER_URL , data = data)
    return_obj = json.loads(res.content)

    videos = return_obj['all'] if return_obj['status'] == "success" else []
    categories = return_obj['category'] if return_obj['status'] == "success" else []
    videos = decode_Video(videos)
    categories = decode_Cate(categories)
    #Paginator
    p = Paginator(videos, 8)
    page = request.GET.get('page') 
    list_res = p.get_page(page)
    nums = "a" * list_res.paginator.num_pages
    context = {'choice':pk, 'cat':cat, 'categories':categories, 'videos':list_res, 'test':q, 'nums':nums}
    return render(request, 'managervideo/managervideo.html', context)

@login_required(login_url='/login')
def addTv(request, pk, cat):
    postObj = {
        'method_name': 'LOAD_CATEGORT',
        'type':pk,
        'search_txt': ''
    }

    data = {
        'data': json.dumps(postObj)
    }

    res = requests.post(SERVER_URL , data = data)
    return_obj = json.loads(res.content)

    categories = return_obj['category'] if return_obj['status'] == "success" else []
    categories = decode_Cate(categories)
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

        postObj =  {
                    'method_name': 'ADD_VIDEO',
                    'cat_id':request.POST.get('category_vid'),
                    'vid_title': bs.encode_Str(request.POST.get('title')),
                    'vid_url': bs.encode_Str(request.POST.get('url')), 
                    'vid_thumbnail': thumbnail,
                    'vid_description': bs.encode_Str(request.POST.get('description')), 
                    'vid_view': "0", 
                    'vid_duration': "0", 
                    'vid_time': request.POST.get('time'), 
                    'vid_avg_rate': "0", 
                    'vid_status': request.POST.get('vid_status'), 
                    'vid_type': pk,
                    'vid_is_premium': "0"}
        data = {
            'data': json.dumps(postObj)
        }
        res = requests.post(SERVER_URL , data = data)
        return_obj = json.loads(res.content)
        if str(return_obj) == "success":
            return redirect("managervideo:managervideo", pk, request.POST.get('category_vid'))
        else:
            return HttpResponse("Error")
    else:   
        date_time = date.today().strftime("%Y-%m-%d")
        page = 'add'
        context = {'page': page, 'choice':pk, 'cat':cat, 'date_time':date_time, 'categories':categories, 'mode': 'create'}
        return render(request, 'managervideo/tvradiodetail.html', context)

@login_required(login_url='/login')
def editTv(request, pk, cat, id):
    video = getVid(id)
    video = decode_Item_Video(video)
    date_time = (datetime.strptime(video['vid_time'], "%Y-%m-%d %H:%M:%S")).strftime('%Y-%m-%d')

    postObj = {
        'method_name': 'LOAD_CATEGORT',
        'type':pk,
        'search_txt': ''
    }

    data = {
        'data': json.dumps(postObj)
    }

    res = requests.post(SERVER_URL , data = data)
    return_obj = json.loads(res.content)

    categories = return_obj['category'] if return_obj['status'] == "success" else []
    categories = decode_Cate(categories)

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
                return redirect('managervideo:editvideo', cat=cat, id=id)

        postObj = {
            'method_name': 'UPDATE_VIDEO','vid_id': video['vid_id'],
            'cat_id': request.POST.get('category_vid'),
            'vid_title': bs.encode_Str(request.POST.get('title')), 
            'vid_url': bs.encode_Str(request.POST.get('url')), 
            'vid_thumbnail': thumbnail,
            'vid_description': bs.encode_Str(request.POST.get('description')), 
            'vid_view': request.POST.get('views'),
            'vid_duration': video['vid_duration'],
            'vid_time': request.POST.get('time'),
            'vid_avg_rate': request.POST.get('rate'),
            'vid_status': request.POST.get('vid_status'), 
            'vid_type': pk,
            'vid_is_premium': "0"}

        data = {
            'data': json.dumps(postObj)
        }
        res = requests.post(SERVER_URL , data = data)
        return_obj = json.loads(res.content)
        if str(return_obj) == "success":
            return redirect("managervideo:managervideo", pk, request.POST.get('category_vid'))
        else:
            return HttpResponse("Error")
    else:
        page = 'edit'
        context = {'page': page, 'choice':pk, 'cat':cat, 'video':video, 'categories':categories, 'date_time':date_time, 'mode': 'update'}
        return render(request, 'managervideo/tvradiodetail.html', context)

@login_required(login_url='/login')
def disableVideo(request, pk, cat, id):
    video = getVid(id)
    postObj = {
        'method_name': 'UPDATE_STATUS_RADIOTV',
        'vid_id': id,
        'status': 1 if video['vid_status'] == '0' else 0
    }

    data = {
        'data': json.dumps(postObj)
    }
    res = requests.post(SERVER_URL , data = data)
    return redirect("managervideo:managervideo", pk, cat)