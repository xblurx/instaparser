import csv
import json
import os
import subprocess
import time


with open('parsed_followers.json', 'r') as file:
    parsed_followers = json.load(file)

connect = """curl 'https://www.instagram.com/{username}/?__a=1' -H 'authority: www.instagram.com' -H 'accept: */*' -H 'sec-fetch-dest: empty' -H 'x-ig-www-claim: hmac.AR31iXXO6vuqolpnv2POHkdIjuVwc_vYNQPpLacVboSDczPA' -H 'x-requested-with: XMLHttpRequest' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36' -H 'x-ig-app-id: 936619743392459' -H 'sec-fetch-site: same-origin' -H 'sec-fetch-mode: cors' -H 'referer: https://www.instagram.com/kat.e_kharitonova/' -H 'accept-language: en-US,en;q=0.9' -H 'cookie: ig_did=00C4C467-381D-4CCA-BEF0-61DC4E9CB6CD; mid=Xl4shAAEAAG6aXwv0Zkp1QkYPakF; csrftoken=NXAaigBeg393lgJlRZxhY7WQxTMH8Zo4; shbid=14468; shbts=1583230111.2538457; ds_user_id=2209768231; sessionid=2209768231%3AyhLN4GBnZv6j5C%3A25; rur=ATN; urlgen="{{\"95.79.134.91\": 42682}}:1j94cc:TIlObBZqNXdHwctkZR6sB9T5TyQ"' --compressed > temp.json"""

index = 0
filtered_followers = []
for user in parsed_followers:
    subprocess.run(connect.format(username=user['username']), shell=True, capture_output=True)
    with open('temp.json', 'r') as file:
        try:
            data = json.load(file)
        except:
            print(f"trouble parsing json in {user['username']}")
            continue

    if 'graphql' not in data:
        time.sleep(5)
        print(f"missing graphql in response, response: {data}")
        continue

    user['following'] = data['graphql']['user']['edge_follow']['count']
    user['posts'] = data['graphql']['user']['edge_owner_to_timeline_media']['count']
    user['is_business'] = data['graphql']['user']['is_business_account']
    filtered_followers.append(user)
    print(f'Cracking {index} out of {len(parsed_followers)}')
    time.sleep(1 if index % 10 != 0 else 5)
    index += 1
print('Filtered, saving')
os.remove('temp.json')

with open('filtered_followers.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Username', 'Following', 'Posts', 'Business account'])
    for user in filtered_followers:
        writer.writerow([user['full_name'], user['username'],
                        user['following'], user['posts'], user['is_business']])
print('Done')
