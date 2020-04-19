import csv
import json
import os
import subprocess
import time


def stage_3():
    with open('parsed_followers.json', 'r') as f:
        parsed_followers = json.load(f)

    connect = """curl 'https://www.instagram.com/{username}/?__a=1' -H 'authority: www.instagram.com' -H 'accept: */*' -H 'sec-fetch-dest: empty' -H 'x-ig-www-claim: hmac.AR31iXXO6vuqolpnv2POHkdIjuVwc_vYNQPpLacVboSDcxji' -H 'x-requested-with: XMLHttpRequest' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' -H 'x-ig-app-id: 936619743392459' -H 'sec-fetch-site: same-origin' -H 'sec-fetch-mode: cors' -H 'referer: https://www.instagram.com/sharowv/' -H 'accept-language: en-US,en;q=0.9,ru;q=0.8' -H 'cookie: ig_did=302AC792-901E-42E3-BE17-0F0A3FE1B5F3; mid=XprQHQAEAAFUSEP-dwyHOYrFLp_U; csrftoken=cCsrrfENAcr15gKoOeJ2KyMZgHqEAG1m; shbid=14468; shbts=1587204132.6504228; ds_user_id=2209768231; sessionid=2209768231%3AWhUwbRgRBK7e0f%3A16; rur=ATN; urlgen="{{\"95.79.134.153\": 42682}}:1jPn0T:quuQ0IehPg-ZLmmD3f3NHgXgh50"' --compressed > temp.json"""

    index = 0
    processed_followers = []
    for user in parsed_followers:
        subprocess.run(connect.format(username=user['username']), shell=True, capture_output=True)
        with open('temp.json', 'r') as f2:
            try:
                data = json.load(f2)
            except:
                print(f"trouble parsing json in {user['username']}")
                continue

        if 'graphql' not in data:
            time.sleep(5)
            print(f"missing graphql in response, response: {data}")
            continue

        user_info_shortener = data['graphql']['user']
        user['following'] = user_info_shortener['edge_follow']['count']
        user['posts'] = user_info_shortener['edge_owner_to_timeline_media']['count']
        user['is_business'] = user_info_shortener['is_business_account']
        user['bio'] = user_info_shortener['biography'].replace('\n', ' ')
        processed_followers.append(user)

        print(f'Cracking {index} out of {len(parsed_followers)}')
        time.sleep(2 if index % 10 != 0 else 5)
        index += 1

    print('Filtered, saving')
    os.remove('temp.json')

    with open('result.csv', 'w', newline='') as result:
        writer = csv.writer(result)
        writer.writerow(['Name', 'Handle', 'Following', 'Posts', 'Bio', 'Business'])
        for user in processed_followers:
            writer.writerow([
                user['full_name'],
                user['username'],
                user['following'],
                user['posts'],
                user['bio'],
                user['is_business']
            ])
    print('Finished, now open an CSV file in this directory')


if __name__ == "__main__":
    stage_3()

