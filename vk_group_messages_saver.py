import vk_api
import time
import vk_token
from datetime import datetime

token = vk_token.token_id
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

MESSAGES_COUNT = 100
CHAT_ID = 2000000000  # Замените на ID группового чата (peer_id)
FILE_NAME = input("Введите имя фала в который будет сохранена переписка из группового чата вк:   ")
FILE_NAME += ".txt"

USER_NAMES = {
    1234: 'Ivan Ivanov',
    4321: 'Pavel Popov',

}


def get_group_messages(chat_id, messages_count=100, offset=0):
    response = vk.messages.getHistory(peer_id=chat_id, count=messages_count, offset=offset)
    return response


def save_chat_history(messages, user_names, message_number, file):
    with open(file, 'a', encoding='utf-8') as f:
        for message in reversed(messages['items']):
            user_id = message.get('from_id', 'Unknown')
            if isinstance(user_id, int) and user_id in user_names:
                user_id = user_names[user_id]
            timestamp = message.get('date')
            readable_date = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S %d-%m-%Y')
            text = message.get('text', '').strip()
            if text:
                f.write('\n\n')
                f.write(f"---||| Message {message_number} |||---\n")
                f.write(f"From: {user_id}\n")
                f.write(f"At: {readable_date}\n")
                f.write("Message:\n")
                f.write(f"{text}\n")
                f.write('_' * 30 + '\n')
                f.write('/' * 15 + '\\' * 15 + '\n')
                message_number += 1
    return message_number


def parse_all_messages(chat_id, user_names, posts_count, file_name):
    messages = get_group_messages(chat_id, posts_count, offset=0)
    total_messages = messages['count']
    if total_messages == 0:
        print("Нет сообщений для обработки.")
        return None
    print(f"Всего сообщений в переписке: {total_messages}")
    quantity_pages = total_messages // 100
    offset = quantity_pages * posts_count
    message_number = 1
    while offset >= 0:
        messages = get_group_messages(chat_id, posts_count, offset)
        if messages['items']:
            print(f"Количество полученных сообщений: {len(messages['items'])}")
            message_number = save_chat_history(messages, user_names, message_number, file_name)
            print(f"Обработано сообщение: {message_number}")
            time.sleep(0.3)
            offset -= posts_count
        else:
            print("Сообщений для сохранения больше нет!")
            break


parse_all_messages(CHAT_ID, USER_NAMES, MESSAGES_COUNT, FILE_NAME)
