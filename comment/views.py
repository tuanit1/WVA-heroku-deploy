from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import main.base64_change as bs
from django.core.paginator import Paginator
from Constant import SERVER_URL
import json
import requests

def decode_Item_Cmt(comment):
    comment['uid'] = bs.decode_Str(comment['uid'])
    comment['cmt_text'] = bs.decode_Str(comment['cmt_text'])
    
    return comment

def decode_Cmt(comments):
    for comment in comments:
        comment = decode_Item_Cmt(comment)
    return comments

def decode_Item_Vid(video):
    video['vid_title'] = bs.decode_Str(video['vid_title'])
    return video

def decode_Vid(videos):
    for video in videos:
        video = decode_Item_Vid(video)
    return videos

@login_required(login_url='/login')
def comment_home(request, video_type):
    video_search = request.GET.get('tv_search_video') if request.GET.get('tv_search_video') != None else ''
    postObj = {
        'method_name': 'LOAD_ALL_VID_CMT',
        'vid_search': bs.encode_Str(video_search),
        'vid_type': video_type,
    }
    data = {
        'data': json.dumps(postObj),
    }
    res = requests.post(SERVER_URL, data=data)
    return_object = json.loads(res.content)

    list_vid = decode_Vid(return_object['list'])

    #Paginator
    p = Paginator(list_vid, 8)
    page = request.GET.get('page') 
    list_vids = p.get_page(page)
    nums = "a" * list_vids.paginator.num_pages

    context = {'list_vids': list_vids, 'video_type':video_type, 'nums':nums}
    return render(request, 'comment/home_comment.html', context)

@login_required(login_url='/login')
def comment_main(request, video_id):
    cmt_search = request.GET.get('tv_search_cmt') if request.GET.get('tv_search_cmt') != None else ''
    postObj = {
        'method_name': 'LOAD_CMT_BY_VID_SEARCH',
        'vid_id': video_id,
        'cmt_search': bs.encode_Str(cmt_search),
    }
    data = {
        'data': json.dumps(postObj),
    }
    res = requests.post(SERVER_URL, data=data)
    return_object = json.loads(res.content)

    cmts = decode_Cmt(return_object['list'])
    Paginator
    p = Paginator(cmts, 8)
    page = request.GET.get('page') 
    list_cmts = p.get_page(page)
    nums = "a" * list_cmts.paginator.num_pages

    if (list_cmts is not None):
        context = {
            
            'video_cat' : bs.decode_Str(list_cmts[0]['cat_name']), 
            'video_title' : bs.decode_Str(list_cmts[0]['vid_title']), 
            'video_id': list_cmts[0]['vid_id'],
            'vid_view': list_cmts[0]['vid_view'],
            'total_comments' : list_cmts[0]['total_comments'], 
            'nums': nums,
            'list_cmts': list_cmts,
        }
        return render(request, 'comment/list_comment.html', context)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    

        

def delete_comment(request, cmt_id):
    
    if request.method=="POST":
        postObj = {
        'method_name': 'DEL_CMT',
        'cmt_id': cmt_id,
        }
        data = {
            'data': json.dumps(postObj),
        }
        res = requests.post(SERVER_URL, data=data)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))