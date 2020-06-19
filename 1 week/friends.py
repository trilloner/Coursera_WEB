import requests
import json
from datetime import datetime
#service token
ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'
#parse str
def check_str(str):
    if str is None:
        return False
    elif len(str) <7:
        return False
    else:
        return True


def get_friends(id):
    url = 'https://api.vk.com/method/friends.get?v=5.71&access_token={token}&user_id={user}&fields=bdate'.format(token = ACCESS_TOKEN, user = id)

    uk = requests.get(url)

    content = uk.content.decode('utf8')

    friend_list = dict([])

    friends = json.loads(content)
    for value in friends['response']['items']:
        temp = value.get("bdate")
        if check_str(temp) is True:
            year = int(datetime.now().year) - int(temp[-4:])
            if year in friend_list:
                friend_list[year] += 1
            else:
                friend_list[year] = 1
    result_list = sorted(friend_list.items(),key=lambda x:(-x[1], x[0]))
    return list(result_list)









def calc_age(uid):
    url = 'https://api.vk.com/method/users.get?v=5.71&access_token={token}&user_ids={user}'.format(token = ACCESS_TOKEN,user = uid)

    uk = requests.get(url)

    content = uk.content.decode('utf8')

    json_file = json.loads(content)

    result = get_friends(json_file['response'][0]['id'])
    return result





if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
