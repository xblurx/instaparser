import json
import time
import requests
import subprocess
import urllib.parse


def stage_1():
    handle = input('Enter Instagram handle of a user you want to inspect: ')
    initial_url = 'https://www.instagram.com/graphql/query/?'
    user_data = requests.get(f'https://www.instagram.com/{handle}/?__a=1').json()
    user_id = user_data['graphql']['user']['id']

    connect = """curl '{url}' -H 'authority: www.instagram.com' -H 'x-ig-www-claim: hmac.AR31iXXO6vuqolpnv2POHkdIjuVwc_vYNQPpLacVboSDcxji' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' -H 'accept: */*' -H 'sec-fetch-dest: empty' -H 'x-requested-with: XMLHttpRequest' -H 'x-csrftoken: cCsrrfENAcr15gKoOeJ2KyMZgHqEAG1m' -H 'x-ig-app-id: 936619743392459' -H 'sec-fetch-site: same-origin' -H 'sec-fetch-mode: cors' -H 'referer: https://www.instagram.com/{handle}/followers/' -H 'accept-language: en-US,en;q=0.9,ru;q=0.8' -H 'cookie: ig_did=302AC792-901E-42E3-BE17-0F0A3FE1B5F3; mid=XprQHQAEAAFUSEP-dwyHOYrFLp_U; csrftoken=cCsrrfENAcr15gKoOeJ2KyMZgHqEAG1m; shbid=14468; shbts=1587204132.6504228; ds_user_id=2209768231; sessionid=2209768231%3AWhUwbRgRBK7e0f%3A16; rur=ATN; urlgen="{{\"95.79.134.153\": 42682}}:1jPkqt:IcCGoo92Il201m2bqbq4TniwQZ8"' --compressed > json/followers_{index}.json"""

    '''
    Forming a cycle of requests to get all followers. 
    NB: Instagram needs "after" parameter from second iteration on.
    '''
    index = 1
    after = None
    in_progress = 0
    while True:
        after_value = f',"after":"{after}"' if after else ''
        variables = f'{{"id":{user_id},"include_reel":true,"fetch_mutual":false,"first":50{after_value}}}'
        params = {
            'query_hash': 'c76146de99bb02f6415203be841dd25a',
            'variables': variables
        }
        request_url = initial_url + urllib.parse.urlencode(params)
        result = subprocess.run(connect.format(url=request_url, handle=handle, index=index),
                                shell=True, capture_output=True)

        if result.returncode != 0:
            exit('An error occurred')
        with open(f'json/followers_{index}.json') as f:
            data = json.load(f)
        if not data['data']['user']['edge_followed_by']['page_info']['has_next_page']:
            break

        after = data['data']['user']['edge_followed_by']['page_info']['end_cursor']
        all_followers = data['data']['user']['edge_followed_by']['count']
        current_portion = len(data['data']['user']['edge_followed_by']['edges'])
        in_progress += current_portion
        print(f'Cracked {in_progress} followers out of {all_followers}')
        time.sleep(5 if index % 10 != 0 else 10)
        index += 1

    print('Users loaded')


if __name__ == "__main__":
    stage_1()
