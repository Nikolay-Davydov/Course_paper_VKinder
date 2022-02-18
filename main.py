from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import vkm

token = 'token group'
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
VK_VERSION = '5.131'
VK_TOKEN = 'token user'


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })


def create_msg(vk_user):
    vkt = vkm.VKinder(token=VK_TOKEN, version=VK_VERSION)
    param_search = vkt.get_info_person(vk_user)
    candidates = vkt.get_users_data(param_search)
    for key, value in candidates.items():
        write_msg(event.user_id, "https://vk.com/id" + str(key))
        write_msg(event.user_id, "Photos:")
        for i in range(len(candidates[key])):
            write_msg(event.user_id, value[i]['url_foto'])


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            elif request == "Пара":
                write_msg(event.user_id, 'идет подбор')
                create_msg(event.user_id)
                write_msg(event.user_id, 'подбор закончен')
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")