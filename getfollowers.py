import json
import time
import subprocess
import urllib.parse
import requests

url = 'https://www.instagram.com/graphql/query/?'
user_handle = input('Enter your Instagram handle: ')
user_data = requests.get(f'https://www.instagram.com/{user_handle}/?__a=1').json()
user_id = user_data['graphql']['user']['id']

connect = """curl '{url}' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'X-CSRFToken: Y8jpccr0E7vh8bAQ9YLhDLQDNSFySf5f' -H 'X-IG-App-ID: 936619743392459' -H 'X-IG-WWW-Claim: hmac.AR31iXXO6vuqolpnv2POHkdIjuVwc_vYNQPpLacVboSDc7wq' -H 'X-Requested-With: XMLHttpRequest' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: https://www.instagram.com/'{{user_handle}}'/followers/' -H 'Cookie: csrftoken=Y8jpccr0E7vh8bAQ9YLhDLQDNSFySf5f; ig_did=4C1E137C-2156-4B91-8289-2DD1A7A70D19; mid=Xlvi1wAEAAGcXkHsDzmXrf_mXgzI; fbm_124024574287414=base_domain=.instagram.com; shbid=14468; shbts=1583080743.425335; ds_user_id=2209768231; sessionid=2209768231%3AG8ISv1kMXdv5jf%3A2; rur=ATN; urlgen="{{\"95.79.219.240\": 42682}}:1j8ksC:gVLgH-lixZ9YlZLLCpQn8dPBnyQ"' -H 'TE: Trailers' > json/followers_{i}.json"""

i = 1
after = None
in_progress = 0
while True:
    after_value = f',"after":"{after}"' if after else ''
    variables = f'{{"id":{user_id},"include_reel":true,"fetch_mutual":false,"first":50{after_value}}}'
    params = {
        'query_hash': 'c76146de99bb02f6415203be841dd25a',
        'variables': variables
    }

    webservice_url = url + urllib.parse.urlencode(params)
    query = subprocess.run(connect.format(url=webservice_url, i=i), shell=True, capture_output=True)

    if query.returncode != 0:
        print('Something bad happened')
    with open(f'json/followers_{i}.json', 'r') as f:
        data = json.load(f)

    if not data['data']['user']['edge_followed_by']['page_info']['has_next_page']:
        break

    after = data['data']['user']['edge_followed_by']['page_info']['end_cursor']
    total_count = data['data']['user']['edge_followed_by']['count']
    current_count = len(data['data']['user']['edge_followed_by']['edges'])
    in_progress += current_count
    print(f'Cracked {in_progress} out of {total_count}')
    time.sleep(2 if i % 10 != 0 else 10)
    i += 1
print('pwned')
