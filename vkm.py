import requests
import datetime

GROUP_TOKEN = '594f2b9f260fcc4169577facfb74fc5f196846c1b6b68cff17ebd24c1a8d446370f139b72f2bffb1f9137'
VK_VERSION = '5.131'


class VKinder:
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    @staticmethod
    def get_candidate(users_params):
        params = {
            'access_token': GROUP_TOKEN,
            'v': VK_VERSION
        }
        url = 'https://api.vk.com/method/users.search'
        users_search = {
            'age_from': users_params['age_from'],
            'age_to': users_params['age_to'],
            'sex': users_params['sex'],
            'hometown': users_params['city'],
            'relation': 6,                        # 6 в активном поиске
            'has_photo': 1,                       # есть аватарка
            'count': 5,                           # количество пользователей
        }
        res = requests.get(url, params={**params, **users_search})
        persons = res.json()
        return persons['response']['items']

    def get_users_data(self, params,  currents):
        candidates = {}
        items = self.get_candidate(params)
        for data_person in items:
            if data_person['is_closed'] == False and data_person['id'] not in currents:
                app_dict = []
                id_person = int(data_person['id'])
                fotos_data = self.get_users_foto(id_person)
                fotos_data = sorted(fotos_data, key=lambda x: (x['likes']['count'], x['comments']['count']),
                                    reverse=True)
                fotos_data = fotos_data[0:3]
                for foto_person in fotos_data:
                    url_foto = foto_person['sizes'][0]['url']
                    app_dict.append({'url_foto': url_foto})
                candidates[id_person] = app_dict
        return candidates

    @staticmethod
    def get_users_foto(id_person):
        params = {
            'access_token': GROUP_TOKEN,
            'v': VK_VERSION
        }
        url_foto = 'https://api.vk.com/method/photos.get'
        foto_search = {
            'extended': '1',
            'owner_id': id_person,
            'count': 5,
            'album_id': 'profile',
            'rev': '0',
            'photo_sizes': 0
        }
        res_foto = requests.get(url_foto, params={**params, **foto_search})
        fotos = res_foto.json()

        return fotos['response']['items']

    def get_info_person(self, user_id):
        url_info_person = 'https://api.vk.com/method/users.get'
        info_search = {
            'user_ids': user_id,
            'fields': 'sex, city, bdate',
        }
        res_info = requests.get(url_info_person, params={**self.params, **info_search})
        info = res_info.json()
        sex = 1 if info['response'][0]['sex'] == 2 else 2
        year = info['response'][0]['bdate'][-4:]
        today = datetime.datetime.now()
        age = int(today.year) - int(year)

        response = info['response'][0]
        city = response['city']
        city_title = city['title']

        info_person = {
            'sex': sex,
            'city': city_title,
            'age_from': age,
            'age_to': age
        }
        return info_person
