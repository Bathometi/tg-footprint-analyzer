import os
import json
import asyncio
import argparse
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import User
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import GetCommonChatsRequest

# 1. Завантаження змінних оточення
load_dotenv()

API_ID = os.getenv('TG_API_ID')
API_HASH = os.getenv('TG_API_HASH')

if not API_ID or not API_HASH:
    print("[!] Помилка: Перевірте TG_API_ID та TG_API_HASH у файлі .env")
    exit(1)

async def extract_footprint(target, download_photo=True):
    client = TelegramClient('footprint_session', int(API_ID), API_HASH)
    await client.start()

    print(f"\n[*] 🔍 Запуск TG-Footprint-Analyzer для цілі: {target}")
    
    try:
        # Отримання базового об'єкта
        entity = await client.get_entity(target)

        if not isinstance(entity, User):
            print(f"[!] Вказана ціль {target} не є користувачем (можливо, це канал чи чат).")
            await client.disconnect()
            return

        # Запит повних даних (Bio) та спільних чатів
        full_user = await client(GetFullUserRequest(entity))
        common_chats = await client(GetCommonChatsRequest(user_id=entity.id, max_id=0, limit=100))

        # Обробка фото
        photo_path = None
        if download_photo and entity.photo:
            os.makedirs("downloads", exist_ok=True)
            photo_filename = f"downloads/avatar_{entity.id}.jpg"
            photo_path = await client.download_profile_photo(entity, file=photo_filename)

        # Створення JSON-структури
        footprint = {
            "query": target,
            "status": "success",
            "data": {
                "id": entity.id,
                "first_name": entity.first_name,
                "last_name": entity.last_name,
                "username": entity.username,
                "phone": entity.phone,
                "bio": full_user.full_user.about,
                "is_bot": entity.bot,
                "is_verified": entity.verified,
                "is_restricted": entity.restricted,
                "is_scam": entity.scam,
                "is_fake": entity.fake,
                "is_premium": getattr(entity, 'premium', False),
                "dc_id": entity.photo.dc_id if entity.photo else None
            },
            "relations": {
                "common_chats_count": len(common_chats.chats),
                "common_chats": [
                    {"id": chat.id, "title": chat.title, "username": getattr(chat, 'username', None)}
                    for chat in common_chats.chats
                ]
            },
            "media": {
                "has_photo": entity.photo is not None,
                "avatar_file": photo_path
            }
        }

        # Збереження JSON
        json_filename = f"report_{entity.id}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(footprint, f, indent=4, ensure_ascii=False)

        # Генерація Executive Summary (Текстового резюме)
        summary = f"""
==================================================
           TG OSINT EXECUTIVE SUMMARY             
==================================================
🎯 Запит: {target}
🆔 Telegram ID: {entity.id}
👤 Ім'я: {entity.first_name or ''} {entity.last_name or ''}
🏷️ Username: @{entity.username if entity.username else 'N/A'}
📞 Телефон: {entity.phone if entity.phone else 'Не повернуто поточній сесії'}
📝 Bio: {full_user.full_user.about if full_user.full_user.about else 'Відсутнє'}
🖼️ Profile Photo DC: {entity.photo.dc_id if entity.photo else 'N/A'}
🤖 Статус бота: {'Так' if entity.bot else 'Ні'}
⚠️ Позначки ризику (Scam/Fake): {'ТАК!' if entity.scam or entity.fake else 'Ні'}
💬 Спільних чатів виявлено: {len(common_chats.chats)}
🖼️ Аватарка: {'Завантажено (' + str(photo_path) + ')' if photo_path else 'Відсутня або пропущена'}
==================================================
📁 Повний JSON збережено у: {json_filename}
"""
        print(summary)

        # Збереження текстового зведення
        summary_filename = f"summary_{entity.id}.txt"
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write(summary)

    except Exception as e:
        print(f"[!] Помилка під час аналізу: {e}")

    finally:
        await client.disconnect()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TG-Footprint-Analyzer: Інструмент енумерації цифрового сліду в Telegram.")
    parser.add_argument("target", help="Username (наприклад @durov) або Telegram ID")
    parser.add_argument("--no-photo", action="store_true", help="Не завантажувати фото профілю")
    
    args = parser.parse_args()
    
    asyncio.run(extract_footprint(args.target, download_photo=not args.no_photo))
