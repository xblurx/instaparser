import glob
import json

followers = {}
files = glob.glob('json/*.json')
for f in files:
    with open(f, 'r') as file:
        data = json.load(file)
        for user in data['data']['user']['edge_followed_by']['edges']:
            user_info = user['node']
            followers[user_info['username']] = {
                'id': user_info['id'],
                'username': user_info['username'],
                'followed_by_me': user_info['followed_by_viewer'],
                'full_name': user_info['full_name']
            }

followers_list = list(followers.values())
with open('parsed_followers.json', 'w') as f:
    json.dump(followers_list, f)

print('Done')
