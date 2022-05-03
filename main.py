import wikipedia
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import datetime
import random
import yandex_search
import random
import sqlite3
from vk_api import audio


n3 = False
wiki = wikipedia
wiki.set_lang('ru')
n = 0
n1 = 0
usli = []
frz = ['И снова здравствуйте! Не жалаете ли вы чего нибудь?', 'Рад вновь приветсвовать вас! Что желаете?'
                                                              "Давно не виделись! Как ваши дела, не нужна ли вам какая нибудь помощь?"]
token = '7e7c992a4e6c71cbf70e0c120dce5085ee8af3fc30f1549c508548ca4559194c06a0af31acc66c5cec793'
di = {}
yandex = yandex_search.Yandex(api_user='asdf', api_key='asdf')
helplist = ['выручай меня', 'спасай меня', 'мне очень нужна твоя помощь', 'выручай, мне без тебя не справиться',
            'не могли бы вы мне помочь?', 'помоги, пожалуйста', 'мне нужна помощь', 'у меня проблемы',
            "я не знаю что делать"]

def main():
    vk_session = vk_api.VkApi(
        token=token)
    longpoll = VkBotLongPoll(vk_session, '211774803')
    for event in longpoll.listen():
        help = ['Это действительно ужасно. Чтобы вам полегчало, советую вам обратиться к вашим друзьям... Никто не знает вас, лучше чем они, даже вы',
            'Если вам грустно, перейдите по данной ссылке, там может быть то, что вас развеселит: https://youtu.be/dQw4w9WgXcQ',
                        'Исследования показывают, что музыка помогает справляться с депрессией. Как вы относитесь к классике?',
            'Фонк может прибавить вам подрости, как думаете?']

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            user = event.obj.messege['from_id']
            if user not in usli:
                usli.append(user)
                di[user] = datetime.time.now
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Рад приветствовать вас в нашем сообществе! Я - Бот, и я Vаш лучший друk!'
                                         'Но вы можете обращаться ко мне и как Бк или Bk(англ). '
                                         'Вы можете обращаться ко мне за советом или за помощью, можете попросить меня найти какую нибудь информацию, либо вы можете попросить'
                                         'меня переместить ваше фото в альбом сообщества. Также я могу вызвать для вас список имеющихся в сообществе песен и список постоянно пополняется другими'
                                         'участниками. Вы и сами можете добавить свою песню по своим предпочтениям!'
                                         'Чтобы более подробо ознакомится о способах взаимодействовать со мной, а также с правилами данного сообщества, вы можете написать "Подробнее" или "Продолжай".'
                                         'Приятного общения!')
            elif (di[user] - datetime.time.now).seconds // 3600 > 0.5:
                di[user] = datetime.time.now
                n1 = 1
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=random.choice(frz))
            elif n1 == 0:
                if "подробнее" in (event.obj.messege['text']).lower or 'продолжай' in (event.obj.messege['text']).lower:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Что бы спросить совета, напишите: "Как...?" или "Почему...?".'
                                             'Если вы хотите поместить ваше фото в альбом, напишите "Вот моя фотка" или "Это моя фотка", файл с фотографией.'
                                             'Если хотите найти какую нибудь информацию, напишите "Поиск: ..."'
                                             'В случае, если вам нужна психологическая помощь, вы можете написать "У меня проблема" или "Мне нужна помощь"'
                                             'Я сделаю всё возможное, чтобы вы почувствовали себя лучше.')
            if "поиск:" in (event.obj.messege['text'][0, 7]).lower:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Вот то, что вы искали:\n' + wiki.summary(event.obj.message['text'][7, -1]))
            if "как" in event.obj.messege['text'] or "почему" in event.obj.messege['text']:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Вот, что мне удалось найти:\n' + yandex.search(
                                     (event.obj.message['text']).items['snippet']
                                     + 'Если вы хотите получить более подробную информацию по запросу, перейдите по ссылке:' +
                                     yandex.search((event.obj.message['text']).items)['url']))
            if "вот моя фотка:" in event.obj.messege['text'].lower() or "это моя фотка:" in event.obj.messege[
                'text'].lower():
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Ваша фотография помещена в альбом')
                filename = event.obj.message['text'][14, -1]
                upload = vk_api.VkUpload(vk_session)
                upload.photo(filename, album_id='285777333', group_id='211774803')
            for i in helplist:
                if i in event.obj.messege['text']:
                    a1 = random.choice(help)
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=a1)
                    n3 = True
                    break
            if n3:
                if 'нет' in event.obj.messege['text'].lower() or 'не' in event.obj.messege['text'].lower():
                    if help.index(a1) != len(help) - 1:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=help[help.index(a1) + 1])
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=help[help.index(a1) - 1])
                elif 'да' in event.obj.messege['text'].lower() or 'спасибо' in event.obj.messege['text'].lower() or 'спасибо!' in event.obj.messege['text'].lower() \
                    or 'помогло' in event.obj.messege['text'].lower():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Всегда рад помочь! Обращайтесь)!')
                    n3 = False



if __name__ == '__main__':
    main()
