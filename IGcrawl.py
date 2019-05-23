import requests
import json
import time
import urllib
import uuid
import os
import random

import sys
if len(sys.argv)==1:
    exit()



BASE_URL = 'https://www.instagram.com/'
LOGIN_URL = BASE_URL + 'accounts/login/ajax/'


USERNAME='User Name goes Here'
PASSWORD = 'Your password goes here'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'

DEVICE_SETTINTS = {'manufacturer': 'Xiaomi',
    'model': 'HM 1SW',
        'android_version': 18,
            'android_release': '4.3'}
USER_AGENT = 'Instagram 10.26.0 Android ({android_version}/{android_release}; 320dpi; 720x1280; {manufacturer}; {model}; armani; qcom; en_US)'.format(**DEVICE_SETTINTS)

USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'



ig_userID = 0
uuid = generateUUID(True)


session = requests.Session()
session.headers = {'user-agent' : USER_AGENT}
session.headers.update({'Referer' : BASE_URL,'X-IG-Connection-Type': 'WIFI'})

req = session.get(BASE_URL)
session.headers.update({'x-csrftoken':req.cookies['csrftoken']})
login_data = {'username' : USERNAME, 'password' : PASSWORD}

req_login = session.post(LOGIN_URL,data=login_data,allow_redirects = True)
session.headers.update({'x-csrftoken':req_login.cookies['csrftoken']})

print(req_login.text)

ig_userID =json.loads(req_login.text)['userId']
print("UserID = " + ig_userID)

'''--------------------------------------------------------- '''




def get_Followers():
    GET_FOLLINGS_URL = BASE_URL + 'graphql/query'
    #session.headers.update({'Referer' : 'https://www.instagram.com/cornerhipster/followers/'})
    #session.headers.update({'X-Instagram-GIS' : 'ad4cf21315718a6b541865f9516c962c'})
    #session.headers.update({'' : 'ad4cf21315718a6b541865f9516c962c'})



    #req_data = {'query_hash' : '56066f031e6239f35a904ac20c9f37d9','variables': json.dumps(variables)}
    #req_get_follings = session.get(GET_FOLLINGS_URL,data = req_data,allow_redirects = True)
    gotoNext = True
    end_cursor = ''
    count =0
    index=0

    while(gotoNext):
        time.sleep(1)
        count = count+1
        if(end_cursor == ''):
            print('first time')
            url = 'https://www.instagram.com/graphql/query/?query_hash=56066f031e6239f35a904ac20c9f37d9&variables=%7B%22id%22%3A%228674797789%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A100%7D'
        #24
        else:
            print('here')
            url ='https://www.instagram.com/graphql/query/?query_hash=56066f031e6239f35a904ac20c9f37d9&variables=%7B%22id%22%3A%228674797789%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A100%2C%22after%22%3A%22' + end_cursor +  '%22%7D'
        req_get_followings = session.get(url)
        session.headers.update({'x-csrftoken':req_get_followings.cookies['csrftoken']})
        data_follow =json.loads(req_get_followings.text)
        print('Followers count:' + str(data_follow['data']['user']['edge_followed_by']['count']))
        print()

        for f in data_follow['data']['user']['edge_followed_by']['edges']:
            print (str(index) + ' ' +f['node']['username'])
            index = index +1
        
        gotoNext = data_follow['data']['user']['edge_followed_by']['page_info']['has_next_page']
        if (gotoNext):
                end_cursor = data_follow['data']['user']['edge_followed_by']['page_info']['end_cursor']
        if(count ==16):
            break

def get_hashtag_post(max_crawl,tag,multipage=False,end_cursor = ''):
   
    gotoNext = True
    
    count =0
    index=0
    hashtag_post_log = open('hashtag_post.txt', 'w')
    while(gotoNext):
        time.sleep(1)
        count = count+1
        if(end_cursor == ''):
            print('first time')
            url = 'https://www.instagram.com/explore/tags/'  + urllib.parse.quote(tag) + '/?__a=1'
            req_get_posts = session.get(url)
        else:
            print('here')
            url ='https://www.instagram.com/graphql/query/?query_hash=f92f56d47dc7a55b606908374b43a314&variables=%7B%22tag_name%22%3A%22' + urllib.parse.quote(tag) + '%22%2C%22show_ranked%22%3Afalse%2C%22first%22%3A100%2C%22after%22%3A%22' + end_cursor + '%22%7D'
            #url = 'https://www.instagram.com/graphql/query/'
            #variables={'tag_name':tag.encode('utf-8'),'show_ranked':False ,'first':100,'after' : end_cursor}
            #req_data = {'query_hash' : 'f92f56d47dc7a55b606908374b43a314','variables': json.dumps(variables)}
            #req_data = {'query_hash' : 'f92f56d47dc7a55b606908374b43a314','variables': {'tag_name':tag.encode('utf-8'),'show_ranked':False ,'first':100,'after' : end_cursor}}
            req_get_posts = session.get(url)
        
        #req_get_posts = session.get(url)
        session.headers.update({'x-csrftoken':req_get_posts.cookies['csrftoken']})
        data_post =json.loads(req_get_posts.text)
        
        
        if(end_cursor != '' and data_post['status'] == 'fail'):
            print('Error occurred from Ig:' + data_post['message'])
            print(data_post)
            break
        #print('Followers count:' + str(data_follow['data']['user']['edge_followed_by']['count']))
        print()
        
        
        posts = ''
        if(end_cursor == ''):
            posts =data_post['graphql']
        else:
            posts = data_post['data']
        
        
        for f in posts['hashtag']['edge_hashtag_to_media']['edges']:
            print (str(index) + '\t' +f['node']['id'])
            print ( 'shortcode\t' +f['node']['shortcode'])
            print ('likes\t' + str(f['node']['edge_liked_by']['count']))
            print ('owner\t'  +f['node']['owner']['id'])
            print()
            hashtag_post_log.write(f['node']['id'] + ' ' + f['node']['shortcode'] + ' ' + str(f['node']['edge_liked_by']['count']) +  ' ' + f['node']['owner']['id'] + '\n')
            index = index +1
            if(index>=max_crawl):
                break

                    
        gotoNext = posts['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
        if (gotoNext):
            end_cursor = posts['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        if(count ==10):
            break
        if(index>=max_crawl):
            break
    hashtag_post_log.close()


def post_photo(image_path,caption):
    print('start_post_photo')
    """ example: post_photo('img.jpg','''This is a Test\n這是中文\n#好棒棒''')"""
    upload_photo_url = BASE_URL + 'create/upload/photo/'
    upload_id = str(int(time.time() * 1000))
    
    #image_path = 'img.jpg'
    image_filename = os.path.basename(image_path)

    multipart_form_data = {
        'upload_id': ('', upload_id),
        'photo': (image_filename, open(image_path, 'rb')),
        'media_type': ('', '1')
    }

    response = session.post(upload_photo_url, files=multipart_form_data)
    session.headers.update({'x-csrftoken':response.cookies['csrftoken']})

    if(json.loads(response.text)['status'] == 'fail'):
        print('[upload] Error occurred from Ig:' + json.loads(response.text)['message'])
        print (json.loads(response.text))
        return False
    else:
        print('upload photo succeed')

    print('wait for 3 seconds')
    time.sleep(3)
#caption.encode('utf-8')
    confugure_url = BASE_URL + 'create/configure/'
    str1 = '{"in":[{"user_id":"8674797789","position":[0.8648033040364583,0.8939236653645833]}]}'
#str1 = '%7B%22in%22%3A%5B%7B%22user_id%22%3A%229790985%22%2C%22position%22%3A%5B0.9384838053385417%2C0.9146411946614583%5D%7D%5D%7D'
    data1 ={'upload_id': json.loads(response.text)['upload_id'],
        'caption': caption.encode('utf-8'),
        'usertags':'',
        'custom_accessibility_caption':'',
        'retry_timeout':''}
    raw = 'upload_id=' + json.loads(response.text)['upload_id'] + '&caption=ttest&usertags=%7B%22in%22%3A%5B%7B%22user_id%22%3A%228674797789%22%2C%22position%22%3A%5B0.8648033040364583%2C0.8939236653645833%5D%7D%5D%7D&custom_accessibility_caption=&retry_timeout='
    #data1 = urllib.parse.urlencode(data1)
    #data1 = data1.encode('utf-8')
#session.headers.update({'Content-Type':'application/x-www-form-urlencoded'})


    response1 = session.post(confugure_url,data = data1)






    if(json.loads(response1.text)['status'] == 'fail'):
        print('[congigure] Error occurred from Ig:' + json.loads(response1.text)['message'])
        print (json.loads(response1.text))
        return False
    else:
        print('configure success')
        return True



#get_Followers()
#get_hashtag_post()
'''
print data_follow['data']['user']['edge_followed_by']['edges']['node']['id']
data_follow['data']['user']['edge_followed_by']['edges']['node']['username']
data_follow['data']['user']['edge_followed_by']['edges']['node']['full_name']
'''

def auto_like_hashtag_post(tag,amount):
    #get_hashtag_post(amount,tag)

    prepare_posts = open("hashtag_post.txt", "r")
    posts = prepare_posts.read().split('\n')
    prepare_posts.close()

    liked_posts_raw =open("like_log.txt", "r")
    liked_posts = liked_posts_raw.read().split('\n')
    liked_posts_raw.close()
    count = 0
    for p in posts:
        if(p.split(' ')[0] in liked_posts):
            print('liked before')
        else:
            like_post(p.split(' ')[0])
            count = count +1
            print(count)
            time.sleep(random.uniform(1.4,2.5))
            if(count%90 == 0 and count>80):
                print('Resting -----')
                time.sleep(random.uniform(300,330))
            

    print('send ' + str(count) + ' likes')

if sys.argv[1]=="gettag" :
    get_hashtag_post(500,sys.argv[2])
elif sys.argv[1]=="like":
    auto_like_hashtag_post("",500)


