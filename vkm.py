import requests
import datetime


class VKinder:
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    @staticmethod
    def get_candidate(self, users_params):
        url = 'https://api.vk.com/method/users.search'
        users_search = {
            'age_from': users_params['age_from'],
            'age_to': users_params['age_to'],
            'sex': users_params['sex'],
            'hometown': users_params['city'],
            'relation': 6,  # 6 в активном поиске
            'has_photo': 1,  # есть аватарка
            'count': 5,  # количество пользователей
        }
        res = requests.get(url, params={**self.params, **users_search})
        persons = res.json()
        return persons['response']['items']

    def get_users_data(self, params):
        candidates = {}
        items = self.get_candidate(self, params)
        for data_person in items:
            if (data_person['is_closed'] == False):
                app_dict = []
                id_person = int(data_person['id'])
                fotos_data = self.get_users_foto(self, id_person)
                fotos_data = sorted(fotos_data, key=lambda x: (x['likes']['count'], x['comments']['count']),
                                    reverse=True)
                fotos_data = fotos_data[0:3]
                for foto_person in fotos_data:
                    url_foto = foto_person['sizes'][0]['url']
                    app_dict.append({'url_foto': url_foto})
                candidates[id_person] = app_dict
        return candidates

    @staticmethod
    def get_users_foto(self, id_person):
        url_foto = 'https://api.vk.com/method/photos.get'
        foto_search = {
            'extended': '1',
            'owner_id': id_person,
            'count': 5,
            'album_id': 'profile',
            'rev': '0',
            'photo_sizes': 0
        }
        res_foto = requests.get(url_foto, params={**self.params, **foto_search})
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

        info_person = {
            'sex': sex,
            'city': info['response'][0]['city']['title'],
            'age_from': age,
            'age_to': age
        }
        return info_person
