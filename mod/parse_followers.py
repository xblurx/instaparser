import glob
import json


def stage_2():
    files = glob.glob('json/*.json')
    followers = {}

    for f in files:
        with open(f, 'r') as file:
            data = json.load(file)
            for user in data['data']['user']['edge_followed_by']['edges']:
                user_info = user['node']
                followers[user_info['username']] = {
                    'id': user_info['id'],
                    'username': user_info['username'],
                    'full_name': user_info['full_name'],
                    'followed_by_me': user_info['followed_by_viewer']
                }

    followers = list(followers.values())
    with open('parsed_followers.json', 'w') as f:
        json.dump(followers, f)

    print('All set')

if __name__ == "__main__":
    stage_2()
