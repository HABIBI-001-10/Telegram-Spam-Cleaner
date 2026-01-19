from telethon import TelegramClient, errors
from telethon.tl.types import Channel
import asyncio
from datetime import datetime
# Import config and spam detector
from config import (
    api_id, api_hash, MESSAGE_CHECK_LIMIT, SAFE_CHANNELS, 
    SPAM_THRESHOLD, MAX_LEAVES_PER_RUN, DELAY_SECONDS
)
from spam_detector import spam_probability

# 1. WHITELIST: Never leave channels containing these words (Case Insensitive)
NAME_WHITELIST = [
    "movie", "cinema", "film", "series", "ott", "dvd", 
    "malayalam", "kerala", "release", "junction", "club", 
    "hub", "request", "media", "entertainment", "troll"
]

# 2. BLACKLIST: Always leave channels containing these words
NAME_BLACKLIST = [
    "bitcoin", "crypto", "invest", "trading", "profit", 
    "money", "earn", "forex", "binance", "doubling", 
    "loot", "giveaway", "betting", "casino", "promotion"
]

client = TelegramClient("spam_ai_session", api_id, api_hash)

def check_keywords(name, keywords):
    """Returns True if any keyword is found in the name."""
    name_lower = name.lower()
    return any(kw in name_lower for kw in keywords)

async def main():
    leaves = 0
    print(f"--- Starting Cleanup (Threshold: {SPAM_THRESHOLD}) ---")
    
    async for dialog in client.iter_dialogs():
        if leaves >= MAX_LEAVES_PER_RUN:
            print(f"Reached max leaves limit ({MAX_LEAVES_PER_RUN}). Stopping.")
            break

        if not dialog.is_channel:
            continue
        
        # Skip manually defined safe channels
        if dialog.name in SAFE_CHANNELS or dialog.id in SAFE_CHANNELS:
            continue

        # Skip if you are the creator
        if isinstance(dialog.entity, Channel) and dialog.entity.creator:
            print(f"Skipping {dialog.name} (Creator)")
            continue

        # --- STEP 1: SAFETY CHECK (The "Movie" Protection) ---
        if check_keywords(dialog.name, NAME_WHITELIST):
            print(f"🛡️  SAFE: {dialog.name} (Matched Whitelist)")
            continue

        # --- STEP 2: INSTANT KILL (The "Crypto" Destroyer) ---
        is_obvious_spam = False
        if check_keywords(dialog.name, NAME_BLACKLIST):
            print(f"🚨 OBVIOUS SPAM: {dialog.name} (Matched Blacklist)")
            is_obvious_spam = True
            # We treat this as 100% spam, skipping message analysis
            avg_prob = 1.0 
        
        # --- STEP 3: MODEL CHECK (Only if not obvious) ---
        if not is_obvious_spam:
            print(f"Analyzing: {dialog.name}...")
            try:
                messages = await client.get_messages(dialog.id, limit=MESSAGE_CHECK_LIMIT)
            except Exception as e:
                print(f"  > Error: {e}")
                continue

            if not messages:
                continue

            probs = []
            for msg in messages:
                if msg.text:
                    probs.append(spam_probability(msg.text))
            
            if not probs:
                continue

            avg_prob = sum(probs) / len(probs)
            print(f"  > Score: {avg_prob:.2f}")

        # --- STEP 4: DECISION ---
        if avg_prob > SPAM_THRESHOLD:
            try:
                await client.delete_dialog(dialog.entity)
                leaves += 1
                
                log_type = "BLACKLIST" if is_obvious_spam else "MODEL"
                log_entry = (
                    f"{datetime.now()} | {log_type} | "
                    f"Channel: {dialog.name} | "
                    f"Score: {avg_prob:.2f}\n"
                )

                with open("leave_log.txt", "a", encoding="utf-8") as f:
                    f.write(log_entry)
                
                print(f"✅ LEFT {dialog.name}")
                await asyncio.sleep(DELAY_SECONDS)

            except errors.FloodWaitError as e:
                print(f"⚠️ FloodWait: Sleeping {e.seconds}s...")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"❌ Failed to leave: {e}")

    print("--- Run Complete ---")

with client:
    client.loop.run_until_complete(main())