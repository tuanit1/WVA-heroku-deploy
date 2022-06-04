import base64
import json
import cv2
import requests as rq
from datetime import datetime
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import re
from Constant import UPLOAD_VIDEO, IMAGE_DIR, executePostRequest

url_regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


@login_required(login_url='/login')
def updateVideo(request, id):

    try:

        # get video post request
        res_video = executePostRequest({
            'method_name': 'GET_VIDEO_BYID',
            'vid_id': id
        })

        res_cat = executePostRequest({
            'method_name': 'LOAD_CATEGORT',
            'type': 1,
            'search_text': ''
        })

        if(res_video['status'] != 'success' or res_cat['status'] != 'success'):
            return HttpResponse("Server Error!")

        video = getDecodeVideo(res_video['video'])
        categories = res_cat['category']

        if request.method == 'POST':

            data = cv2.VideoCapture(request.POST.get('url'))
            frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = int(data.get(cv2.CAP_PROP_FPS))
            seconds = int(frames / fps)

            params = {
                'method_name': 'UPDATE_VIDEO',
                'vid_id': request.POST.get('id'),
                'cat_id':  request.POST.get('cat_id'),
                'vid_title': base64.b64encode(request.POST.get('title').encode('utf-8')).decode('utf-8'),
                'vid_url': base64.b64encode(request.POST.get('url').encode('utf-8')).decode('utf-8'),
                'vid_thumbnail':  base64.b64encode(request.POST.get('thumbnail').encode('utf-8')).decode('utf-8')
                if request.POST.get('thumbnail') != "" else "",
                'vid_description': base64.b64encode(request.POST.get('description').encode('utf-8')).decode('utf-8'),
                'vid_view': round(int(request.POST.get('views'))),
                'vid_duration': seconds,
                'vid_time': datetime.strptime(request.POST.get('time'), '%Y-%m-%d')
                .strftime("%Y-%m-%d %H:%M:%S"),
                'vid_avg_rate':  request.POST.get('rate'),
                'vid_status': request.POST.get('status'),
                'vid_type': 1,
                'vid_is_premium': 0,
            }

            # check user update image
            if 'file_img' in request.FILES:
                print("update image")

                url = UPLOAD_VIDEO
                files = {'file': request.FILES['file_img']}
                data = {'crr': request.POST.get('thumbnail')}
                res = rq.post(url, files=files, params=data)

                js = json.loads(res.content)
                if(js['status'] == 1):
                    image_dir = IMAGE_DIR + js['dir']
                    params['vid_thumbnail'] = base64.b64encode(
                        image_dir.encode('utf-8')).decode('utf-8')
                else:
                    messages.error(
                        request, "Something wrong when upload image, please try again!")
                    return redirect('videoapp:update', id=id)

            status = executePostRequest(params)

            if(status == 'success'):
                messages.success(request, "Update video successfully!")
            else:
                messages.error(
                    request, "Update video failed!")

            return redirect('managervideo:managervideo', 1, 0)

        # load to screen
        date_time = datetime.strptime(
            video['vid_time'], '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")

        for index in range(len(categories)):
            categories[index] = getDecodeCategory(categories[index])

        context = {
            'mode': 'update',
            'video': video,
            'date': date_time,
            'categories': categories
        }

        return render(request, 'videoapp/updateVideo.html', context)

    except:
        return HttpResponse("Server Error!")

@login_required(login_url='/login')
def createVideo(request):

    try:

        #post new video
        if request.method == 'POST':
    
            data = cv2.VideoCapture(request.POST.get('url'))
            frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = int(data.get(cv2.CAP_PROP_FPS))
            seconds = int(frames / fps)

            param = {
                'method_name': 'ADD_VIDEO',
                'cat_id':  request.POST.get('cat_id'),
                'vid_title': base64.b64encode(request.POST.get('title').encode('utf-8')).decode('utf-8'),
                'vid_url': base64.b64encode(request.POST.get('url').encode('utf-8')).decode('utf-8'),
                'vid_thumbnail':  base64.b64encode(request.POST.get('thumbnail').encode('utf-8')).decode('utf-8')
                    if request.POST.get('thumbnail') != "" else "",
                'vid_description': base64.b64encode(request.POST.get('description').encode('utf-8')).decode('utf-8'),
                'vid_view': round(int(request.POST.get('views'))),
                'vid_duration': seconds,
                'vid_time': datetime.strptime(request.POST.get('time'), '%Y-%m-%d')
                    .strftime("%Y-%m-%d %H:%M:%S"),
                'vid_avg_rate':  0,
                'vid_status': request.POST.get('status'),
                'vid_type': 1,
                'vid_is_premium': 0,
            }

            # check user update image
            if 'file_img' in request.FILES:
                print("update image")

                url = UPLOAD_VIDEO
                files = {'file': request.FILES['file_img']}
                data = {'crr': request.POST.get('thumbnail')}
                res = rq.post(url, files=files, params=data)

                js = json.loads(res.content)
                if(js['status'] == 1):
                    image_dir = IMAGE_DIR +js['dir']
                    param['vid_thumbnail'] = base64.b64encode(
                        image_dir.encode('utf-8')).decode('utf-8')
                else:
                    messages.error(
                        request, "Something wrong when upload image, please try again!")
                    return redirect('videoapp:create')
            else:
                messages.error(request, "Thumbnail is required!")
                return redirect('videoapp:create')


            status = executePostRequest(param)

            if(status == 'success'):
                messages.success(request, "Create video successfully!")
            else:
                messages.error(request, "Create video failed!")
                
            return redirect('managervideo:managervideo', 1, 0)


        #load to screen
        res_cat = executePostRequest({
                'method_name': 'LOAD_CATEGORT',
                'type': 1,
                'search_text': ''
        })

        if(res_cat['status'] != 'success'):
            return HttpResponse("Server Error!")

        categories = res_cat['category']

        for index in range(len(categories)):
            categories[index] = getDecodeCategory(categories[index])

        now = datetime.now()
        date_time = now.strftime('%Y-%m-%d')

        context = {
            'mode': 'create',
            'date': date_time,
            'categories': categories
        }

        return render(request, 'videoapp/updateVideo.html', context)
    except:
        return HttpResponse("Server Error!")

    

@login_required(login_url='/login')
def videoPlayer(request):

    url = request.POST.get('url') if request.POST.get('url') != None else ''

    context = {'url': url}
    return render(request, 'videoapp/videoPlayer.html', context)


def getDecodeVideo(video):
    base64.b64decode(video['vid_title']).decode('utf-8')
    return {

        'vid_id': int(video['vid_id']),
        'cat_id': int(video['cat_id']),
        'vid_title': base64.b64decode(video['vid_title']).decode('utf-8'),
        'vid_url': base64.b64decode(video['vid_url']).decode('utf-8'),
        'vid_thumbnail': base64.b64decode(video['vid_thumbnail']).decode('utf-8'),
        'vid_description': base64.b64decode(video['vid_description']).decode('utf-8'),
        'vid_view': int(video['vid_view']),
        'vid_duration': int(video['vid_duration']),
        'vid_avg_rate': float(video['vid_avg_rate']),
        'vid_status': int(video['vid_status']),
        'vid_type': int(video['vid_type']),
        'vid_time': video['vid_time'],
        'vid_is_premium': int(video['vid_is_premium'])
    }


def getDecodeCategory(cat):
    return {
        'cat_id': int(cat['cat_id']),
        'cat_name': base64.b64decode(cat['cat_name']).decode('utf-8'),
        'cat_image': base64.b64decode(cat['cat_image']).decode('utf-8'),
        'cat_type': int(cat['cat_type'])
    }
