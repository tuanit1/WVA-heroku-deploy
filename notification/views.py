import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import base64
from django.contrib import messages
from Constant import DEFAULT_ONESIGNAL_APP_ID, DEFAULT_REST_API_KEY, executePostRequest

# Create your views here.


@login_required(login_url='/login')
def sendNotification(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        side_icon = request.POST.get('side_icon')
        image_message = request.POST.get('image_message')
        app_id = DEFAULT_ONESIGNAL_APP_ID
        rest_api_key = DEFAULT_REST_API_KEY

        res_obj = executePostRequest({'method_name': 'GET_SETTING'})

        if res_obj['status'] == 'success':
            app_id = base64.b64decode(res_obj['setting_array']['onesignal_app_id']).decode('utf-8')
            rest_api_key = base64.b64decode(res_obj['setting_array']['onesignal_rest_api']).decode('utf-8')
        
        url = "https://onesignal.com/api/v1/notifications"

        payload = {
            "included_segments": ["Subscribed Users"],
            "contents": {
                "en": message
            },
            "headings": {
                "en": title
            },
            "name": "WatchVideoApp message",
            "app_id": app_id,
            "small_icon": "ic_stat_onesignal_small",
            "large_icon": side_icon,
            "big_picture": image_message
        }

        headers = {
            "Accept": "application/json",
            "Authorization": "Basic " + rest_api_key,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        res_obj = json.loads(response.text)

        print(response.text)

        if "errors" in res_obj:
            messages.error(request, "Send failed: " + str(res_obj["errors"]))
        else:
            messages.success(request, "Send push notifcation success!")

        return redirect('notification:send')

    return render(request, 'notification/sendNotification.html', {})
