import vk_api
import json
import vkm
import work_database
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = '13b1fc17e6319ca4ed55655319bc1ca5156391d4b800b5de376f026d1af618e1533e6190dcf53a777086b'
GROUP_TOKEN = '594f2b9f260fcc4169577facfb74fc5f196846c1b6b68cff17ebd24c1a8d446370f139b72f2bffb1f9137'
VK_VERSION = '5.131'

vk = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })


def create_msg(vk_user):
    vkt = vkm.VKinder(token=TOKEN, version=VK_VERSION)
    param_search = vkt.get_info_person(vk_user)
    person_db = work_database.workWithDatabase()
    person_db.create_table()
    current_ids = person_db.select_data(vk_user)
    if current_ids is not None:
        current_ids = list(current_ids)[0]
        insert = 0
    else:
        current_ids = []
        insert = 1
    candidates = vkt.get_users_data(param_search, current_ids)
    current_ids.extend(list(candidates.keys()))
    json_ids = json.dumps(current_ids)

    if insert:
        person_db.insert_data(vk_user, json_ids)
    else:
        person_db.update_date(json_ids, vk_user)

    for key, value in candidates.items():
        write_msg(event.user_id, "https://vk.com/id" + str(key))
        write_msg(event.user_id, "Photos:")
        for i in range(len(candidates[key])):
            write_msg(event.user_id, value[i]['url_foto'])


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text

            if request.lower() == "привет":
                write_msg(event.user_id, f"Привет, {event.user_id}")
            elif request.lower() == "пока":
                write_msg(event.user_id, "Пока((")
            elif request.lower() == "пара":
                write_msg(event.user_id, 'идет подбор')
                create_msg(event.user_id)
                write_msg(event.user_id, 'подбор закончен')
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
