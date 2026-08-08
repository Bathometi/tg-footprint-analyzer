import os
import sys
import json
import asyncio
import argparse

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import User
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import GetCommonChatsRequest


# --------------------------------------------------
# Environment configuration
# --------------------------------------------------

load_dotenv()

API_ID = os.getenv("TG_API_ID")
API_HASH = os.getenv("TG_API_HASH")

if not API_ID or not API_HASH:
    print("[!] Помилка: перевірте TG_API_ID та TG_API_HASH у файлі .env")
    sys.exit(1)

try:
    API_ID = int(API_ID)
except ValueError:
    print("[!] Помилка: TG_API_ID має бути числом.")
    sys.exit(1)


async def extract_footprint(target, download_photo=True):
    client = TelegramClient(
        "footprint_session",
        API_ID,
        API_HASH
    )

    try:
        await client.start()

        print(f"\n[*] 🔍 Запуск TG-Footprint-Analyzer для цілі: {target}")

        # Resolve target
        entity = await client.get_entity(target)

        if not isinstance(entity, User):
            print(
                f"[!] Вказана ціль {target} не є користувачем "
                "(можливо, це канал або чат)."
            )
            return

        # Get additional account data available to this session
        full_user = await client(GetFullUserRequest(entity))

        # Get common chats available to this session
        common_chats = await client(
            GetCommonChatsRequest(
                user_id=entity.id,
                max_id=0,
                limit=100
            )
        )

        # Profile photo
        photo_path = None

        if download_photo and entity.photo:
            os.makedirs("downloads", exist_ok=True)

            photo_filename = f"downloads/avatar_{entity.id}.jpg"

            photo_path = await client.download_profile_photo(
                entity,
                file=photo_filename
            )

        # Telegram-provided account flags
        telegram_flags = {
            "is_scam": entity.scam,
            "is_fake": entity.fake
        }

        # Structured local report
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
                "is_premium": getattr(entity, "premium", False),
                "profile_photo_dc_id": (
                    entity.photo.dc_id
                    if entity.photo
                    else None
                ),
                "telegram_flags": telegram_flags
            },
            "relations": {
                "common_chats_count": len(common_chats.chats),
                "common_chats": [
                    {
                        "id": chat.id,
                        "title": chat.title,
                        "username": getattr(chat, "username", None)
                    }
                    for chat in common_chats.chats
                ]
            },
            "media": {
                "has_photo": entity.photo is not None,
                "avatar_file": photo_path
            }
        }

        # Save JSON report
        json_filename = f"report_{entity.id}.json"

        with open(json_filename, "w", encoding="utf-8") as file:
            json.dump(
                footprint,
                file,
                indent=4,
                ensure_ascii=False
            )

        phone_display = (
            entity.phone
            if entity.phone
            else "Не повернуто поточній сесії"
        )

        bio_display = (
            full_user.full_user.about
            if full_user.full_user.about
            else "Відсутнє"
        )

        photo_dc_display = (
            entity.photo.dc_id
            if entity.photo
            else "N/A"
        )

        telegram_flags_display = (
            "YES"
            if entity.scam or entity.fake
            else "NO"
        )

        avatar_display = (
            f"Завантажено ({photo_path})"
            if photo_path
            else "Відсутня або пропущена"
        )

        # Human-readable summary
        summary = f"""
==================================================
              TG FOOTPRINT SUMMARY
==================================================
🎯 Запит: {target}
🆔 Telegram ID: {entity.id}
👤 Ім'я: {entity.first_name or ''} {entity.last_name or ''}
🏷️ Username: @{entity.username if entity.username else 'N/A'}
📞 Телефон: {phone_display}
📝 Bio: {bio_display}
🖼️ Profile Photo DC: {photo_dc_display}
🤖 Статус бота: {'Так' if entity.bot else 'Ні'}
🏷️ Telegram flags (Scam/Fake): {telegram_flags_display}
💬 Спільних чатів виявлено: {len(common_chats.chats)}
🖼️ Аватарка: {avatar_display}
==================================================
📁 Local JSON report: {json_filename}
"""

        print(summary)

        # Save text summary
        summary_filename = f"summary_{entity.id}.txt"

        with open(summary_filename, "w", encoding="utf-8") as file:
            file.write(summary)

    except Exception as error:
        print(f"[!] Помилка під час аналізу: {error}")

    finally:
        await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "TG-Footprint-Analyzer: educational tool for collecting "
            "Telegram metadata available to an authenticated session."
        )
    )

    parser.add_argument(
        "target",
        help="Telegram username або Telegram ID"
    )

    parser.add_argument(
        "--no-photo",
        action="store_true",
        help="Не завантажувати фото профілю"
    )

    args = parser.parse_args()

    asyncio.run(
        extract_footprint(
            args.target,
            download_photo=not args.no_photo
        )
    )
