from warrant.aws_srp import AWSSRP
import configparser
import urllib.request
import json
import base64



def post_article_to_alis(id_token):
    # JST = timezone(timedelta(hours=+9), 'JST')
    # nowx = datetime.now(JST)
    #
    # # make dammy
    # url = 'https://alis.to/api/me/articles/drafts'
    # title = 'ダミー'
    # body = '本文'
    # method = 'POST'
    # headers = {'Authorization': id_token}
    # data ={
    #   'title': title,
    #   'body': body,
    # }
    #
    # request = urllib.request.Request(url,  json.dumps(data).encode(), method=method, headers=headers)
    # with urllib.request.urlopen(request) as response:
    #     response_body = json.load(response)
    # article_id = response_body['article_id']

    article_id = '3qQXNRq08RP4'

    # upload eyecatch
    url = 'https://alis.to/api/me/articles/' + article_id + '/images'
    image_path = './wordcloud.png'
    image_data = open(image_path, "rb").read()

    method = 'POST'
    headers = {
        'Authorization': id_token,
        'accept': 'application/json application/octet-stream',
        'content-type': 'png',
    }
    data ={
      'article_image': base64.b64encode(image_data).decode('utf-8'),
    }
    request = urllib.request.Request(url,  json.dumps(data).encode(), method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = json.load(response)
    image_url = response_body['image_url']

    # upload contents
    url = 'https://alis.to/api/me/articles/' + artcle_id + '/drafts'
    title = '日刊 ALISコメントランキング(' + str(nowx.month) + '/' + str(nowx.day) + ')'
    eye_catch_url = image_url
    overview = '毎日定時にALISのコメント多かった記事の抜粋をお届けします'
    with open('./alis_media.html') as f:
        body = f.read()

    method = 'POST'
    headers = {'Authorization': id_token}
    data ={
      'title': title,
      'body': body,
      'eye_catch_url': eye_catch_url,
      'overview': overview
    }
    request = urllib.request.Request(url,  json.dumps(data).encode(), method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = json.load(response)



    # publish
    url = 'https://alis.to/api/me/articles/' + artcle_id  + '/drafts/publish'
    method = 'PUT'
    headers = {'Authorization': id_token}
    data = {
        'topic': 'others',
        'tags': ['ALISコメントランキング']
    }
    request = urllib.request.Request(url, json.dumps(data).encode(), method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        print(request)


def get_alis_access_token():
    config = configparser.ConfigParser()
    config.read('./alis_connect.ini')
    POOL_ID = 'ap-northeast-1_HNT0fUj4J'
    POOL_REGION = 'ap-northeast-1'
    CLIENT_ID = '2gri5iuukve302i4ghclh6p5rg'
    USERNAME = config.get('DB', 'USERNAME')
    PASSWORD = config.get('DB', 'PASSWORD')
    aws = AWSSRP(username=USERNAME, password=PASSWORD, pool_id=POOL_ID, client_id=CLIENT_ID, pool_region=POOL_REGION)
    id_token = aws.authenticate_user()['AuthenticationResult']['IdToken']
    return id_token


if __name__ == '__main__':
    id_token = get_alis_access_token()
    post_article_to_alis(id_token)
